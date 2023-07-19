from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, Type
from nerfstudio.configs.base_config import PrintableConfig

@dataclass
class WandbConfig(PrintableConfig):
    """Configuration for wandb visualizer instantiation"""

    run_id: Optional[str] = None
    """wandb run id"""
    project: Optional[str] = "volinga"
    """wandb project"""