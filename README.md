
# 🧠 End-to-End MRI Analysis: Disease Classification & 3D Mesh Generation

This repository contains a two-phase pipeline for processing and analyzing clinical MRI data. 
* **Phase 1** focuses on AI-driven disease classification using deep learning. 
* **Phase 2** focuses on computational geometry, automatically extracting and generating watertight 3D CAD models (Virtual Twins) from the raw voxel data for physical simulation.

---

## 🔬 Phase 1: Alzheimer's Detection using ResNet50 and InceptionV3
# Alzheimer Detection using ResNet50 and InceptionV3

## Overview
This project classifies MRI brain scans into 4 Alzheimer's stages using transfer learning on InceptionV3 and ResNet50, both pretrained on ImageNet. The dataset is class-balanced via SMOTE before training.

**4 classes:** NonDemented (ND), VeryMildDemented (VMD), MildDemented (MILD_D), ModerateDemented (MOD_D)

## Dataset
- 6,407 MRI images across 4 classes (imbalanced)
- SMOTE oversampling → 12,832 balanced samples
- Image size: 150×150
- Augmentation: brightness range [0.8, 1.2], zoom [0.99, 1.01], horizontal flip
- Split: 80% train / 20% validation / 20% test (sequential splits)

## Models

### InceptionV3
- Pretrained InceptionV3 (ImageNet weights, top layers frozen)
- Custom head: GlobalAveragePooling → Flatten → BatchNorm → Dense(512) → Dense(256) → Dense(128) → Dense(64) → Dense(4, softmax)
- Dropout(0.5) + BatchNormalization throughout
- Optimizer: Adam | Loss: CategoricalCrossentropy | Epochs: 40
- Metrics tracked: Accuracy, Precision, Recall, AUC

### ResNet50
- Pretrained ResNet50 (ImageNet weights)
- Fine-tuned on the same 4-class MRI dataset

## Performance
InceptionV3 achieves the highest test accuracy of **91.43%** with AUC **0.9686**.

| Metric | InceptionV3 |
|---|---|
| Test Accuracy | 91.43% |
| AUC | 0.9686 |
| Macro F1 | 0.86 |
| Precision | 0.837 |
| Recall | 0.816 |

Evaluated with per-class classification report and confusion matrix heatmap.
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