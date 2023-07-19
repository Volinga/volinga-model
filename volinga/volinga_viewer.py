from nerfstudio.configs import base_config as cfg
from nerfstudio.utils.writer import WandbWriter
from nerfstudio.utils.writer import EVENT_WRITERS, TensorboardWriter, CONSOLE
from pathlib import Path
from typing import Optional
from volinga.volinga_base_config import WandbConfig
import wandb



def setup_event_writer(
    is_wandb_enabled: bool,
    is_tensorboard_enabled: bool,
    log_dir: Path,
    wandb_config: Optional[WandbConfig] = None
) -> None:
    """Initialization of all event writers specified in config
    Args:
        config: configuration to instantiate loggers
        max_iter: maximum number of train iterations
        banner_messages: list of messages to always display at bottom of screen
    """
    using_event_writer = False
    if is_wandb_enabled:
        curr_writer = VolingaWandbWriter(log_dir=log_dir, wandb_config = wandb_config)
        EVENT_WRITERS.append(curr_writer)
        using_event_writer = True
    if is_tensorboard_enabled:
        curr_writer = TensorboardWriter(log_dir=log_dir)
        EVENT_WRITERS.append(curr_writer)
        using_event_writer = True
    if using_event_writer:
        string = f"logging events to: {log_dir}"
    else:
        string = "Disabled tensorboard/wandb event writers"
    CONSOLE.print(f"[bold yellow]{string}")


class VolingaWandbWriter(WandbWriter):
    def __init__(self, log_dir: Path, wandb_config: Optional[WandbConfig] = None):
        if wandb_config:
            wandb.init(id=wandb_config.run_id, project=wandb_config.project, dir=str(log_dir))
        else:
            super().__init__(log_dir)