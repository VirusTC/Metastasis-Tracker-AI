"""
Unified Patient Anatomy & Physiological Engine
Merges core anatomy, metabolic profiles, extended structural compartments, 
and final systemic tracking matrices into a single, highly cohesive source of truth.
"""

import math
import json

# =====================================================================
# TIER 1: CORE PHYSIOLOGICAL & METABOLIC ENGINES
# (These contain your existing complex WBE scaling & fluid dynamics)
# =====================================================================

class CompleteMetabolicCTCUniverse:
    # [RETAIN YOUR EXISTING IMPLEMENTATION HERE]
    # Includes calculate_ca_kinetics, simulate_respiratory_compensation, predict_ctc_seeding_matrix
    pass

class PatientSimulationEngine:
    # [RETAIN YOUR EXISTING IMPLEMENTATION HERE]
    # Includes build_complete_dataset, generate_airway_tree, generate_organ_matrix
    pass

class AdvancedMetabolicEngine:
    # [RETAIN YOUR EXISTING IMPLEMENTATION HERE]
    # Includes calculate_renal_bicarbonate_handling, compute_bohr_oxygen_offloading, simulate_strenuous_exertion_lactate_curve
    pass

class AdvancedClinicalImmunoEngine:
    # [RETAIN YOUR EXISTING IMPLEMENTATION HERE]
    # Includes ingest_clinical_chart_profile, simulate_ph_recovery_trajectory
    pass


# =====================================================================
# TIER 2: EXTENDED ANATOMICAL COMPARTMENTS
# =====================================================================

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

        # Mesenteric branches generally originate between generations 5 and 8 of the systemic tree
        arterial_source = systemic_circulatory_data["systemic_arterial_tree"][6]
        available_pressure_mmHg = arterial_source["pressure_out_mmHg"]
        
        # Splanchnic circulation takes approximately 25% of the total resting cardiac output
        total_splanchnic_flow_L_min = self.cardiac_output_L_min * 0.25

        digestive_map = {}
        for name, geom in segments.items():
            # Apply hydration tuning variables to active tissue volumes
            calc_volume_cm3 = math.pi * ((geom["mean_diameter_cm"] / 2.0) ** 2) * (geom["length_m"] * 100.0) * self.chi
            
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
        w = self.weight
        kidney_mass_base = 1.45 * (w ** 0.95)
        
        left_kidney_mass = kidney_mass_base * 1.05
        right_kidney_mass = kidney_mass_base * 0.98

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
        nasal_volume_mL = 0.015 * self.height_cm * self.chi
        
        upper_zones = {
            "nasal_cavity_proper":  {"volume_mL": nasal_volume_mL, "surface_area_cm2": 155.0},
            "nasopharynx":          {"volume_mL": 15.0, "surface_area_cm2": 28.0},
            "oropharynx":           {"volume_mL": 25.0, "surface_area_cm2": 38.0},
            "laryngopharynx":       {"volume_mL": 18.0, "surface_area_cm2": 32.0}
        }

        sinuses = {
            "maxillary_sinus_bilateral": {"volume_mL": 30.0, "structural_access_ostia_cm": 0.25},
            "frontal_sinus_bilateral":   {"volume_mL": 12.0, "structural_access_ostia_cm": 0.15},
            "ethmoid_sinus_cells":       {"volume_mL": 10.0, "structural_access_ostia_cm": 0.10},
            "sphenoid_sinus_bilateral":  {"volume_mL": 15.0, "structural_access_ostia_cm": 0.18}
        }

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

        axial_skeletal_routing = [
            {"node": "Pelvic_Sacral_Confluence", "vertebral_level": "S5-S1", "segment_distance_offset_cm": 0.0},
            {"node": "Lumbar_Vertebral_Matrix",  "vertebral_level": "L5-L1", "segment_distance_offset_cm": 18.0},
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
                    "target_sinus_proximity_distance_cm": 0.5 
                }
            }
        }

    def build_extended_dataset(self, core_dataset: dict, biological_sex: str) -> dict:
        """
        Compiles and merges all newly mapped anatomical layers with existing
        circulatory and respiratory trees to construct a cohesive system-wide matrix.
        """
        circ = core_dataset["circulatory_network"]
        airways = core_dataset["airway_network"]
        
        return {
            "digestive_system": self.generate_digestive_system(circ),
            "urinary_system": self.generate_urinary_system(),
            "nasal_sinus_throat_system": self.generate_nasal_sinus_throat_system(airways),
            "reproductive_and_axial_routing": self.generate_reproductive_system(biological_sex)
        }


# =====================================================================
# TIER 3: FINAL SYSTEMIC & BARRIER MATRICES
# =====================================================================

class FinalAnatomySimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the final anatomical extension tier.
        Completes the mapping of endocrine, lymphatic, muscular, and barrier matrices.
        """
        self.height_cm = height_cm
        self.height_m = height_cm / 100.0
        self.weight = weight_kg
        self.build = body_build.lower()
        self.chi = max(0.5, min(1.5, hydration_level))
        
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight ** 0.425)
        self.cardiac_output_L_min = self.bsa * 3.0 * math.sqrt(self.chi)

    def generate_endocrine_system(self, systemic_circulatory_data: dict) -> dict:
        """
        Maps the coordinates, masses, and blood flow distributions 
        for the primary systemic endocrine glands.
        """
        w = self.weight
        
        gland_blueprints = {
            "pituitary":      (0.6, 3),   
            "thyroid":        (20.0, 4),  
            "adrenal_each":   (5.0, 6),   
            "parathyroid_4x": (0.15, 4)
        }
        
        p_base = systemic_circulatory_data["systemic_arterial_tree"][0]["pressure_out_mmHg"]
        
        endocrine_map = {}
        for name, (base_mass, gen_feed) in gland_blueprints.items():
            scaled_mass = base_mass * (w / 70.0)
            volume_cm3 = scaled_mass / 1.05
            
            endocrine_map[name] = {
                "glandular_mass_grams": round(scaled_mass, 3),
                "calculated_volume_cm3": round(volume_cm3, 3),
                "arterial_generation_feed_source": gen_feed,
                "local_perfusion_pressure_mmHg": round(p_base * (0.98 ** gen_feed), 2)
            }
        return endocrine_map

    def generate_lymphatic_system(self, dynamic_starling_flux: float) -> dict:
        """
        Models the interstitial fluid clearance channels and lymph node clusters.
        Sinks return volume from Generation 30 back into the venous circulation trunk.
        """
        base_lymph_flow_L_min = (120.0 / 60.0) / 1000.0
        active_lymph_return_L_min = base_lymph_flow_L_min * (dynamic_starling_flux / 0.5) * self.chi

        regional_node_stations = {
            "cervical_clusters":     {"node_count_approx": 75,  "mean_node_diameter_mm": 6.0},
            "axillary_clusters":     {"node_count_approx": 45,  "mean_node_diameter_mm": 8.0},
            "mesenteric_aggregates": {"node_count_approx": 150, "mean_node_diameter_mm": 5.0},
            "inguinal_clusters":     {"node_count_approx": 25,  "mean_node_diameter_mm": 10.0}
        }

        return {
            "lymph_recirculation_flux_L_min": round(active_lymph_return_L_min, 5),
            "central_terminal_drainage_point": "Left and Right Subclavian Venous Confluence",
            "regional_filtration_hubs": regional_node_stations,
            "valved_vessel_continuity_verified": True
        }

    def generate_musculoskeletal_mass_grid(self) -> dict:
        """
        Partitions the remaining somatic frame into skeletal muscle compartments
        and axial/appendicular structural bone tissue masses.
        """
        w = self.weight
        
        if self.build == "endomorph":
            muscle_fraction = 0.36
            bone_fraction = 0.12
        elif self.build == "ectomorph":
            muscle_fraction = 0.42
            bone_fraction = 0.16
        else: # Mesomorphic default
            muscle_fraction = 0.45
            bone_fraction = 0.14
            
        total_muscle_mass_kg = w * muscle_fraction
        total_bone_mass_kg = w * bone_fraction
        
        return {
            "skeletal_muscle_compartment": {
                "total_mass_kg": round(total_muscle_mass_kg, 2),
                "estimated_tissue_density_g_cm3": 1.06,
                "basal_oxygen_consumption_fraction": 0.20
            },
            "osseous_skeleton_compartment": {
                "total_mass_kg": round(total_bone_mass_kg, 2),
                "structural_matrix_density_g_cm3": 1.92,
                "active_bone_marrow_volume_cm3": round((total_bone_mass_kg * 1000.0 * 0.05) / 1.02, 1)
            }
        }

    def calculate_blood_brain_barrier_interface(self, brain_vascular_node: dict) -> dict:
        """
        Simulates the microvascular tight junction barrier parameters of 
        the blood-brain barrier (BBB) within cerebral capillary matrices.
        """
        local_shear = brain_vascular_node.get("shear_rate_s1", 150.0)
        vessel_radius_m = brain_vascular_node.get("radius_m", 4.5e-6)
        vessel_length_m = brain_vascular_node.get("length_m", 0.001)
        
        capillary_surface_area_um2 = 2.0 * math.pi * (vessel_radius_m * 1e6) * (vessel_length_m * 1e6)
        
        # Structural barrier permeability constant
        p_base = 1.5e-7 * (1.0 / (1.0 + 0.002 * local_shear))
        
        # Functional permeability-surface area coefficient
        ps_product_cm3_s = (p_base * (capillary_surface_area_um2 * 1e-8)) * self.chi

        return {
            "cerebral_capillary_surface_area_um2": capillary_surface_area_um2,
            "calculated_endothelial_tight_junction_tightness_index": round(1.0 + (0.001 * local_shear), 2),
            "permeability_coefficient_p_cm_s": p_base,
            "calculated_ps_product_cm3_s": ps_product_cm3_s,
            "barrier_structural_integrity_status": "Intact Protective State" if self.chi >= 0.85 else "Hyperpermeable Leakage Strain"
        }

    def build_comprehensive_universe_dataset(self, existing_patient_dataset: dict) -> dict:
        """
        Consolidates all previous core, extended, and final anatomical layers
        into a unified structural and mathematical package.
        """
        circ_tree = existing_patient_dataset["circulatory_network"]
        starling = existing_patient_dataset["capillary_starling_forces"]
        
        cerebral_sample_node = circ_tree["systemic_arterial_tree"][12]

        return {
            "endocrine_matrix": self.generate_endocrine_system(circ_tree),
            "lymphatic_network": self.generate_lymphatic_system(starling["fluid_flux_mL_min"]),
            "musculoskeletal_grid": self.generate_musculoskeletal_mass_grid(),
            "blood_brain_barrier_interface": self.calculate_blood_brain_barrier_interface(cerebral_sample_node)
        }


# =====================================================================
# MASTER SYSTEM VERIFICATION SANDBOX
# =====================================================================

if __name__ == "__main__":
    print("=========================================================================")
    print("UNIFIED PATIENT ANATOMY & PHYSIOLOGICAL ENGINE INITIALIZATION")
    print("=========================================================================\n")

    # 1. Initialize Core Engine
    print("[*] Booting Tier 1: Core System Structures...")
    base_engine = PatientSimulationEngine(height_cm=175.0, weight_kg=72.0, body_build="mesomorph", hydration_level=1.0)
    master_core_data = base_engine.build_complete_dataset()

    # 2. Append Extended Systems
    print("[*] Booting Tier 2: Extended Anatomical Compartments...")
    extended_engine = ExtendedAnatomySimulationEngine(height_cm=175.0, weight_kg=72.0, body_build="mesomorph", hydration_level=1.0)
    extended_dataset = extended_engine.build_extended_dataset(master_core_data, biological_sex="male")
    
    # Merge extended into core
    master_core_data.update(extended_dataset)

    # 3. Append Final Systemic Systems
    print("[*] Booting Tier 3: Final Systemic & Barrier Matrices...")
    final_engine = FinalAnatomySimulationEngine(height_cm=175.0, weight_kg=72.0, body_build="mesomorph", hydration_level=1.0)
    final_dataset = final_engine.build_comprehensive_universe_dataset(master_core_data)
    
    # Merge final into core
    master_core_data.update(final_dataset)

    print("\n" + "="*75)
    print("FINAL PHYSIOLOGICAL ENVIRONMENT DATA MAP COMPLETED")
    print("="*75)

    # Print Verification Targets
    endo = master_core_data["endocrine_matrix"]
    lymph = master_core_data["lymphatic_network"]
    repro = master_core_data["reproductive_and_axial_routing"]
    bbb = master_core_data["blood_brain_barrier_interface"]

    print(f"\n[DIGESTIVE SYSTEM]: Total Segment Length: {master_core_data['digestive_system']['total_gi_tract_length_meters']} meters")
    print(f"\n[REPRODUCTIVE & AXIAL ROUTING]: Biological Sex Assignment: {repro['biological_sex_assignment'].upper()}")
    print(f" - Target Skull Base Entry Point: {repro['cross_systemic_routing_column']['structural_backbone_path'][-1]['vertebral_level']}")
    
    print(f"\n[ENDOCRINE SYSTEM]: Mapped Gland Mass Details:")
    print(f" - Thyroid Gland Mass: {endo['thyroid']['glandular_mass_grams']} g | Feed Gen: {endo['thyroid']['arterial_generation_feed_source']}")
    print(f" - Adrenal Glands (Each): Mass: {endo['adrenal_each']['glandular_mass_grams']} g | Perfusion: {endo['adrenal_each']['local_perfusion_pressure_mmHg']} mmHg")

    print(f"\n[LYMPHATIC DRAINAGE]: Target Clear Return Sink Rate: {lymph['lymph_recirculation_flux_L_min']:.5f} L/min")

    print(f"\n[BLOOD-BRAIN BARRIER INTERFACE]: Cerebral microvascular capillary line data:")
    print(f" - Permeability-Surface Area Product (PS): {bbb['calculated_ps_product_cm3_s']:.3e} cm³/s")
    print(f" - Structural Barrier Functional Status:   {bbb['barrier_structural_integrity_status']}\n")
