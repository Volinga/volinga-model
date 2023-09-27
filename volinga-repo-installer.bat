@echo off
IF "%~1"=="-windows11" (
    SET cuda_installer=https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe
)
IF "%~1"=="-windows10" (
    SET cuda_installer=https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe
)

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://aka.ms/vs/16/release/vs_buildtools.exe','vs_buildtools.exe')"
start /WAIT vs_buildtools.exe --passive --wait --add "Microsoft.VisualStudio.Workload.VCTools;includeRecomended;includeOptional" --add "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"


curl %cuda_installer% -o cuda.exe 
start /WAIT cuda.exe -s

winget install --id Git.Git -e --source winget
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe', 'python3.exe')"
start /WAIT python3.exe /quiet Include_pip=1 Include_launcher=1
set PATH=%PATH%;%localappdata%\Programs\Python\Python310\Scripts
set PATH=%PATH%;C:\Program Files\Git\cmd

pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
pip3 install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
pip3 install git+https://github.com/Volinga/volinga-model
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')
tar -xf ffmpeg.zip
move ffmpeg-master-latest-win64-gpl C:\ffmpeg
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/colmap/colmap/releases/download/3.8/COLMAP-3.8-windows-cuda.zip', 'colmap.zip')
tar -xf colmap.zip
move COLMAP-3.8-windows-cuda C:\Colmap
echo %PATH%

IF "%~2%"=="-setPath" (
  setx PATH "%PATH%;C:\Colmap;C:\ffmpeg\bin"
)
