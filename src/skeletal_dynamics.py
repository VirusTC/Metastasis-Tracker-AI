import math

class DynamicSkeletalEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the Dynamic Osseous Skeleton and Bone Marrow Engine.
        Structural matrices adapt dynamically to baseline anthropometrics.
        """
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.build = body_build.lower()
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration vector factor
        
        # Ingest baseline metrics matching repository protocols
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight_kg ** 0.425)
        self.lbm = 1.10 * self.weight_kg - 128 * ((self.weight_kg / self.height_cm) ** 2)
        
        # Calculate global skeletal parameters
        self.total_skeleton_mass_kg = self._calculate_skeletal_mass()
        self.bone_density_g_cm3 = 1.92

    def _calculate_skeletal_mass(self) -> float:
        if self.build == "ectomorph":
            c_frame = 0.13
        elif self.build == "endomorph":
            c_frame = 0.18
        else:
            c_frame = 0.15 # Mesomorphic baseline norm
        return c_frame * math.pow(self.lbm, 0.95)

    def generate_regional_skeletal_matrix(self, mechanical_strain_load: float) -> dict:
        """
        Partitions global skeletal mass into functional bone matrices, 
        tracking structural density, trabecular voids, and active marrow volumes.
        
        :param mechanical_strain_load: Multiplier representing physical exertion force (1.0 = resting)
        """
        w_skel_g = self.total_skeleton_mass_kg * 1000.0
        
        # Regional distributions: { Identity: (Mass_Fraction, Bone_Count, Has_Red_Marrow) }
        regions = {
            "cranial_facial":      (0.12, 22, False),
            "axial_spine":         (0.20, 26, True),
            "thoracic_cage":       (0.15, 25, True),
            "upper_extremities":   (0.23, 64, False),
            "lower_pelvic_matrix": (0.30, 69, True)
        }

        # Bone Mineral Density (BMD) adjusts dynamically via Wolff's Law approximations
        # Dehydration strains bone matrix turnover pathways
        bmd_baseline = 1.25 * self.chi  # g/cm² reference unit scaling
        bmd_dynamic = bmd_baseline * (1.0 + 0.08 * (mechanical_strain_load - 1.0))

        regional_matrix = {}
        for name, (fraction, count, has_marrow) in regions.items():
            reg_mass = w_skel_g * fraction
            reg_volume_cm3 = reg_mass / self.bone_density_g_cm3
            
            # Active adult red marrow is localized to axial/pelvic trabecular spaces
            if has_marrow:
                # Marrow space volume scales with overall bone volume and hydration thickness
                marrow_vol_cm3 = (reg_volume_cm3 * 0.18) * self.chi
                structural_void_fraction = 0.35
            else:
                marrow_vol_cm3 = 0.0
                structural_void_fraction = 0.08 # Cortical dominance

            # Structural critical failure threshold (Fractal bone load ceiling in Newtons)
            fracture_threshold_N = 4500.0 * bmd_dynamic * (reg_mass / w_skel_g)

            regional_matrix[name] = {
                "bone_count": count,
                "total_regional_mass_g": round(reg_mass, 1),
                "total_regional_volume_cm3": round(reg_volume_cm3, 1),
                "structural_porosity_fraction": structural_void_fraction,
                "active_red_marrow_volume_cm3": round(marrow_vol_cm3, 2),
                "local_bone_mineral_density_g_cm2": round(bmd_dynamic, 3),
                "calculated_fracture_threshold_newtons": round(fracture_threshold_N, 1)
            }

        return regional_matrix

    def calculate_bone_marrow_sinusoidal_flux(self, regional_matrix: dict, local_perfusion_pressure_mmHg: float) -> dict:
        """
        Models the cell-shedding and mass transport kinetics out of the trabecular bone 
        marrow niches directly into neighboring vascular generation loops.
        """
        # Baseline shedding coefficient (cells exiting per cm³ of marrow per mmHg per second)
        k_sinusoidal = 4.2e2
        p_local = max(5.0, min(120.0, local_perfusion_pressure_mmHg))
        
        total_marrow_volume = sum(r["active_red_marrow_volume_cm3"] for r in regional_matrix.values())
        
        # Cellular efflux rate equation: J = K * V * P
        cell_efflux_rate_sec = k_sinusoidal * total_marrow_volume * p_local
        
        # Scale up microvascular blood flow resistance inside bone canals if dehydration is active
        intraosseous_vascular_resistance_multiplier = 1.0 + 0.4 * (1.0 - self.chi)

        return {
            "total_systemic_red_marrow_volume_cm3": round(total_marrow_volume, 2),
            "sinusoidal_perfusion_pressure_mmHg": p_local,
            "sinusoidal_cell_shedding_rate_seconds": int(cell_efflux_rate_sec),
            "intraosseous_vascular_resistance_multiplier": round(intraosseous_vascular_resistance_multiplier, 2),
            "hematopoietic_niche_status": "HIGH TURNOVER" if p_local > 40.0 else "BASAL RETENTION STATE"
        }

# =====================================================================
# Operational Verification Matrix
# =====================================================================
if __name__ == "__main__":
    # Simulate an athletic patient under high physical strain (Strain load = 1.5, e.g. sprinting/lifting)
    engine = DynamicSkeletalEngine(height_cm=180.0, weight_kg=78.0, body_build="mesomorph", hydration_level=1.0)
    
    print("=========================================================================")
    print("DYNAMIC OSSEOUS SKELETON AND HEMATOPOIETIC MARROW LOGS")
    print("=========================================================================\n")
    
    # 1. Generate the dynamic structural bone matrix profile
    skeletal_matrix = engine.generate_regional_skeletal_matrix(mechanical_strain_load=1.5)
    print(f"--- 1. STRUCTURAL FRAMEWORK PARTITIONING ( Wolff's Law Strain: 1.5 ) ---")
    print(f" Calculated Dry Skeletal Mass: {engine.total_skeleton_mass_kg:.2f} kg")
    
    spine = skeletal_matrix["axial_spine"]
    pelvis = skeletal_matrix["lower_pelvic_matrix"]
    upper_limb = skeletal_matrix["upper_extremities"]
    
    print(f"  -> Spine Node Matrix  | Mass: {spine['total_regional_mass_g']}g | Local BMD: {spine['local_bone_mineral_density_g_cm2']} g/cm²")
    print(f"  -> Pelvis Node Matrix | Mass: {pelvis['total_regional_mass_g']}g | Red Marrow Pool: {pelvis['active_red_marrow_volume_cm3']} cm³")
    print(f"  -> Upper Extremities  | Mass: {upper_limb['total_regional_mass_g']}g | Fracture Ceiling: {upper_limb['calculated_fracture_threshold_newtons']} N\n")

    # 2. Compute live sinusoidal cell-shedding kinetics into circulation loops
    # Simulate a local nutrient artery perfusion pressure of 45 mmHg
    marrow_kinetics = engine.calculate_bone_marrow_sinusoidal_flux(skeletal_matrix, local_perfusion_pressure_mmHg=45.0)
    print("--- 2. BONE MARROW SINUSOIDAL EMISSION KINETICS ---")
    print(f" Systemic Adult Red Marrow Capacity: {marrow_kinetics['total_systemic_red_marrow_volume_cm3']} cm³")
    print(f" Local Perfusion Delivery Pressure:  {marrow_kinetics['sinusoidal_perfusion_pressure_mmHg']} mmHg")
    print(f" Sinusoidal Cell Influx Into Flow:   {marrow_kinetics['sinusoidal_cell_shedding_rate_seconds']:,} cells/second")
    print(f" Intraosseous Resistance Multiplier: {marrow_kinetics['intraosseous_vascular_resistance_multiplier']}x base")
    print(f" Hematopoietic Structural Status:     {marrow_kinetics['hematopoietic_niche_status']}")
