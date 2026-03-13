import nibabel as nib
import numpy as np
from skimage import measure
import trimesh
import scipy.ndimage as ndi  # Updated import


def generate_mesh_from_mri(nifti_file_path, output_stl_path, threshold_value):
    print(f"\n--- Starting 3D Generation ---")
    print(f"Loading MRI scan: {nifti_file_path}")

    img = nib.load(nifti_file_path)
    img_data = img.get_fdata()

    # 1. Initial Smoothing
    print("Applying initial smoothing...")
    smoothed_data = ndi.gaussian_filter(img_data, sigma=1.0)

    # 2. Create a True/False mask of the solid tissue
    print(f"Isolating tissue at threshold: {threshold_value}...")
    binary_mask = smoothed_data > threshold_value

    # 3. THE FIX: Morphological Closing (Digital Shrink-Wrap)
    # 'iterations=3' determines how aggressively it bridges gaps.
    # Increase to 4 or 5 if the mouth is still slightly open!
    print("Applying morphological closing to seal mouth and eye cavities...")
    closed_mask = ndi.binary_closing(binary_mask, iterations=3)

    # 4. Re-smooth the mask so the final output isn't blocky like Minecraft
    print("Polishing the final surface...")
    final_data = ndi.gaussian_filter(closed_mask.astype(float), sigma=1.0)

    # 5. Marching Cubes (Threshold is now 0.5 because our data is 0s and 1s)
    verts, faces, normals, values = measure.marching_cubes(
        final_data, level=0.5)

    print(f"Raw mesh generated! {len(verts)} vertices and {len(faces)} faces.")

    # 6. Clean up floating scanner noise
    raw_mesh = trimesh.Trimesh(
        vertices=verts, faces=faces, vertex_normals=normals)
    print("Cleaning up floating artifacts...")
    components = raw_mesh.split(only_watertight=False)
    clean_mesh = max(components, key=lambda m: len(m.faces))

    print(
        f"Cleaned mesh has {len(clean_mesh.faces)} faces. Exporting to STL...")
    clean_mesh.export(output_stl_path)
    print(f"Success! Saved as: {output_stl_path}\n")


if __name__ == "__main__":
    INPUT_MRI = r'C:\Users\haris\projects\MRIto3d\sub-07_T1w.nii.gz'
    OUTPUT_MESH = r'C:\Users\haris\projects\MRIto3d\virtual_twin_brain_sub-07.stl'

    # Keep this around 80-100 based on your last good run
    TISSUE_THRESHOLD = 80

    generate_mesh_from_mri(INPUT_MRI, OUTPUT_MESH, TISSUE_THRESHOLD)
