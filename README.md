
<p align="center">
    <!-- pypi-strip -->
    <picture>
    <img alt="Volinga" src="https://volinga.ai/early_access/Volinga%20Suite%20-%20User%20Manual%206d1d5b9c2a2046829b2e2cbe16d112f8/MicrosoftTeams-image_(73).png">
    <!-- pypi-strip -->
    </picture>
    <!-- /pypi-strip -->
    <a href="https://discord.gg/XxVdfWvcge"><img src="https://img.shields.io/badge/Join-Discord-blue.svg"/></a>
</p>

# About
Volinga's vision is to enable the use of Neural Radiance Fields for any use case by providing the first platform for frictionless creation and native rendering in 3D engines. This repo provides an extension to nerfstudio, implementing volinga model, a modification of Nerfacto that allows the conversion to NVOL file, using Volinga Exporter. NVOL files can be rendered in Unreal Engine and disguise RenderStream using Volinga Renderer. 

Log in to unleash the power of NeRF into Unreal Engine: https://volinga.ai/

# Installation
Volinga follows the integration described in [nerfstudio](https://docs.nerf.studio/en/latest/developer_guides/new_methods.html) for custom methods. You will need to install nerfstudio first, and then add Volinga integration.


## 0. Prerequisites

### 0.1. Cuda
You must have an NVIDIA video card with CUDA installed on the system. This library has been tested with version 11.8 of CUDA. You can find more information about installing CUDA [here](https://docs.nvidia.com/cuda/cuda-quick-start-guide/index.html)

### 0.2. Create environment

Volinga requires `python >= 3.8`. We recommend using conda to manage dependencies. Make sure to install [Conda](https://docs.conda.io/en/latest/miniconda.html) before proceeding.

```bash
conda create --name volinga -y python=3.8
conda activate volinga
python -m pip install --upgrade pip
```


## 1. Install nerfstudio  v0.3.2
Nerfstudio v0.3.2 is the last compatible version with Volinga Exporter. To install it, follow these steps:

### 1.1. Install Dependencies

Install pytorch with CUDA (this repo has been tested with CUDA 11.7 and CUDA 11.8) and [tiny-cuda-nn](https://github.com/NVlabs/tiny-cuda-nn)

For CUDA 11.7:

```bash
pip install torch==2.0.1+cu117 torchvision==0.15.2+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

For CUDA 11.8:

```bash
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
```

See [Dependencies](https://github.com/nerfstudio-project/nerfstudio/blob/main/docs/quickstart/installation.md#dependencies)
in the Installation documentation for more.

### 1.2. Install nerfstudio

You can now install nerfstudio v0.3.2 using the following command:

```bash
pip install nerfstudio==0.3.2
```

## 2. Clone Volinga repo
```bash
git clone https://github.com/Volinga/volinga-model
```

## 3. Install Volinga repo as a python package

```bash
cd volinga_model
pip install -e .
```

## 4. Install tab completion from Nerfstudio

```bash
ns-install-cli
```

## 5. Checking the install
The following command should include `volinga` as one of the options:
```bash
ns-train -h
```

# Using Volinga
Now that Volinga is installed, you can unleash the power of NeRF:
```bash
ns-train volinga --data /path/to/your/data --vis viewer
```

## Previsualization
You can generate a previsualization video of you Volinga NeRF by using:

```bash
volinga-preview --output-format [images, video] --load-config path/or/your/config/config.yml --traj interpolate --eval-num-rays-per-chunk [int] --output-path /output/path --order_poses --adjust_frame_rate
```
