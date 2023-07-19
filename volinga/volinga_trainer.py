from dataclasses import dataclass, field
from typing import Type, Literal
from pathlib import Path
import dataclasses
from nerfstudio.utils import profiler, writer
from nerfstudio.engine.callbacks import TrainingCallback, TrainingCallbackAttributes, TrainingCallbackLocation
from torch.cuda.amp.grad_scaler import GradScaler
from nerfstudio.engine.trainer import Trainer, TrainerConfig, TORCH_DEVICE, CONSOLE
from nerfstudio.viewer.server.viewer_state import ViewerState
from nerfstudio.viewer_beta.viewer import Viewer as ViewerBetaState
from volinga.volinga_base_config import WandbConfig
from volinga.volinga_viewer import setup_event_writer


@dataclass
class VolingaTrainerConfig(TrainerConfig):
    """Configuration for the Volinga trainer."""
    _target: Type = field(default_factory=lambda: VolingaTrainer)
    """target class to instantiate"""
    vis: Literal["viewer", "wandb", "tensorboard", "viewer+wandb", "viewer+tensorboard", "viewer_beta", "volinga_wandb"] = "wandb"
    """Which visualizer to use."""
    wandb: WandbConfig = WandbConfig()
    """Wandb configuration"""

class VolingaTrainer(Trainer):
    def __init__(self, config: TrainerConfig, local_rank: int = 0, world_size: int = 1) -> None:
        super().__init__(config, local_rank, world_size)

    def setup(self, test_mode: Literal["test", "val", "inference"] = "val") -> None:
          """Setup the Trainer by calling other setup functions.

          Args:
              test_mode:
                  'val': loads train/val datasets into memory
                  'test': loads train/test datasets into memory
                  'inference': does not load any dataset into memory
          """
          self.pipeline = self.config.pipeline.setup(
              device=self.device,
              test_mode=test_mode,
              world_size=self.world_size,
              local_rank=self.local_rank,
              grad_scaler=self.grad_scaler,
          )
          self.optimizers = self.setup_optimizers()

          # set up viewer if enabled
          viewer_log_path = self.base_dir / self.config.viewer.relative_log_filename
          self.viewer_state, banner_messages = None, None
          if self.config.is_viewer_enabled() and self.local_rank == 0:
              datapath = self.config.data
              if datapath is None:
                  datapath = self.base_dir
              self.viewer_state = ViewerState(
                  self.config.viewer,
                  log_filename=viewer_log_path,
                  datapath=datapath,
                  pipeline=self.pipeline,
                  trainer=self,
                  train_lock=self.train_lock,
              )
              banner_messages = [f"Viewer at: {self.viewer_state.viewer_url}"]
          if self.config.is_viewer_beta_enabled() and self.local_rank == 0:
              self.viewer_state = ViewerBetaState(
                  self.config.viewer,
                  log_filename=viewer_log_path,
                  datapath=self.base_dir,
                  pipeline=self.pipeline,
                  trainer=self,
                  train_lock=self.train_lock,
              )
              banner_messages = [f"Viewer Beta at: {self.viewer_state.viewer_url}"]
          self._check_viewer_warnings()

          self._load_checkpoint()

          self.callbacks = self.pipeline.get_training_callbacks(
              TrainingCallbackAttributes(
                  optimizers=self.optimizers,
                  grad_scaler=self.grad_scaler,
                  pipeline=self.pipeline,
              )
          )

          # set up writers/profilers if enabled
          writer_log_path = self.base_dir / self.config.logging.relative_log_dir
          setup_event_writer(
              self.config.is_wandb_enabled(),
              self.config.is_tensorboard_enabled(),
              log_dir=writer_log_path,
              wandb_config=self.config.wandb
          )
          writer.setup_local_writer(
              self.config.logging, max_iter=self.config.max_num_iterations, banner_messages=banner_messages
          )
          writer.put_config(name="config", config_dict=dataclasses.asdict(self.config), step=0)
          profiler.setup_profiler(self.config.logging, writer_log_path)