import math

class SystemicChemicalCompositionEngine:
    def __init__(self, global_hydration_level: float):
        """
        :param global_hydration_level: Multiplier factor (\u03c7) from core engine (e.g. 1.0 = normal, 0.85 = dehydrated)
        """
        self.chi = max(0.5, min(1.5, global_hydration_level)) # Clamped security ceiling

        # Biochemical profiles for major organs: { name: (Water, Lipid, Protein, Carbs, Ash/Mineral fractions) }
        # Baselines derived from ICRP Reference Human compositional metrics
        self.organ_biochem_blueprints = {
            "heart":       {"water": 0.79, "lipid": 0.04, "protein": 0.16, "carbs": 0.005, "ash": 0.005},
            "liver":       {"water": 0.72, "lipid": 0.05, "protein": 0.19, "carbs": 0.025, "ash": 0.015},
            "kidney_each": {"water": 0.81, "lipid": 0.05, "protein": 0.12, "carbs": 0.010, "ash": 0.010},
            "spleen":      {"water": 0.78, "lipid": 0.02, "protein": 0.18, "carbs": 0.010, "ash": 0.010},
            "pancreas":    {"water": 0.73, "lipid": 0.11, "protein": 0.14, "carbs": 0.010, "ash": 0.010},
            "brain":       {"water": 0.77, "lipid": 0.12, "protein": 0.09, "carbs": 0.010, "ash": 0.010}
        }

        # Stoichiometric approximations mapping biochemical groupings to elemental mass fractions
        # e.g., Protein is highly nitrogenous; Lipids are heavily carbonaceous
        self.biochem_to_element_matrix = {
            "water":   {"O": 0.888, "H": 0.112, "C": 0.0,   "N": 0.0,   "Ca_P_Ash": 0.0},
            "lipid":   {"O": 0.120, "H": 0.120, "C": 0.760, "N": 0.0,   "Ca_P_Ash": 0.0},
            "protein": {"O": 0.220, "H": 0.070, "C": 0.530, "N": 0.160, "Ca_P_Ash": 0.0},
            "carbs":   {"O": 0.490, "H": 0.060, "C": 0.450, "N": 0.0,   "Ca_P_Ash": 0.0},
            "ash":     {"O": 0.400, "H": 0.0,   "C": 0.0,   "N": 0.0,   "Ca_P_Ash": 0.60}
        }

    def compute_organ_chemical_composition(self, organ_name: str, calculated_mass_g: float) -> dict:
        """
        Calculates biochemical mass allocations and elemental weight breakdowns for a target organ mass,
        dynamically adjusting for the patient's current hydration status.
        """
        name_key = organ_name.lower()
        if name_key not in self.organ_biochem_blueprints:
            # Safe generic soft tissue fallback if an unmapped organ string enters the engine
            blueprint = {"water": 0.75, "lipid": 0.06, "protein": 0.17, "carbs": 0.01, "ash": 0.01}
        else:
            blueprint = self.organ_biochem_blueprints[name_key].copy()

        # Step 1: Adjust water fraction based on dynamic hydration metrics
        raw_water = blueprint["water"] * self.chi
        
        # Renormalize non-aqueous fractions so total mass distribution equals exactly 1.0
        remaining_fraction = 1.0 - raw_water
        base_non_water_sum = sum(v for k, v in blueprint.items() if k != "water")
        
        biochem_fractions = {"water": raw_water}
        for k, v in blueprint.items():
            if k != "water":
                biochem_fractions[k] = (v / base_non_water_sum) * remaining_fraction

        # Step 2: Compute explicit mass profiles for biochemical components (grams)
        biochem_mass_g = {k: v * calculated_mass_g for k, v in biochem_fractions.items()}

        # Step 3: Map biochemical masses to core elemental components via stoichiometric ratios
        elemental_mass_g = {"O": 0.0, "H": 0.0, "C": 0.0, "N": 0.0, "Ca_P_Ash": 0.0}
        
        for pool_key, pool_mass in biochem_mass_g.items():
            ratios = self.biochem_to_element_matrix[pool_key]
            for element_key in elemental_mass_g.keys():
                elemental_mass_g[element_key] += pool_mass * ratios[element_key]

        # Step 4: Derive clinical ionic concentrations (mmol/L of tissue water)
        # Scaled dynamically based on hemoconcentration/hemodilution states
        tissue_water_v_liters = biochem_mass_g["water"] / 1000.0
        
        # Baselines scaled inversely to tissue water concentration shifts
        na_conc_mmol_L = 140.0 * (1.0 / self.chi) if tissue_water_v_liters > 0 else 0
        k_conc_mmol_L  = 120.0 * (1.0 / self.chi) if tissue_water_v_liters > 0 else 0 # Intracellular dominance
        cl_conc_mmol_L = 102.0 * (1.0 / self.chi) if tissue_water_v_liters > 0 else 0

        return {
            "organ_identity": organ_name,
            "total_mass_g": calculated_mass_g,
            "biochemical_mass_breakdown_g": {k: round(v, 2) for k, v in biochem_mass_g.items()},
            "biochemical_mass_percentages": {k: round(v * 100.0, 2) for k, v in biochem_fractions.items()},
            "elemental_mass_breakdown_g": {k: round(v, 2) for k, v in elemental_mass_g.items()},
            "ionic_interstitial_profile_mmol_L": {
                "Na+": round(na_conc_mmol_L, 1),
                "K+": round(k_conc_mmol_L, 1),
                "Cl-": round(cl_conc_mmol_L, 1)
            }
        }

    def compute_circulatory_fluid_composition(self, vessel_generation: int, pool_volume_mL: float) -> dict:
        """
        Resolves the fluid chemical configuration of circulating blood volumes inside specific tree structures.
        """
        # Approximated blood density: 1.06 g/mL
        total_fluid_mass_g = pool_volume_mL * 1.06
        
        # Blood plasma hydration scaling tracking profile
        water_fraction = 0.81 * self.chi
        protein_fraction = 0.12 * (1.0 / self.chi) # Hemoconcentration inverse scaling
        lipid_fraction = 0.06
        carbs_fraction = 0.005
        ash_fraction = 0.005
        
        # Normalize boundaries safely
        total_sum = water_fraction + protein_fraction + lipid_fraction + carbs_fraction + ash_fraction
        
        biochem_mass_g = {
            "water": (water_fraction / total_sum) * total_fluid_mass_g,
            "protein": (protein_fraction / total_sum) * total_fluid_mass_g,
            "lipid": (lipid_fraction / total_sum) * total_fluid_mass_g,
            "carbs": (carbs_fraction / total_sum) * total_fluid_mass_g,
            "ash": (ash_fraction / total_sum) * total_fluid_mass_g
        }
        
        return {
            "vessel_generation": vessel_generation,
            "fluid_segment_mass_g": total_fluid_mass_g,
            "biochemical_mass_g": {k: round(v, 3) for k, v in biochem_mass_g.items()},
            "iron_content_mg": round(total_fluid_mass_g * 0.0005, 3) # Tracking functional heme groups
        }

    def compute_airway_wall_composition(self, generation: int, tissue_volume_cm3: float) -> dict:
        """
        Resolves the physical chemical structure of the respiratory epithelial/cartilaginous wall boundary layer.
        """
        # Mucosal structural tissue density ~ 1.04 g/cm3
        wall_mass_g = tissue_volume_cm3 * 1.04
        
        # Airway Surface Liquid (ASL) & cartilage matrix composite configurations
        blueprint_fractions = {"water": 0.83 * self.chi, "protein": 0.13, "lipid": 0.02, "carbs": 0.01, "ash": 0.01}
        f_sum = sum(blueprint_fractions.values())
        
        biochem_mass_g = {k: (v / f_sum) * wall_mass_g for k, v in blueprint_fractions.items()}
        
        return {
            "airway_generation": generation,
            "calculated_wall_mass_g": wall_mass_g,
            "biochemical_mass_g": {k: round(v, 3) for k, v in biochem_mass_g.items()}
        }


TARGET_PROTEINS_COMPREHENSIVE = {
    # --- I. SOLID ORGAN METASTASIS (HEMATIC) ---
    
    # Major Visceral Organs
    'Liver (Hepatic)': [],
    'Lungs (Pulmonary)': [],
    'Kidneys (Renal)': [],
    'Adrenals': [],
    'Spleen': [],
    'Pancreas': [],
    'Thyroid': [],
    
    # Gastrointestinal Tract
    'Stomach': [],
    'Small Intestine': [],
    'Large Intestine (Colorectal)': [],
    
    # Reproductive/Genitourinary
    'Prostate': [],
    'Ovaries': [],
    'Uterus': [],
    'Testes': [],
    'Bladder': [],
    
    # Central Nervous System
    'Brain': [],
    'Spinal Cord': [],
    
    # Skin and Soft Tissue
    'Skin (Dermal)': [],
    'Soft Tissue (Muscular)': [],
    
    # --- II. LYMPHOMA / LYMPHATIC SPREAD (LYMPHATIC ARTERIAL FLOW) ---
    
    'Cervical Lymph Nodes (Neck)': [],
    'Axillary Lymph Nodes (Armpit)': [],
    'Mediastinal Lymph Nodes (Chest)': [],
    'Abdominal Lymph Nodes (Mesenteric)': [],
    'Pelvic Lymph Nodes': [],
    'Inguinal Lymph Nodes (Groin)': [],
    
    # --- III. SKELETAL METASTASIS (BONE ARTERIAL FLOW) ---
    
    'Vertebrae (Spine)': [],
    'Pelvis': [],
    'Femur (Thigh Bone)': [],
    'Humerus (Upper Arm Bone)': [],
    'Ribs': [],
    'Skull': [],
    'Sternum': [],
    
    # --- IV. OTHER VITAL SYSTEMS ---
    'Peritoneum (Abdominal Lining)': [],
    'Pericardium (Heart Sac)': [],
    'Pleura (Lung Lining)': [],
    'Bone Marrow': []
}

# Instruction: Fill the brackets [] with target protein factors (e.g., ['Protein_X', 'Receptor_Y'])
# for the specific metastatic cell type being modeled.
