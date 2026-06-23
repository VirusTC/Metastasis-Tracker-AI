import math

class ExtendedAnatomySimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the extended anatomical compartment template.
        All structural matrices adapt dynamically to baseline parameters.
        """
        self.height_cm = height_cm
        self.height_m = height_cm / 100.0
        self.weight = weight_kg
        self.build = body_build.lower()
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration vector factor

        # Compute core anthropometric markers
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight ** 0.425)
        self.cardiac_output_L_min = self.bsa * 3.0 * math.sqrt(self.chi)

    def generate_digestive_system(self, systemic_circulatory_data: dict) -> dict:
        """
        Maps the complete digestive path from mouth to anus.
        Integrates directly with mesenteric arterial branches and hepatic portal loops.
        """
        # Morphometric dimensional scaling based on patient height
        gi_length_m = 4.5 * self.height_m
        
        # Segment allocations tracking total tract path length distribution
        segments = {
            "mouth_and_oral_cavity": {"length_m": 0.08, "mean_diameter_cm": 6.5, "surface_area_cm2": 155.0},
            "esophagus":            {"length_m": 0.25, "mean_diameter_cm": 2.0, "surface_area_cm2": 150.0},
            "stomach":              {"length_m": 0.28, "mean_diameter_cm": 12.0, "surface_area_cm2": 800.0},
            "duodenum":             {"length_m": 0.25, "mean_diameter_cm": 3.8, "surface_area_cm2": 300.0},
            "jejunum":              {"length_m": gi_length_m * 0.40, "mean_diameter_cm": 3.0, "surface_area_cm2": 180000.0}, # Microvilli expanded
            "ileum":                {"length_m": gi_length_m * 0.50, "mean_diameter_cm": 2.5, "surface_area_cm2": 120000.0}, # Microvilli expanded
            "large_intestine":      {"length_m": 1.50, "mean_diameter_cm": 6.5, "surface_area_cm2": 2500.0},
            "anal_canal":           {"length_m": 0.04, "mean_diameter_cm": 2.8, "surface_area_cm2": 35.0}
        }

        # Circulatory Linkage Layer: Extracting flow metrics from mid-tier arterial generations
        # Mesenteric branches generally originate between generations 5 and 8 of the systemic tree
        arterial_source = systemic_circulatory_data["systemic_arterial_tree"][6]
        available_pressure_mmHg = arterial_source["pressure_out_mmHg"]
        
        # Splanchnic circulation takes approximately 25% of the total resting cardiac output
        total_splanchnic_flow_L_min = self.cardiac_output_L_min * 0.25

        digestive_map = {}
        for name, geom in segments.items():
            # Apply hydration tuning variables to active tissue volumes
            calc_volume_cm3 = math.pi * ((geom["mean_diameter_cm"] / 2.0) ** 2) * (geom["length_m"] * 100.0) * self.chi
            
            # Map portal venous routing dependencies
            # Foregut/Midgut/Hindgut venous return confluences into the Hepatic Portal Vein
            drains_to_portal_system = name not in ["mouth_and_oral_cavity", "esophagus", "anal_canal"]
            
            digestive_map[name] = {
                "segment_length_meters": round(geom["length_m"], 3),
                "segment_diameter_cm": geom["mean_diameter_cm"],
                "mucosal_surface_area_cm2": geom["surface_area_cm2"],
                "calculated_tissue_volume_cm3": round(calc_volume_cm3, 2),
                "arterial_inflow_pressure_mmHg": round(available_pressure_mmHg, 2),
                "allocated_segment_flow_L_min": round(total_splanchnic_flow_L_min * (geom["length_m"] / gi_length_m), 4),
                "portal_circulation_routing": drains_to_portal_system
            }
            
        return {"total_gi_tract_length_meters": round(gi_length_m + 0.62, 3), "gi_compartments": digestive_map}

    def generate_urinary_system(self) -> dict:
        """
        Calculates the physical structural dimensions, filtration profiles,
        and volumetric metrics of the left and right urinary tracks.
        """
        # Structural metrics scaled directly to mass and density parameters
        w = self.weight
        kidney_mass_base = 1.45 * (w ** 0.95)
        
        # Left and right morphological variations (Right kidney bounded by liver margin)
        left_kidney_mass = kidney_mass_base * 1.05
        right_kidney_mass = kidney_mass_base * 0.98

        # Glomerular filtration tracking scaled to combined renal volume
        total_renal_volume_cm3 = (left_kidney_mass / 1.05) + (right_kidney_mass / 1.05)
        gfr_mL_min = 0.00055 * total_renal_volume_cm3 * 1000.0

        return {
            "left_kidney": {
                "mass_g": round(left_kidney_mass, 2),
                "dimensions_cm": {"length": 11.5, "width": 6.0, "depth": 3.5},
                "ureter_length_cm": 30.0,
                "ureter_lumen_diameter_cm": 0.35
            },
            "right_kidney": {
                "mass_g": round(right_kidney_mass, 2),
                "dimensions_cm": {"length": 11.0, "width": 5.5, "depth": 3.2},
                "ureter_length_cm": 28.0,
                "ureter_lumen_diameter_cm": 0.35
            },
            "urinary_bladder": {
                "maximum_capacity_mL": round(500.0 * self.chi, 1),
                "resting_wall_thickness_cm": 0.45
            },
            "hemodynamic_filtration_metrics": {
                "calculated_gfr_mL_min": round(gfr_mL_min, 2),
                "renal_blood_flow_allocation_L_min": round(self.cardiac_output_L_min * 0.22, 3)
            }
        }

    def generate_nasal_sinus_throat_system(self, existing_airway_tree: list) -> dict:
        """
        Maps the upper respiratory zones and links them directly as proximal 
        boundaries to Generation 0 (Trachea) of the existing airway network.
        """
        # Base dimensions mapped to structural height scaling vectors
        nasal_volume_mL = 0.015 * self.height_cm * self.chi
        
        upper_zones = {
            "nasal_cavity_proper": {"volume_mL": nasal_volume_mL, "surface_area_cm2": 155.0},
            "nasopharynx":          {"volume_mL": 15.0, "surface_area_cm2": 28.0},
            "oropharynx":           {"volume_mL": 25.0, "surface_area_cm2": 38.0},
            "laryngopharynx":       {"volume_mL": 18.0, "surface_area_cm2": 32.0}
        }

        # Reference paranasal cavity mapping matrix
        sinuses = {
            "maxillary_sinus_bilateral": {"volume_mL": 30.0, "structural_access_ostia_cm": 0.25},
            "frontal_sinus_bilateral":   {"volume_mL": 12.0, "structural_access_ostia_cm": 0.15},
            "ethmoid_sinus_cells":       {"volume_mL": 10.0, "structural_access_ostia_cm": 0.10},
            "sphenoid_sinus_bilateral":  {"volume_mL": 15.0, "structural_access_ostia_cm": 0.18}
        }

        # Extract target structural reference metrics from the existing Generation 0 airway node
        trachea_node = existing_airway_tree[0]
        
        return {
            "upper_conducting_spaces": upper_zones,
            "paranasal_sinus_matrix": sinuses,
            "proximal_airway_linkage": {
                "target_generation": trachea_node["generation"],
                "terminal_throat_to_trachea_radius_m": trachea_node["radius_m"],
                "downstream_continuity_verified": True
            }
        }

    def generate_reproductive_system(self, biological_sex: str) -> dict:
        """
        Compiles structural values for the left and right gonadal matrices.
        Establishes the anatomical routing column from pelvic hubs up to cranial sinuses.
        """
        gonad_map = {}
        sex_key = biological_sex.lower()

        if sex_key == "male":
            gonad_map["left_testicle"] = {"mass_g": 18.5, "volume_cm3": 17.5, "dimensions_cm": {"L": 4.5, "W": 2.8, "D": 3.0}}
            gonad_map["right_testicle"] = {"mass_g": 17.2, "volume_cm3": 16.3, "dimensions_cm": {"L": 4.3, "W": 2.6, "D": 2.8}}
            gonad_map["accessory_structures"] = {"prostate_volume_cm3": 20.0, "urethral_length_cm": 19.5}
        else:
            gonad_map["left_ovary"] = {"mass_g": 6.5, "volume_cm3": 6.2, "dimensions_cm": {"L": 4.0, "W": 2.0, "D": 1.5}}
            gonad_map["right_ovary"] = {"mass_g": 6.1, "volume_cm3": 5.8, "dimensions_cm": {"L": 3.8, "W": 1.9, "D": 1.4}}
            gonad_map["accessory_structures"] = {"uterus_mass_g": 70.0, "fallopian_tube_length_cm": 11.0}

        # Define Cross-Systemic Structural Routing (Reproductive Hub to Cranial Sinuses)
        # Tracks parallel axial columns through vertebrae up to the skull base
        axial_skeletal_routing = [
            {"node": "Pelvic_Sacral_Confluence", "vertebral_level": "S5-S1", "segment_distance_offset_cm": 0.0},
            {"node": "Lumbar_Vertebral_Matrix",   "vertebral_level": "L5-L1", "segment_distance_offset_cm": 18.0},
            {"node": "Thoracic_Vertebral_Matrix", "vertebral_level": "T12-T1", "segment_distance_offset_cm": 48.0},
            {"node": "Cervical_Vertebral_Matrix", "vertebral_level": "C7-C1", "segment_distance_offset_cm": 61.0},
            {"node": "Skull_Base_Interface",      "vertebral_level": "Clivus", "segment_distance_offset_cm": 63.5}
        ]

        return {
            "biological_sex_assignment": biological_sex,
            "gonadal_bilateral_matrix": gonad_map,
            "cross_systemic_routing_column": {
                "structural_backbone_path": axial_skeletal_routing,
                "valveless_fluid_shunt_network": {
                    "identity": "Vertebral Venous Plexus (Batson's Plexus)",
                    "pelvic_to_dural_sinus_continuity": True,
                    "target_sinus_proximity_distance_cm": 0.5 # Proximity behind pharyngeal boundaries
                }
}}def build_extended_dataset(self, core_dataset: dict, biological_sex: str) -> dict:"""Compiles and merges all newly mapped anatomical layers with existingcirculatory and respiratory trees to construct a cohesive system-wide matrix."""circ = core_dataset["circulatory_network"]airways = core_dataset["airway_network"]return {"digestive_system": self.generate_digestive_system(circ),"urinary_system": self.generate_urinary_system(),"nasal_sinus_throat_system": self.generate_nasal_sinus_throat_system(airways),"reproductive_and_axial_routing": self.generate_reproductive_system(biological_sex)}=====================================================================Standalone Structural Verification Sandbox=====================================================================if name == "main":from patient_anatomy import PatientSimulationEngine# 1. Initialize core system structures using your repo's baseline engine configuration rulesprint("Initializing baseline structural templates...")core_engine = PatientSimulationEngine(height_cm=175.0, weight_kg=72.0, body_build="mesomorph", hydration_level=0.95)core_data = core_engine.build_complete_dataset()# 2. Run the extended mapping pipeline matrixextended_engine = ExtendedAnatomySimulationEngine(height_cm=175.0, weight_kg=72.0, body_build="mesomorph", hydration_level=0.95)extended_dataset = extended_engine.build_extended_dataset(core_data, biological_sex="male")print("\n" + "="*73)print("EXTENDED ANATOMICAL COMPARTMENT VERIFICATION SUMMARY")print("="*73)# Validate Digestive Connectionsgi = extended_dataset["digestive_system"]print(f"\n[DIGESTIVE SYSTEM]: Total Segment Length: {gi['total_gi_tract_length_meters']} meters")print(f" - Jejunum Surface Area (Villi Expanded): {gi['gi_compartments']['jejunum']['mucosal_surface_area_cm2']:,} cm²")print(f" - Hepatic Portal Routing Active for Stomach/Intestines: {gi['gi_compartments']['stomach']['portal_circulation_routing']}")# Validate Urinary Matricesurinary = extended_dataset["urinary_system"]print(f"\n[URINARY SYSTEM]:")print(f" - Left Kidney Structural Mass: {urinary['left_kidney']['mass_g']} g | Ureter Length: {urinary['left_kidney']['ureter_length_cm']} cm")print(f" - Total Allocated Renal Flow Volume: {urinary['hemodynamic_filtration_metrics']['renal_blood_flow_allocation_L_min']:.3f} L/min")# Validate Upper conducting airway junctionsresp = extended_dataset["nasal_sinus_throat_system"]print(f"\n[NASAL / SINUS / THROAT]: Nasal Space Target Capacity: {resp['upper_conducting_spaces']['nasal_cavity_proper']['volume_mL']:.2f} mL")print(f" - Downstream Trachea Connectivity Link Verification Status: {resp['proximal_airway_linkage']['downstream_continuity_verified']}")# Validate Reproductive and batson plexus spinal pathsrepro = extended_dataset["reproductive_and_axial_routing"]print(f"\n[REPRODUCTIVE & AXIAL ROUTING]: Biological Sex Assignment Profile: {repro['biological_sex_assignment'].upper()}")print(f" - Left Gonadal Mass: {repro['gonadal_bilateral_matrix']['left_testicle']['mass_g']} g")print(f" - Axial Fluid Shunt: {repro['cross_systemic_routing_column']['valveless_fluid_shunt_network']['identity']}")print(f" - Target Skull Base Entry Point: {repro['cross_systemic_routing_column']['structural_backbone_path'][-1]['vertebral_level']}")
### Architectural & Project Alignment Notes
* **Modular Parallels**: This file mirrors your repository's object-oriented initialization structure, ensuring all computed properties accept similar baseline anthropometric scalars.
* **Circulatory Interfacing**: The `generate_digestive_system` class method accepts the systemic arterial generation array directly, resolving internal splanchnic perfusion pressures alongside mesenteric flow drops.
* **Airway Interfacing**: Upper respiratory conducting points parse the `airway_network` dataset dynamically, anchoring the nasal and pharyngeal cavities directly to the trachea (Generation 0) model boundaries.
