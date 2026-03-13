# 🧠 Automated 3D Segmentation & Mesh Generator for MRI

An automated Python pipeline that converts raw clinical MRI data (NIfTI) into smoothed, watertight 3D CAD geometries (STL). This tool is designed to bridge the gap between medical imaging and physical 3D modeling, allowing researchers and engineers to generate simulation-ready anatomical structures without hours of manual CAD tracing.

## 🎯 Project Objective
In fields ranging from biomechanics to electromagnetic simulation, accurate physical models of human anatomy are strictly required. This project automates the extraction of specific tissues (e.g., skin, bone, or brain matter) from 3D voxel data, mathematically cleans scanner artifacts, and exports high-fidelity geometries ready for structural or physics simulations.

## ⚙️ The Automation Pipeline
This script processes medical imaging data through a robust 6-step computer vision pipeline:
1. **Data Ingestion:** Reads compressed NIfTI (`.nii.gz`) MRI scans.
2. **Gaussian Smoothing (Pre-processing):** Suppresses high-frequency magnetic noise from the raw scan.
3. **Intensity Thresholding:** Isolates specific tissue types based on voxel intensity values.
4. **Morphological Closing:** Acts as a digital "shrink-wrap" to bridge anatomical air cavities (e.g., mouth, sinuses) and seal the mesh.
5. **Marching Cubes Algorithm:** Extracts the 3D surface geometry from the processed voxel array.
6. **Artifact Cleanup:** Algorithmically identifies and deletes disconnected floating scanner noise, keeping only the primary watertight anatomical structure.

---

## 🔬 Concepts & Medical Imaging Theory

### 1. Voxels & Intensity Values
An MRI is not a standard 2D image; it is a 3D grid of data points called **voxels** (volumetric pixels). Every voxel contains an intensity value representing the physical properties of that specific 1mm block of space. Air registers near `0`, soft tissues register mid-range, and dense structures register highly. By targeting specific value ranges, we can digitally segment specific organs.

### 2. The "Air Cavity" Problem & Morphological Closing
MRI scanners do not detect air. Because the mouth, sinuses, and eye sockets contain air, they register as `0` intensity. A standard surface-extraction algorithm will draw the mesh *inside* these cavities, resulting in an incomplete or "hollow" model. 
* **The Solution:** We apply **Morphological Closing** (`scipy.ndimage.binary_closing`). This mathematical operation rolls a digital sphere over the 3D data, bridging narrow gaps and sealing the face into a continuous, watertight solid necessary for accurate physical simulations.

### 3. The Marching Cubes Algorithm
A classic computer graphics algorithm that iterates through a 3D scalar field (our MRI voxel grid). It locates the exact coordinates where the voxel values cross our defined tissue threshold, generating triangles (faces) and vertices to construct a continuous polygonal 3D surface.

---

## 🛠️ What to Tweak (Hyperparameters)

If you are using a different MRI scan, the contrast and scanner intensity will vary. You can tune the following parameters inside the script to achieve the perfect tissue extraction:

* `TISSUE_THRESHOLD` **(Default: 80 - 100)**
  * **Lower it:** If the mesh has holes or looks "eaten away." This includes more low-intensity soft tissue.
  * **Raise it:** To mathematically "peel" the anatomy. A high threshold (e.g., `400+`) will bypass the skin/fat and generate a 3D model of only the densest structures, like the skull or brain folds.
* `sigma` **(Default: 1.0)**
  * Controls the Gaussian blur. Increase to `1.5` or `2.0` for a smoother, clay-like CAD model. Decrease to `0.5` if you need high-fidelity anatomical details (but risk picking up scanner noise).
* `iterations` **in Morphological Closing (Default: 3)**
  * Controls how aggressively the algorithm bridges gaps. If the subject's mouth or eye sockets still look open or incomplete, increase this to `4` or `5`.

## 🚀 Installation & Usage

**Prerequisites:**
Ensure you have Python installed along with the required scientific computing libraries.

```bash
pip install numpy scipy scikit-image trimesh nibabel