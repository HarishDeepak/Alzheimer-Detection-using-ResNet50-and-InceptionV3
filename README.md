
# 🧠 End-to-End MRI Analysis: Disease Classification & 3D Mesh Generation

This repository contains a two-phase pipeline for processing and analyzing clinical MRI data. 
* **Phase 1** focuses on AI-driven disease classification using deep learning. 
* **Phase 2** focuses on computational geometry, automatically extracting and generating watertight 3D CAD models (Virtual Twins) from the raw voxel data for physical simulation.

---

## 🔬 Phase 1: Alzheimer's Detection using ResNet50 and InceptionV3
# Alzheimer Detection using ResNet50 and InceptionV3

## Overview
This project focuses on detecting Alzheimer's disease using two powerful convolutional neural networks: ResNet50 and InceptionV3. These models are pretrained on the ImageNet dataset and are fine-tuned to classify MRI images for Alzheimer detection.

## Features
- Utilizes ResNet50 and InceptionV3 architectures for Alzheimer detection.
- Includes scripts for preprocessing MRI images and evaluating model performance.
- Implements transfer learning to adapt the pretrained models to the Alzheimer's MRI dataset.

## Performance
The project compares the performance of the two models, with InceptionV3 achieving the highest test accuracy of 91.43%.
---

## ⚙️ Phase 2: Automated 3D Segmentation & Mesh Generator (BioEM Ready)
**Folder:** `/3D_Mesh_Generation`

This pipeline converts raw clinical MRI data (NIfTI) into smoothed, watertight 3D CAD geometries (STL). This tool bridges the gap between medical imaging and physical 3D modeling, allowing researchers and engineers to generate simulation-ready anatomical structures without manual CAD tracing.

### The Automation Pipeline
This script processes medical imaging data through a robust computer vision pipeline:
1. **Gaussian Smoothing (Pre-processing):** Suppresses high-frequency magnetic noise from the raw scan.
2. **Intensity Thresholding:** Isolates specific tissue types based on voxel intensity values.
3. **Morphological Closing:** Acts as a digital "shrink-wrap" to bridge anatomical air cavities (e.g., mouth, sinuses) and seal the mesh.
4. **Marching Cubes Algorithm:** Extracts the 3D surface geometry from the processed voxel array.
5. **Artifact Cleanup:** Algorithmically identifies and deletes disconnected floating scanner noise, keeping only the primary watertight anatomical structure.

### Usage
Navigate to the `3D_Mesh_Generation` folder and ensure you have the required scientific computing libraries installed (`numpy scipy scikit-image trimesh nibabel`).

```bash
python mri_to_mesh.py