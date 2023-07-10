# Volinga
Volinga model is a modification of Nerfacto that allows the conversion to NVOL file, that can be rendered in Unreal Engine.

# Installation
Volinga follows the integration described in [Nerfstudio](https://docs.nerf.studio/en/latest/developer_guides/new_methods.html) for custom methods.

## 1. Install Nerfstudio dependencies
Follow the instructions given in the [official  documentation](https://docs.nerf.studio/en/latest/quickstart/installation.html) up to and including tinycudann.

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
The following command shoud include `volinga` as one of the options:
```bash
ns-train -h
```

# Using Volinga
Now that Volinga is installed, you can unleash the power of NeRF in virtual production:
```bash
ns-train volinga --data /path/to/your/data --vis viewer
```

## Previsualization
You can do a previsualization of the NeRF by using:

```bash
volinga-preview --output-format [images, video] --load-config path/or/your/config/config.yml --traj interpolate --eval-num-rays-per-chunk [int] --output-path /output/path --order_poses --adjust_frame_rate
```
