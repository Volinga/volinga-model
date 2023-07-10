"""
Volinga configuration file
"""

from nerfstudio.cameras.camera_optimizers import CameraOptimizerConfig
from nerfstudio.configs.base_config import ViewerConfig
from nerfstudio.plugins.types import MethodSpecification


from nerfstudio.data.datamanagers.base_datamanager import VanillaDataManagerConfig

from nerfstudio.data.dataparsers.nerfstudio_dataparser import NerfstudioDataParserConfig
from nerfstudio.engine.optimizers import AdamOptimizerConfig

from nerfstudio.engine.trainer import TrainerConfig
from nerfstudio.models.nerfacto import NerfactoModelConfig
from nerfstudio.pipelines.base_pipeline import VanillaPipelineConfig


volinga_method = MethodSpecification(
    TrainerConfig(
        method_name="volinga",
        steps_per_eval_batch=500,
        steps_per_save=2000,
        max_num_iterations=30000,
        mixed_precision=True,
        pipeline=VanillaPipelineConfig(
            datamanager=VanillaDataManagerConfig(
                dataparser=NerfstudioDataParserConfig(),
                train_num_rays_per_batch=4096,
                eval_num_rays_per_batch=4096,
                camera_optimizer=CameraOptimizerConfig(
                    mode="SO3xR3", optimizer=AdamOptimizerConfig(lr=6e-4, eps=1e-8, weight_decay=1e-2)
                ),
            ),
            model=NerfactoModelConfig(
                eval_num_rays_per_chunk=1 << 15,
                hidden_dim=32,
                hidden_dim_color=32,
                hidden_dim_transient=32,
                num_nerf_samples_per_ray=24,
                proposal_net_args_list=[
                    {"hidden_dim": 16, "log2_hashmap_size": 17, "num_levels": 5, "max_res": 128, "use_linear": True},
                    {"hidden_dim": 16, "log2_hashmap_size": 17, "num_levels": 5, "max_res": 256, "use_linear": True},
                ],
            ),
        ),
        optimizers={
            "proposal_networks": {
                "optimizer": AdamOptimizerConfig(lr=1e-2, eps=1e-15),
                "scheduler": None,
            },
            "fields": {
                "optimizer": AdamOptimizerConfig(lr=1e-2, eps=1e-15),
                "scheduler": None,
            },
        },
        viewer=ViewerConfig(num_rays_per_chunk=1 << 15),
        vis="viewer",
    ),
    description="Real-time rendering model from Volinga. Directly exportable to NVOL format at https://volinga.ai/"
)
