# Splenic Dilation Profiles and 3D Voxel Coordinate Engine Specifications

## 1. Overview
This module standardizes the biophysical modeling parameters governing splenic engorgement secondary to portal vein congestion (splenomegaly) and outlines the continuous mapping of spatial coordinate tracking nodes down to 3D voxel grid arrays.

---

## 2. Mathematical Formulations

### A. Vascular Hydrostatic Dilation Profile
The real-time volume expansion of the splenic parenchymal envelope (\(V_{\text{spleen}}\), mL) matches the pressure differential between the splenic venous sinus interior and capsular wall counterpressures:

\[\frac{dV_{\text{spleen}}(t)}{dt} = C_{\text{splenic\_tissue}} \times \max\left(0.0, \, P_{\text{sinus}}(t) - P_{\text{capsular}}\right) - J_{\text{lymphatic\_drainage}}\]

Where sinus backpressure scales non-linearly with incoming portal vein hypertension variables (\(\Delta P_{\text{portal}}\)):

\[P_{\text{sinus}}(t) = P_{\text{portal\_baseline}} + \beta_{\text{congest}} \cdot \Delta P_{\text{portal}}(t) \times \left(\frac{1.0}{\chi}\right)\]

If \(\Delta P_{\text{portal}} > 25\text{ mmHg}\), the matrix logs an automated capsular structural failure condition (`CAPSULAR_RUPTURE_CRISIS`).

---

## 3. Tool Utility Frameworks

### A. YAML Archive Scheduling Wrapper
To modify loose data storage cleaning rules without hardcoding core code, customize the parameter attributes inside `tests/archive_settings.yaml`:

```yaml
archive_policies:
  retention_threshold_days: 7     # Tracks time threshold boundaries
  compression_level: "DEFLATED"   # Standard ZIP compression envelope 
  auto_cleanup_raw_medbin: true   # Releases active disk sectors
```

Execute the configuration engine automatically using the short controller sequence:
```bash
make archive
```

### B. Volumetric 3D Voxel Coordinate Plotting
To track coordinates arrays and render diagnostic voxel density images, call the mapping interface engine within your main predictor suite loop:

```python
from src.voxel_coordinate_interface import OcularVoxelStructuralInterface

# 1. Instantiate the grid matrix mapper object
vox_engine = OcularVoxelStructuralInterface(grid_resolution=32)

# 2. Inject target tracking spatial coordinates node (X, Y, Z normalized)
vox_engine.inject_tracking_coordinate_node(x_normalized=0.512, y_normalized=0.488, z_normalized=0.722)

# 3. Compile and save automated 3D volumetric output image plot
vox_engine.render_voxel_diagnostic_plot(output_img_path="docs/focal_seeding_voxels.png")
```
