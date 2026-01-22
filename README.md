# Video-to-3D Room Reconstruction from Monocular Video

This repository contains a Python-based pipeline for reconstructing a 3D representation
of an indoor environment from a monocular video (MP4).

The project automates the full workflow from video frames to a dense 3D point cloud
and surface mesh. It focuses on preprocessing, pipeline orchestration, visualization,
and export of results, while relying on a proven external SfM/MVS engine.

---

## Overview

The goal of this project is to convert a handheld video of a room into a usable 3D
representation suitable for visualization, inspection, or further processing.

The pipeline performs:
- video frame extraction,
- sparse Structure-from-Motion reconstruction (camera poses + sparse points),
- dense Multi-View Stereo reconstruction,
- depth map fusion into a dense point cloud,
- surface mesh generation,
- visualization and export to common 3D formats.

This repository does not reimplement SfM or MVS algorithms from scratch. Instead, it
provides a clean, reproducible, and extensible automation layer around an established
reconstruction engine.

---

## Pipeline Components

- Video preprocessing and frame extraction: **:contentReference[oaicite:0]{index=0}**
- Structure-from-Motion (SfM) and Multi-View Stereo (MVS): **:contentReference[oaicite:1]{index=1}**
- Visualization and export of 3D data: **:contentReference[oaicite:2]{index=2}**

---

## Requirements

### System
- Windows 10 / 11 (64-bit)
- NVIDIA GPU with CUDA support (recommended)
- COLMAP installed separately and available in system PATH

### Python
- Python 3.9 or newer
- Dependencies listed in `requirements.txt`

Install Python dependencies:
```bash
pip install -r requirements.txt
COLMAP Installation
COLMAP must be installed independently of this repository.

For Windows with NVIDIA GPU, download the CUDA-enabled binary from the official releases page:
https://github.com/colmap/colmap/releases

After installation, verify that COLMAP is accessible:


colmap -h
If the help message is shown, COLMAP is correctly installed.

Project Structure

room3d-video-reconstruction/
├── src/
│   ├── main.py        # Entry point for reconstruction
│   ├── pipeline.py    # COLMAP pipeline orchestration
│   ├── viewer.py      # Visualization using Open3D
│   └── exporter.py    # Export utilities
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
Usage
Run reconstruction from video

python src/main.py \
  --video path/to/room.mp4 \
  --fps 1.5 \
  --max_frames 500 \
  --work work \
  --export_dir exports
Output files
After successful execution, the following files are produced:

room_pointcloud.ply — dense point cloud

room.obj — surface mesh

room.glb — mesh in GLB format

Visualization
To visualize the generated point cloud or mesh, specify the file path directly inside
viewer.py:

GEOMETRY_PATH = r"C:\path\to\exports\room_pointcloud.ply"
Then run:


python src/viewer.py
An interactive Open3D window will open, allowing rotation, zooming, and inspection
of the reconstructed scene.

Notes and Limitations
Reconstruction quality strongly depends on video quality and camera motion.

Slow camera movement with large frame overlap is recommended.

Motion blur, poor lighting, and textureless surfaces may reduce reconstruction quality.

High-resolution videos (e.g., 4K) significantly increase processing time.

License
The code in this repository is released under the MIT License.

COLMAP is licensed under the BSD License and is distributed separately.

Credits and Citation
This project uses COLMAP for Structure-from-Motion (SfM) and Multi-View Stereo (MVS)
reconstruction.

COLMAP is developed by Johannes L. Schönberger and collaborators.
The official source code is available at:
https://github.com/colmap/colmap

If you use this project for academic or research purposes, please cite the original
COLMAP publications:

@inproceedings{schoenberger2016sfm,
  author    = {Johannes L. Sch{\"o}nberger and Jan-Michael Frahm},
  title     = {Structure-from-Motion Revisited},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016}
}

@inproceedings{schoenberger2016mvs,
  author    = {Johannes L. Sch{\"o}nberger and Enliang Zheng and Marc Pollefeys and Jan-Michael Frahm},
  title     = {Pixelwise View Selection for Unstructured Multi-View Stereo},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2016}
}
