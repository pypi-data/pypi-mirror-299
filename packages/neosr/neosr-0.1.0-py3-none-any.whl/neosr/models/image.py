import math
import sys
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING, Any

import torch
from torch import Tensor
from torch.nn import functional as F
from torch.optim.swa_utils import AveragedModel, get_ema_multi_avg_fn
from tqdm import tqdm

from neosr.archs import build_network
from neosr.data.augmentations import apply_augment
from neosr.losses import build_loss
from neosr.losses.wavelet_guided import wavelet_guided
from neosr.metrics import calculate_metric
from neosr.models.base import base
from neosr.optimizers import adamw_sf, adan, adan_sf, fsam
from neosr.utils import get_root_logger, imwrite, tc, tensor2img
from neosr.utils.registry import MODEL_REGISTRY

if TYPE_CHECKING:
    from torch.optim.optimizer import Optimizer


@MODEL_REGISTRY.register()
class image(base):
    """Single-Image Super-Resolution model."""

    def __init__(self, opt: dict[str, Any]) -> None:
        super().__init__(opt)

        # define network net_g
        self.net_g = build_network(opt["network_g"])
        self.net_g = self.model_to_device(self.net_g)  # type: ignore[reportArgumentType,reportArgumentType,arg-type]
        if self.opt["path"].get("print_network", False) is True:
            self.print_network(self.net_g)

        # define network net_d
        self.net_d = self.opt.get("network_d", None)
        if self.net_d is not None:
            self.net_d = build_network(self.opt["network_d"])
            self.net_d = self.model_to_device(self.net_d)  # type: ignore[reportArgumentType]
            if self.opt.get("print_network", False) is True:
                self.print_network(self.net_d)

        # load pretrained g
        load_path = self.opt["path"].get("pretrain_network_g", None)
        if load_path is not None:
            param_key = self.opt["path"].get("param_key_g")
            self.load_network(
                self.net_g,
                load_path,
                param_key,
                self.opt["path"].get("strict_load_g", True),
            )

        # load pretrained d
        load_path = self.opt["path"].get("pretrain_network_d", None)
        if load_path is not None:
            param_key = self.opt["path"].get("param_key_d")
            self.load_network(
                self.net_d,
                load_path,
                param_key,
                self.opt["path"].get("strict_load_d", True),
            )

        if self.is_train:
            self.init_training_settings()

    def init_training_settings(self) -> None:
        # options var
        train_opt = self.opt["train"]
        # initialize logger
        logger = get_root_logger()

        # set EMA
        self.ema = self.opt["train"].get("ema", -1)
        if self.ema > 0:
            self.net_g_ema = AveragedModel(
                self.net_g,  # type: ignore[reportArgumentType,arg-type]
                multi_avg_fn=get_ema_multi_avg_fn(self.ema),
                device=self.device,
            )
            logger.info("Using exponential-moving average.")

        # sharpness-aware minimization
        self.sam = self.opt["train"].get("sam", None)
        self.sam_init = self.opt["train"].get("sam_init", -1)

        # set up optimizers and schedulers
        self.setup_optimizers()
        self.setup_schedulers()

        # set nets to training mode
        self.net_g.train()  # type: ignore[reportAttributeAccessIssue,attr-defined]
        if self.sf_optim_g and self.is_train:
            self.optimizer_g.train()  # type: ignore[attr-defined]

        if self.net_d is not None:
            self.net_d.train()  # type: ignore[reportArgumentType]
            if self.sf_optim_d and self.is_train:
                self.optimizer_d.train()  # type: ignore[attr-defined]

        # scale ratio var
        self.scale = self.opt["scale"]

        # patch size var
        self.patch_size = self.opt["datasets"]["train"].get("patch_size")

        # augmentations
        self.aug = self.opt["datasets"]["train"].get("augmentation", None)
        self.aug_prob = self.opt["datasets"]["train"].get("aug_prob", None)

        # for amp
        self.use_amp = self.opt.get("use_amp", False) is True
        self.amp_dtype = (
            torch.bfloat16 if self.opt.get("bfloat16", False) is True else torch.float16
        )

        self.gradscaler_g = torch.amp.GradScaler(
            "cuda", enabled=self.use_amp, init_scale=2.0**5
        )
        if self.net_d is not None:
            self.gradscaler_d = torch.amp.GradScaler("cuda", enabled=self.use_amp)

        # LQ matching for Color/Luma losses
        self.match_lq_colors = self.opt["train"].get("match_lq_colors", False)

        # Total expected iters
        self.total_iter = self.opt["train"].get("total_iter", 200000)

        # enable ECO optimization:
        self.eco = self.opt["train"].get("eco", False)
        # ECO alpha scheduling
        self.eco_schedule = self.opt["train"].get("eco_schedule", "sigmoid")
        # ECO amount of iters
        self.eco_iters = self.opt["train"].get("eco_iters", 80000)
        # ECO init iters
        self.eco_init = self.opt["train"].get("eco_init", 15000)
        # using pretrain?
        self.pretrain = self.opt["path"].get("pretrain_network_g", None)

        # initialise counter of how many batches has to be accumulated
        self.n_accumulated = 0
        self.accum_iters = self.opt["datasets"]["train"].get("accumulate", 1)
        if self.accum_iters in {0, None}:
            self.accum_iters = 1

        # pixel loss
        if train_opt.get("pixel_opt"):
            self.cri_pix = build_loss(train_opt["pixel_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_pix = None

        # mssim loss
        if train_opt.get("mssim_opt"):
            self.cri_mssim = build_loss(train_opt["mssim_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_mssim = None

        # consistency loss
        if train_opt.get("consistency_opt"):
            self.cri_consistency = build_loss(train_opt["consistency_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_consistency = None

        # vgg19 perceptual loss
        if train_opt.get("perceptual_opt"):
            self.cri_perceptual = build_loss(train_opt["perceptual_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_perceptual = None

        if train_opt.get("dists_opt"):
            self.cri_dists = build_loss(train_opt["dists_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_dists = None

        # gan loss
        if train_opt.get("gan_opt"):
            self.cri_gan = build_loss(train_opt["gan_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_gan = None

        # ldl loss
        if train_opt.get("ldl_opt"):
            self.cri_ldl = build_loss(train_opt["ldl_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_ldl = None

        # focal-frequency loss
        if train_opt.get("ff_opt"):
            self.cri_ff = build_loss(train_opt["ff_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_ff = None

        # gradient-weighted loss
        if train_opt.get("gw_opt"):
            self.cri_gw = build_loss(train_opt["gw_opt"]).to(  # type: ignore[reportCallIssue,attr-defined]
                self.device, memory_format=torch.channels_last, non_blocking=True
            )
        else:
            self.cri_gw = None

        # wavelet-guided loss
        self.wavelet_guided = self.opt["train"].get("wavelet_guided", False)
        self.wavelet_init = self.opt["train"].get("wavelet_init", 0)
        if self.wavelet_guided:
            logger.info("Loss [Wavelet-Guided] enabled.")

        # gradient clipping
        self.gradclip = self.opt["train"].get("grad_clip", True)

        # log sam
        if self.sam is not None:
            logger.info("Sharpness-Aware Minimization enabled.")

        # log eco
        if self.eco:
            logger.info("ECO enabled.")

        # error handling
        optim_d = self.opt["train"].get("optim_d", None)
        pix_losses_bool = self.cri_pix or self.cri_mssim is not None
        percep_losses_bool = self.cri_perceptual or self.cri_dists is not None

        if self.sam is not None and self.use_amp is True:
            # Closure not supported:
            # https://github.com/pytorch/pytorch/blob/main/torch/amp/grad_scaler.py#L384
            msg = f"""{tc.red}SAM does not support GradScaler. As a result, AMP could cause
                      instability with it. Disable AMP if you get undesirable results.{tc.end}"""
            logger.warning(msg)
        if self.sam is not None and self.accum_iters > 1:
            msg = f"{tc.red}SAM can't be used with gradient accumulation yet.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if pix_losses_bool is False and percep_losses_bool is False:
            msg = f"{tc.red}Both pixel/mssim and perceptual losses are None. Please enable at least one.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.net_d is None and optim_d is not None:
            msg = f"{tc.red}Please set a discriminator in network_d or disable optim_d.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.net_d is not None and optim_d is None:
            msg = f"{tc.red}Please set an optimizer for the discriminator or disable network_d.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.net_d is not None and self.cri_gan is None:
            msg = f"{tc.red}Discriminator needs GAN to be enabled.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.net_d is None and self.cri_gan is not None:
            msg = f"{tc.red}GAN requires a discriminator to be set.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.aug is not None and self.patch_size % 4 != 0:
            msg = f"{tc.red}The patch_size value must be a multiple of 4. Please change it.{tc.end}"
        if self.wavelet_guided and self.cri_gan is None:
            msg = f"{tc.red}Wavelet-Guided requires GAN.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        if self.net_d is not None:  # noqa: SIM102
            if (
                self.opt["network_d"].get("type") == "ea2fpn"
                and self.patch_size == 48
                and self.scale == 1
            ):
                msg = f"""
                {tc.red}
                Discriminator ea2fpn does not work with patch_size 48 while doing 1x ratio.
                Please increase or decrease patch_size.
                {tc.end}
                """
                logger.error(msg)
                sys.exit(1)

    def setup_optimizers(self) -> None:
        train_opt = self.opt["train"]
        optim_params = []
        logger = get_root_logger()
        for k, v in self.net_g.named_parameters():  # type: ignore[reportAttributeAccessIssue,attr-defined]
            if v.requires_grad:
                optim_params.append(v)
            else:
                logger.warning(f"Params {k} will not be optimized.")
        # optimizer g
        optim_type = train_opt["optim_g"].pop("type")
        # condition for schedule_free
        if (
            optim_type in {"AdamW_SF", "adamw_sf", "adan_sf", "Adan_SF"}
            and "schedule_free" not in train_opt["optim_g"]
        ):
            msg = f"{tc.red}The option 'schedule_free' must be in the config file.{tc.end}"
            logger.error(msg)
            sys.exit(1)
        # get optimizer g
        self.optimizer_g = self.get_optimizer(
            optim_type, optim_params, **train_opt["optim_g"]
        )
        self.optimizers.append(self.optimizer_g)

        # SAM
        if self.sam is not None:
            if optim_type in {"AdamW", "adamw"}:
                base_optimizer: type[Optimizer] = torch.optim.AdamW  # type: ignore[reportPrivateImportUsage]
            elif optim_type in {"Adan", "adan"}:
                base_optimizer = adan
            elif optim_type in {"AdamW_SF", "adamw_sf"}:
                base_optimizer = adamw_sf
            elif optim_type in {"Adan_SF", "adan_sf"}:
                base_optimizer = adan_sf
            else:
                msg = (
                    f"{tc.red}SAM not supported by optimizer {optim_type} yet.{tc.end}"
                )
                logger.error(msg)
                sys.exit(1)

            if self.sam in {"FSAM", "fsam"}:
                self.sam_optimizer_g = fsam(
                    optim_params,
                    base_optimizer,
                    rho=0.5,
                    sigma=1,
                    lmbda=0.9,
                    adaptive=True,
                    **train_opt["optim_g"],
                )
            elif self.sam is not None:
                msg = f"{tc.red}SAM type {self.sam} not supported yet.{tc.end}"
                logger.error(msg)
                sys.exit(1)
            else:
                pass

        # optimizer d
        if self.net_d is not None:
            optim_type = train_opt["optim_d"].pop("type")
            # condition for schedule_free
            if (
                optim_type in {"AdamW_SF", "adamw_sf", "adan_sf", "Adan_SF"}
                and "schedule_free" not in train_opt["optim_d"]
            ):
                msg = f"{tc.red}The option 'schedule_free' must be in the config file.{tc.end}"
                logger.error(msg)
                sys.exit(1)
            # get optimizer d
            self.optimizer_d = self.get_optimizer(
                optim_type,
                self.net_d.parameters(),  # type: ignore[reportAttributeAccessIssue]
                **train_opt["optim_d"],
            )
            self.optimizers.append(self.optimizer_d)

    @torch.no_grad()
    def feed_data(self, data: dict[str, str | Tensor]) -> None:
        self.lq = data["lq"].to(self.device, non_blocking=True)  # type: ignore[union-attr]
        if "gt" in data:
            self.gt = data["gt"].to(self.device, non_blocking=True)  # type: ignore[union-attr]

        # augmentation
        if self.is_train and self.aug is not None:
            if len(self.aug) == 1 and "none" in self.aug:
                pass
            else:
                self.gt, self.lq = apply_augment(
                    self.gt,
                    self.lq,
                    scale=self.scale,
                    augs=self.aug,
                    prob=self.aug_prob,
                )

    def eco_strategy(self, current_iter: int):
        """Adapted version of "Empirical Centroid-oriented Optimization":
        https://arxiv.org/abs/2312.17526.
        """
        with torch.no_grad():
            # define alpha with sigmoid-like curve, slope/skew at 0.25
            if self.eco_schedule == "sigmoid":
                a = 1 / (
                    1 + math.exp(-1 * (10 * (current_iter / self.eco_iters - 0.25)))
                )
            else:
                a = min(current_iter / self.eco_iters, 1.0)
            # network prediction
            self.net_output = self.net_g(self.lq)  # type: ignore[reportCallIssue,operator]
            # define gt centroid
            self.gt = ((1 - a) * self.net_output) + (a * self.gt)
            # downsampled prediction
            self.lq_scaled = torch.clamp(
                F.interpolate(
                    self.net_output,
                    scale_factor=1 / self.scale,
                    mode="bicubic",
                    antialias=True,
                ),
                0,
                1,
            )
            # define lq centroid
            self.output = ((1 - a) * self.lq_scaled) + (a * self.lq)
        # predict from lq centroid
        self.output = self.net_g(self.output)  # type: ignore[reportCallIssue,operator]

        return self.output, self.gt

    def closure(self, current_iter: int):
        if self.net_d is not None:
            for p in self.net_d.parameters():  # type: ignore[reportAttributeAccessIssue,operator]
                p.requires_grad = False

        # increment accumulation counter
        self.n_accumulated += 1
        # reset accumulation counter
        if self.n_accumulated >= self.accum_iters:
            self.n_accumulated = 0

        with torch.autocast(
            device_type="cuda", dtype=self.amp_dtype, enabled=self.use_amp
        ):
            # eco
            if self.eco and current_iter <= self.eco_iters:
                if current_iter < self.eco_init and self.pretrain is None:
                    self.output = self.net_g(self.lq)  # type: ignore[reportCallIssue,operator]
                else:
                    self.output, self.gt = self.eco_strategy(current_iter)
            else:
                self.output = self.net_g(self.lq)  # type: ignore[reportCallIssue,operator]

            # lq match
            if self.match_lq_colors:
                with torch.no_grad():
                    self.lq_interp = torch.clamp(
                        F.interpolate(
                            self.lq,
                            scale_factor=self.scale,
                            mode="bicubic",
                            antialias=True,
                        ),
                        1 / 255,
                        1,
                    )

            # wavelet guided loss
            if self.wavelet_guided and current_iter >= self.wavelet_init:
                with torch.no_grad():
                    combined_HF, combined_HF_gt = wavelet_guided(self.output, self.gt)

            l_g_total: Tensor = torch.zeros(1)
            loss_dict = OrderedDict()

            # pixel loss
            if self.cri_pix:
                l_g_pix = self.cri_pix(self.output, self.gt)
                l_g_total += l_g_pix
                loss_dict["l_g_pix"] = l_g_pix
            # ssim loss
            if self.cri_mssim:
                l_g_mssim = self.cri_mssim(self.output, self.gt)
                l_g_total += l_g_mssim
                loss_dict["l_g_mssim"] = l_g_mssim
            # consistency loss
            if self.cri_consistency:
                if self.match_lq_colors:
                    l_g_consistency = self.cri_consistency(self.output, self.lq_interp)
                else:
                    l_g_consistency = self.cri_consistency(self.output, self.gt)
                l_g_total += l_g_consistency
                loss_dict["l_g_consistency"] = l_g_consistency
            # perceptual loss
            if self.cri_perceptual:
                l_g_percep = self.cri_perceptual(self.output, self.gt)
                l_g_total += l_g_percep
                loss_dict["l_g_percep"] = l_g_percep
            # dists loss
            if self.cri_dists:
                l_g_dists = self.cri_dists(self.output, self.gt)
                l_g_total += l_g_dists
                loss_dict["l_g_dists"] = l_g_dists
            # ldl loss
            if self.cri_ldl:
                l_g_ldl = self.cri_ldl(self.output, self.gt)
                l_g_total += l_g_ldl
                loss_dict["l_g_ldl"] = l_g_ldl
            # focal frequency loss
            if self.cri_ff:
                l_g_ff = self.cri_ff(self.output, self.gt)
                l_g_total += l_g_ff
                loss_dict["l_g_ff"] = l_g_ff
            # gradient-weighted loss
            if self.cri_gw:
                l_g_gw = self.cri_gw(self.output, self.gt)
                l_g_total += l_g_gw
                loss_dict["l_g_gw"] = l_g_gw
            # gan loss
            if self.cri_gan:
                fake_g_pred = self.net_d(self.output)  # type: ignore[reportCallIssue,reportOptionalCall]
                l_g_gan = self.cri_gan(fake_g_pred, target_is_real=True, is_disc=False)
                l_g_total += l_g_gan
                loss_dict["l_g_gan"] = l_g_gan

        # add total generator loss for tensorboard tracking
        loss_dict["l_g_total"] = l_g_total

        # divide losses by accumulation factor
        l_g_total /= self.accum_iters
        # backward generator
        if self.sam and current_iter >= self.sam_init:
            l_g_total.backward()
        else:
            self.gradscaler_g.scale(l_g_total).backward()  # type: ignore[reportFunctionMemberAccess,attr-defined]

        if (
            self.n_accumulated % self.accum_iters == 0
            and self.gradclip
            and not (self.sam is not None and current_iter >= self.sam_init)
        ):
            # gradient clipping on generator
            self.gradscaler_g.unscale_(self.optimizer_g)  # type: ignore[reportFunctionMemberAccess,attr-defined]
            torch.nn.utils.clip_grad_norm_(
                self.net_g.parameters(),  # type: ignore[reportAttributeAccessIssue,attr-defined]
                1.0,
                error_if_nonfinite=False,
            )

        # optimize net_d
        if self.net_d is not None:
            for p in self.net_d.parameters():  # type: ignore[reportAttributeAccessIssue,attr-defined]
                p.requires_grad = True

            with torch.autocast(
                device_type="cuda", dtype=self.amp_dtype, enabled=self.use_amp
            ):
                if self.cri_gan:
                    # real
                    if self.wavelet_guided and current_iter >= self.wavelet_init:
                        real_d_pred = self.net_d(combined_HF_gt)  # type: ignore[reportPossiblyUnboundVariable]
                    else:
                        real_d_pred = self.net_d(self.gt)  # type: ignore[reportCallIssue]

                    l_d_real = self.cri_gan(
                        real_d_pred, target_is_real=True, is_disc=True
                    )

                    l_d_real /= self.accum_iters

                    loss_dict["l_d_real"] = l_d_real
                    loss_dict["out_d_real"] = torch.mean(real_d_pred.detach())

                    # fake
                    if self.wavelet_guided and current_iter >= self.wavelet_init:
                        fake_d_pred = self.net_d(combined_HF.detach())  # type: ignore[reportPossiblyUnboundVariable]
                    else:
                        fake_d_pred = self.net_d(self.output.detach())  # type: ignore[reportCallIssue]

                    l_d_fake = self.cri_gan(
                        fake_d_pred, target_is_real=False, is_disc=True
                    )

                    l_d_fake /= self.accum_iters

                    loss_dict["l_d_fake"] = l_d_fake
                    loss_dict["out_d_fake"] = torch.mean(fake_d_pred.detach())

                    # add total discriminator loss for tensorboard tracking
                    loss_dict["l_d_total"] = (l_d_real + l_d_fake) / 2

                    # backward discriminator
                    if self.sam and current_iter >= self.sam_init:
                        l_d_real.backward()
                        l_d_fake.backward()
                    else:
                        self.gradscaler_d.scale(l_d_real).backward()  # type: ignore[reportFunctionMemberAccess,attr-defined]
                        self.gradscaler_d.scale(l_d_fake).backward()  # type: ignore[reportFunctionMemberAccess,attr-defined]

            # clip discriminator
            if (
                self.n_accumulated % self.accum_iters == 0
                and self.gradclip
                and not (self.sam is not None and current_iter >= self.sam_init)
            ):
                # gradient clipping on discriminator
                self.gradscaler_d.unscale_(self.optimizer_d)  # type: ignore[reportFunctionMemberAccess,attr-defined]
                torch.nn.utils.clip_grad_norm_(
                    self.net_d.parameters(),  # type: ignore[reportAttributeAccessIssue,attr-defined]
                    1.0,
                    error_if_nonfinite=False,
                )

        # error if NaN
        if torch.isnan(l_g_total):
            msg = f"""
                  {tc.red}
                  NaN found, aborting training. Make sure you're using a proper learning rate.
                  If you have AMP enabled, try using bfloat16. For more information:
                  https://github.com/muslll/neosr/wiki/Configuration-Walkthrough
                  {tc.end}
                  """
            raise ValueError(msg)

        # average losses among gpu's, if doing distributed training
        self.log_dict = self.reduce_loss_dict(loss_dict)

        # return generator loss
        return l_g_total

    def optimize_parameters(self, current_iter: int) -> None:
        # increment accumulation counter
        self.n_accumulated += 1
        # reset accumulation counter
        if self.n_accumulated >= self.accum_iters:
            self.n_accumulated = 0

        # run forward-backward
        self.closure(current_iter)

        if (self.n_accumulated) % self.accum_iters == 0:
            # step() for generator
            if self.sam and current_iter >= self.sam_init:
                self.sam_optimizer_g.step(self.closure, current_iter)
            else:
                self.gradscaler_g.step(self.optimizer_g)  # type: ignore[reportFunctionMemberAccess,attr-defined]
            # step() for discriminator
            if self.net_d is not None:
                self.gradscaler_d.step(self.optimizer_d)  # type: ignore[reportFunctionMemberAccess,attr-defined]

            # zero generator grads
            if self.sam and current_iter >= self.sam_init:
                self.sam_optimizer_g.zero_grad(set_to_none=True)
            else:
                # update gradscaler
                self.gradscaler_g.update()  # type: ignore[reportFunctionMemberAccess,attr-defined]
                if self.net_d is not None:
                    self.gradscaler_d.update()  # type: ignore[reportFunctionMemberAccess,attr-defined]
                self.optimizer_g.zero_grad(set_to_none=True)

            # zero discriminator grads
            if self.net_d is not None:
                self.optimizer_d.zero_grad(set_to_none=True)

            if self.ema > 0:
                self.net_g_ema.update_parameters(self.net_g)  # type: ignore[reportArgumentType,arg-type]

    def test(self) -> None:
        self.tile = self.opt["val"].get("tile", -1)
        scale = self.opt["scale"]
        if self.tile == -1:
            if self.sf_optim_g and self.is_train:
                self.optimizer_g.eval()  # type: ignore[attr-defined]

            with torch.inference_mode():
                if hasattr(self, "ema"):
                    if self.ema > 0:
                        self.net_g_ema.eval()
                        self.output = self.net_g_ema(self.lq)
                else:
                    self.net_g.eval()  # type: ignore[reportAttributeAccessIssue,attr-defined]
                    self.output = self.net_g(self.lq)  # type: ignore[reportCallIssue,operator]

            self.net_g.train()  # type: ignore[reportAttributeAccessIssue,attr-defined]
            if self.sf_optim_g and self.is_train:
                self.optimizer_g.train()  # type: ignore[attr-defined]
        # test by partitioning
        else:
            _, C, h, w = self.lq.size()

            if self.opt.get("color", None) == "y":
                C = 1

            split_token_h = h // self.tile + 1  # number of horizontal cut sections
            split_token_w = w // self.tile + 1  # number of vertical cut sections

            patch_size_tmp_h = split_token_h
            patch_size_tmp_w = split_token_w

            # padding
            mod_pad_h, mod_pad_w = 0, 0
            if h % patch_size_tmp_h != 0:
                mod_pad_h = patch_size_tmp_h - h % patch_size_tmp_h
            if w % patch_size_tmp_w != 0:
                mod_pad_w = patch_size_tmp_w - w % patch_size_tmp_w

            img = self.lq
            img = torch.cat([img, torch.flip(img, [2])], 2)[:, :, : h + mod_pad_h, :]
            img = torch.cat([img, torch.flip(img, [3])], 3)[:, :, :, : w + mod_pad_w]

            _, _, H, W = img.size()
            split_h = H // split_token_h  # height of each partition
            split_w = W // split_token_w  # width of each partition

            # overlapping
            shave_h = 16
            shave_w = 16
            ral = H // split_h
            row = W // split_w
            slices = []  # list of partition borders
            for i in range(ral):
                for j in range(row):
                    if i == 0 and i == ral - 1:
                        top = slice(i * split_h, (i + 1) * split_h)
                    elif i == 0:
                        top = slice(i * split_h, (i + 1) * split_h + shave_h)
                    elif i == ral - 1:
                        top = slice(i * split_h - shave_h, (i + 1) * split_h)
                    else:
                        top = slice(i * split_h - shave_h, (i + 1) * split_h + shave_h)
                    if j == 0 and j == row - 1:
                        left = slice(j * split_w, (j + 1) * split_w)
                    elif j == 0:
                        left = slice(j * split_w, (j + 1) * split_w + shave_w)
                    elif j == row - 1:
                        left = slice(j * split_w - shave_w, (j + 1) * split_w)
                    else:
                        left = slice(j * split_w - shave_w, (j + 1) * split_w + shave_w)
                    temp = (top, left)
                    slices.append(temp)
            img_chops = []  # list of partitions
            for temp in slices:
                top, left = temp
                img_chops.append(img[..., top, left])

            if self.is_train:
                if self.ema > 0:
                    self.net_g_ema.eval()
                else:
                    self.net_g.eval()  # type: ignore[reportAttributeAccessIssue,attr-defined]
            else:
                self.net_g.eval()  # type: ignore[reportAttributeAccessIssue,attr-defined]

            if self.sf_optim_g and self.is_train:
                self.optimizer_g.eval()  # type: ignore[attr-defined]

            with torch.inference_mode():
                outputs = []
                for chop in img_chops:
                    if self.is_train:
                        out = self.net_g_ema(chop) if self.ema > 0 else self.net_g(chop)  # type: ignore[reportCallIssue,operator]
                    else:
                        out = self.net_g(chop)  # type: ignore[reportCallIssue,operator]

                    outputs.append(out)
                _img = torch.zeros(1, C, H * scale, W * scale)
                # merge
                for i in range(ral):
                    for j in range(row):
                        top = slice(i * split_h * scale, (i + 1) * split_h * scale)
                        left = slice(j * split_w * scale, (j + 1) * split_w * scale)
                        if i == 0:
                            _top = slice(0, split_h * scale)
                        else:
                            _top = slice(shave_h * scale, (shave_h + split_h) * scale)
                        if j == 0:
                            _left = slice(0, split_w * scale)
                        else:
                            _left = slice(shave_w * scale, (shave_w + split_w) * scale)
                        _img[..., top, left] = outputs[i * row + j][..., _top, _left]
                self.output = _img
            self.net_g.train()  # type: ignore[reportAttributeAccessIssue,attr-defined]
            if self.sf_optim_g and self.is_train:
                self.optimizer_g.train()  # type: ignore[attr-defined]
            _, _, h, w = self.output.size()
            self.output = self.output[
                :, :, 0 : h - mod_pad_h * scale, 0 : w - mod_pad_w * scale
            ]

    def dist_validation(
        self, dataloader, current_iter: int, tb_logger, save_img: bool = True
    ) -> None:
        if self.opt["rank"] == 0:
            self.nondist_validation(dataloader, current_iter, tb_logger, save_img)

    def nondist_validation(
        self, dataloader, current_iter: int, tb_logger, save_img: bool = True
    ) -> None:
        # flag to not apply augmentation during val
        self.is_train = False
        dataset_name = dataloader.dataset.opt["name"]
        dataset_type = dataloader.dataset.opt["type"]
        # progress bar
        use_pbar = self.opt["val"].get("pbar", True)

        if dataset_type == "single":
            with_metrics = False
        else:
            with_metrics = self.opt["val"].get("metrics") is not None

        if with_metrics:
            if not hasattr(self, "metric_results"):  # only execute in the first run
                self.metric_results: dict[str, float] = dict.fromkeys(
                    self.opt["val"]["metrics"].keys(), 0
                )
            # initialize the best metric results for each dataset_name (supporting multiple validation datasets)
            self._initialize_best_metric_results(dataset_name)
        # zero self.metric_results
        if with_metrics:
            self.metric_results = dict.fromkeys(self.metric_results, 0)

        if use_pbar:
            pbar = tqdm(
                total=len(dataloader), unit="image", colour="green", ascii=" >="
            )

        metric_data = {}

        for _idx, val_data in enumerate(dataloader):
            img_name = Path(Path(val_data["lq_path"][0]).name).stem
            self.feed_data(val_data)
            self.test()

            visuals = self.get_current_visuals()
            sr_img = tensor2img([visuals["result"]])
            metric_data["img"] = sr_img
            if "gt" in visuals:
                gt_img = tensor2img([visuals["gt"]])
                metric_data["img2"] = gt_img
                del self.gt

            # tentative for out of GPU memory
            del self.lq
            del self.output
            torch.cuda.empty_cache()

            # check if dataset has save_img option, and if so overwrite global save_img option
            save_img = self.opt["val"].get("save_img", True)
            val_suffix = self.opt["val"].get("suffix", None)
            if save_img:
                if self.opt["is_train"]:
                    save_img_path = (
                        Path(self.opt["path"]["visualization"])
                        / img_name
                        / f"{img_name}_{current_iter}.png"
                    )
                elif val_suffix is not None:
                    save_img_path = (
                        Path(self.opt["path"]["visualization"])
                        / dataset_name
                        / f'{img_name}_{self.opt["val"]["suffix"]}.png'
                    )
                else:
                    save_img_path = (
                        Path(self.opt["path"]["visualization"])
                        / dataset_name
                        / f'{img_name}_{self.opt["name"]}.png'
                    )
                imwrite(sr_img, str(save_img_path))  # type: ignore[arg-type]
                # TODO: add original lq and gt to results folder, once

            # check for dataset option save_tb, to save images on tb_logger
            if self.is_train:
                save_tb_img = self.opt["logger"].get("save_tb_img", False)
                if save_tb_img:
                    sr_img_tb = tensor2img([visuals["result"]], rgb2bgr=False)
                    tb_logger.add_image(
                        f"{img_name}/{current_iter}",
                        sr_img_tb,
                        global_step=current_iter,
                        dataformats="HWC",
                    )

            if with_metrics:
                # calculate metrics
                for name, opt_ in self.opt["val"]["metrics"].items():
                    self.metric_results[name] += calculate_metric(metric_data, opt_)  # type: ignore[reportOperatorIssue]
            if use_pbar:
                pbar.update(1)  # type: ignore[reportPossiblyUnboundVariable]
                pbar.set_description(f"{tc.light_green}Inferring on {img_name}{tc.end}")  # type: ignore[reportPossiblyUnboundVariable]

        if use_pbar:
            pbar.close()  # type: ignore[reportPossiblyUnboundVariable]

        if with_metrics:
            for metric in self.metric_results:
                self.metric_results[metric] /= _idx + 1  # type: ignore[reportPossiblyUnboundVariable]
                # update the best metric result
                self._update_best_metric_result(
                    dataset_name, metric, self.metric_results[metric], current_iter
                )

            self._log_validation_metric_values(current_iter, dataset_name, tb_logger)

        self.is_train = True

    def _log_validation_metric_values(
        self, current_iter: int, dataset_name: str, tb_logger
    ) -> None:
        log_str = f"Validation {dataset_name}\n\n"
        for metric, value in self.metric_results.items():
            log_str += f"\t # {metric}: {value:.4f}"
            if hasattr(self, "best_metric_results"):
                log_str += (
                    f'{tc.light_green}........ Best: {self.best_metric_results[dataset_name][metric]["val"]:.4f} @ '
                    f'{self.best_metric_results[dataset_name][metric]["iter"]} iter{tc.end}'
                )
            log_str += "\n"

        logger = get_root_logger()
        logger.info(log_str)
        if tb_logger:
            for metric, value in self.metric_results.items():
                tb_logger.add_scalar(
                    f"metrics/{dataset_name}/{metric}", value, current_iter
                )

    def get_current_visuals(self) -> OrderedDict:
        out_dict = OrderedDict()
        out_dict["lq"] = self.lq.detach().cpu()
        out_dict["result"] = self.output.detach().cpu()
        if hasattr(self, "gt"):
            out_dict["gt"] = self.gt.detach().cpu()
        return out_dict

    def save(self, epoch: int, current_iter: int) -> None:
        """Save networks and training state."""
        if self.ema > 0:
            self.save_network(self.net_g_ema, "net_g", current_iter)
        else:
            self.save_network(self.net_g, "net_g", current_iter)

        if self.net_d is not None:
            self.save_network(self.net_d, "net_d", current_iter)

        self.save_training_state(epoch, current_iter)

    def _print_different_keys_loading(
        self, crt_net, load_net: dict[Any, Any], strict: bool = True
    ) -> None:
        """Print keys with different name or different size when loading models.

        1. Print keys with different names.
        2. If strict=False, print the same key but with different tensor size.
            It also ignore these keys with different sizes (not load).

        Args:
        ----
            crt_net (torch model): Current network.
            load_net (dict): Loaded network.
            strict (bool): Whether strictly loaded. Default: True.

        """
        crt_net = self.get_bare_model(crt_net)
        crt_net = crt_net.state_dict()
        crt_net_keys = set(crt_net.keys())
        load_net_keys = set(load_net.keys())

        logger = get_root_logger()
        if crt_net_keys != load_net_keys:
            logger.warning("Current net - loaded net:")
            for v in sorted(crt_net_keys - load_net_keys):
                logger.warning(f"  {v}")
            logger.warning("Loaded net - current net:")
            for v in sorted(load_net_keys - crt_net_keys):
                logger.warning(f"  {v}")

        # check the size for the same keys
        if not strict:
            common_keys = crt_net_keys & load_net_keys
            for k in common_keys:
                if crt_net[k].size() != load_net[k].size():
                    logger.warning(
                        f"Size different, ignore [{k}]: crt_net: "
                        f"{crt_net[k].shape}; load_net: {load_net[k].shape}"
                    )
                    load_net[k + ".ignore"] = load_net.pop(k)
