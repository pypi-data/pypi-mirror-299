from typing import Literal, Optional, List, Union

import jsonargparse
import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback
from pytorch_lightning.loggers import Logger

from plasmidai.experimental.callbacks import GradNormMonitor
from plasmidai.experimental.lit import LitLLM
from plasmidai.paths import LOG_DIR, random_checkpoint_dir
from plasmidai.utils import configure_torch_backends


class SimpleTrainer(pl.Trainer):
    """
    A custom PyTorch Lightning Trainer with simplified configuration options.

    This trainer extends the functionality of pl.Trainer with pre-configured callbacks
    and logging options suitable for training language models.
    """

    def __init__(
        self,
        strategy: Literal["auto", "ddp"] = "auto",
        accelerator: Literal["cpu", "gpu"] = "cpu",
        devices: int = 1,
        precision: Literal["32", "16-mixed", "bf16-mixed", "bf16-true"] = "32",
        max_epochs: int = 50000,
        train_steps_per_epoch: Optional[int] = None,
        val_steps_per_epoch: Optional[int] = None,
        log_every_n_steps: int = 5,
        progress_bar: bool = False,
        wandb: bool = False,
        wandb_dir: str = str(LOG_DIR),
        wandb_project: str = "train_plasmid_llm",
        wandb_entity: Optional[str] = None,
        checkpoint: bool = False,
        checkpoint_dir: Optional[str] = None,
    ):
        """
        Initialize the SimpleTrainer with custom configuration.

        Args:
            strategy (Literal["auto", "ddp"]): The training strategy to use.
            accelerator (Literal["cpu", "gpu"]): The hardware accelerator to use.
            devices (int): Number of devices to use for training.
            precision (Literal["32", "16-mixed", "bf16-mixed", "bf16-true"]): Precision for training.
            max_epochs (int): Maximum number of epochs to train.
            train_steps_per_epoch (Optional[int]): Number of training steps per epoch.
            val_steps_per_epoch (Optional[int]): Number of validation steps per epoch.
            log_every_n_steps (int): Frequency of logging in steps.
            progress_bar (bool): Whether to enable progress bar.
            wandb (bool): Whether to use Weights & Biases for logging.
            wandb_dir (str): Directory for Weights & Biases logs.
            wandb_project (str): Weights & Biases project name.
            wandb_entity (Optional[str]): Weights & Biases entity.
            checkpoint (bool): Whether to enable checkpointing.
            checkpoint_dir (Optional[str]): Directory for saving checkpoints.
        """
        callbacks: List[Callback] = [pl.callbacks.ModelSummary(max_depth=2)]

        if checkpoint:
            callbacks.append(
                pl.callbacks.ModelCheckpoint(
                    dirpath=checkpoint_dir or random_checkpoint_dir(),
                    filename="epoch={epoch}-loss={val/loss_finetune:.3f}",
                    auto_insert_metric_name=False,
                    monitor="val/loss",
                    mode="min",
                    save_top_k=1,
                    save_last=True,
                    verbose=True,
                )
            )

        logger: Union[Logger, bool] = False
        if wandb:
            logger = pl.loggers.WandbLogger(
                project=wandb_project,
                entity=wandb_entity,
                log_model=False,
                save_dir=wandb_dir,
            )
            callbacks.extend(
                [
                    pl.callbacks.LearningRateMonitor(),
                    GradNormMonitor(),
                ]
            )

        super().__init__(
            accelerator=accelerator,
            devices=devices,
            precision=precision,
            strategy=strategy,
            callbacks=callbacks,
            enable_checkpointing=checkpoint,
            logger=logger,
            max_epochs=max_epochs,
            limit_train_batches=train_steps_per_epoch,
            limit_val_batches=val_steps_per_epoch,
            log_every_n_steps=log_every_n_steps,
            enable_progress_bar=progress_bar,
            reload_dataloaders_every_n_epochs=1,
            use_distributed_sampler=True,
        )


def train() -> None:
    """
    Main training function that sets up and runs the training process.

    This function parses command-line arguments, instantiates necessary classes,
    configures the training environment, and starts the training process.
    """
    parser = jsonargparse.ArgumentParser()

    # Populate arguments
    parser.add_function_arguments(configure_torch_backends, "backend")
    parser.add_subclass_arguments(pl.LightningDataModule, "data")
    parser.add_class_arguments(LitLLM, "lit")
    parser.add_class_arguments(SimpleTrainer, "trainer")
    parser.add_argument("--resume_path", type=Optional[str], default=None)
    parser.add_argument("--finetune_path", type=Optional[str], default=None)

    # Argument linking
    parser.link_arguments(
        "data.tokenizer_path", "lit.tokenizer_path", apply_on="instantiate"
    )

    # Parse
    cfg = parser.parse_args()

    # Instantiate
    init = parser.instantiate_classes(cfg)
    configure_torch_backends(**vars(cfg.backend))

    # Initialize and load model
    if cfg.finetune_path is not None:
        raise NotImplementedError()

    # Start training
    for logger in init.trainer.loggers:
        logger.log_hyperparams(cfg.as_dict())
    init.trainer.fit(model=init.lit, datamodule=init.data, ckpt_path=cfg.resume_path)


if __name__ == "__main__":
    train()
