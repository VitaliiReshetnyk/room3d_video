# Video-to-3D Room Reconstruction from Monocular Video

This repository provides a Python-based pipeline for reconstructing a 3D representation
of an indoor environment from a monocular video (MP4).  
The project automates the complete workflow from raw video frames to a dense 3D point cloud
and a surface mesh.

Rather than reimplementing Structure-from-Motion (SfM) and Multi-View Stereo (MVS) algorithms
from scratch, this repository focuses on building a clean, reproducible, and extensible
automation layer around a proven external reconstruction engine.

---

## Overview

The goal of this project is to convert a handheld video of a room into a usable 3D
representation suitable for visualization, inspection, and further processing.

The pipeline performs the following steps:

1. Extract frames from an input video (MP4)
2. Perform sparse Structure-from-Motion reconstruction (camera poses + sparse points)
3. Run dense Multi-View Stereo reconstruction
4. Fuse depth maps into a dense point cloud
5. Generate a surface mesh
6. Visualize and export results to common 3D formats

This repository is intended for research, educational use, and rapid prototyping of
video-based indoor 3D reconstruction pipelines.

---

## Technologies Used

- **OpenCV** — video preprocessing and frame extraction  
- **COLMAP** — Structure-from-Motion (SfM) and Multi-View Stereo (MVS) reconstruction  
- **Open3D** — visualization and export of 3D data  

COLMAP is used strictly as an external dependency and is not distributed with this repository.

---

## System Requirements

- Windows 10 / 11 (64-bit)
- Python 3.9 or newer
- Separate installation of COLMAP (CUDA-enabled NVIDIA GPU strongly recommended)

---

## Python Dependencies

All required Python packages are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

## COLMAP Installation

COLMAP must be installed independently and available in the system PATH.

For Windows systems with NVIDIA GPUs, download the CUDA-enabled binary from the official
COLMAP releases page:

https://github.com/colmap/colmap/releases

## Project Structure

```
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
```

## Usage

Run reconstruction from video
```
python src/main.py \
  --video path/to/room.mp4 \
  --fps 1.5 \
  --max_frames 500 \
  --work work \
  --export_dir exports
```

## Output Files

After successful execution, the following files are generated:
-room_pointcloud.ply — dense point cloud
-room.obj — surface mesh
-room.glb — mesh in GLB format

## Notes and Limitations

Reconstruction quality strongly depends on video quality and camera motion.
Slow camera movement with large frame overlap is recommended.
Motion blur, poor lighting, and textureless surfaces may reduce reconstruction quality.
High-resolution videos (e.g. 4K) significantly increase processing time.

## License

The code in this repository is released under the MIT License.
COLMAP is licensed separately under the BSD License and is distributed independently.

## Credits and Citation

This project uses COLMAP for Structure-from-Motion (SfM) and Multi-View Stereo (MVS)
reconstruction.

COLMAP is developed by Johannes L. Schönberger and collaborators.
Official source code: https://github.com/colmap/colmap

If you use this project for academic or research purposes, please cite the original
COLMAP publications:
```bibtex
@inproceedings{schoenberger2016sfm,
  author    = {Johannes L. Schönberger and Jan-Michael Frahm},
  title     = {Structure-from-Motion Revisited},
  booktitle = {Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016}
}

@inproceedings{schoenberger2016mvs,
  author    = {Johannes L. Schönberger and Enliang Zheng and Marc Pollefeys and Jan-Michael Frahm},
  title     = {Pixelwise View Selection for Unstructured Multi-View Stereo},
  booktitle = {European Conference on Computer Vision (ECCV)},
  year      = {2016}
}
```
