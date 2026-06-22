import math

class CompleteMetabolicCTCUniverse:
    def __init__(self, height_cm: float, weight_kg: float, hydration_level: float):
        self.height_m = height_cm / 100.0
        self.weight = weight_kg
        self.chi = hydration_level
        
        # Fundamental Physiology baselines
        self.bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
        self.cardiac_output_L_min = self.bsa * 3.0 * math.sqrt(self.chi)
        
        # Enzyme Profile
        self.ca_acceleration_factor = 18500.0  # CA-II/IV kinetic multiplier
        self.k_f_uncatalyzed = 0.03            # s^-1
        
    def calculate_ca_kinetics(self, co2_mmol_L: float, hco3_mmol_L: float, local_ph: float) -> dict:
        """
        Calculates the accelerated conversion rate of carbon dioxide to protons
        within the RBC boundary layers.
        """
        h_insitu = math.pow(10, -local_ph) * 1e3 # mmol/L
        
        # Scale up forward and reverse rate constants using the acceleration factor
        k_f_catalyzed = self.k_f_uncatalyzed * self.ca_acceleration_factor
        k_r_catalyzed = k_f_catalyzed / 3.4e-4 # Equilibrium dissociation tracking constant
        
        forward_flux = k_f_catalyzed * co2_mmol_L
        reverse_flux = k_r_catalyzed * hco3_mmol_L * h_insitu
        net_flux = forward_flux - reverse_flux
        
        return {
            "kinetic_acceleration_factor": self.ca_acceleration_factor,
            "forward_hydration_flux_mmol_L_s": forward_flux,
            "reverse_dehydration_flux_mmol_L_s": reverse_flux,
            "net_proton_generation_rate": net_flux
        }

    def simulate_respiratory_compensation(self, current_arterial_ph: float, baseline_pco2: float) -> dict:
        """
        Simulates the brainstem cheoreceptor feedback loop executing hyperventilation
        to rescue the blood pool from acidosis.
        """
        ve_baseline = 6.0  # Liters/min standard resting minute ventilation
        
        # Sensitivity parameters to deviations from homeostatic norms (pH 7.40, pCO2 40mmHg)
        s_central_ph = 115.0 
        s_peripheral_pco2 = 1.2
        
        ph_deviation = max(0.0, 7.40 - current_arterial_ph)
        pco2_deviation = max(0.0, baseline_pco2 - 40.0)
        
        # Calculate dynamic target minute ventilation
        minute_ventilation_L_min = ve_baseline + (s_central_ph * ph_deviation) + (s_peripheral_pco2 * pco2_deviation)
        minute_ventilation_L_min = min(90.0, max(ve_baseline, minute_ventilation_L_min)) # Human ceiling cap
        
        # Calculate corrected homeostatic pCO2 following expiration washout rules
        washout_coefficient = minute_ventilation_L_min / ve_baseline
        compensated_pco2 = baseline_pco2 / washout_coefficient
        
        return {
            "induced_minute_ventilation_L_min": minute_ventilation_L_min,
            "washout_efficiency_multiplier": washout_coefficient,
            "post_compensation_pco2_mmHg": max(15.0, compensated_pco2)
        }

    def predict_ctc_seeding_matrix(self, generation: int, local_ph: float, vessel_radius_m: float, input_ctc_count: int) -> dict:
        """
        Integrates downstream physiological data directly into tumor cell transport,
        mechanical deformation entrapment, and endothelial adhesion matrices.
        """
        # Step 1: Evaluate micro-environmental acidosis severity
        acid_stress_factor = max(0.0, 7.40 - local_ph)
        
        # Step 2: Model structural cell rigidity mechanics (Deformability loss under acid conditions)
        # Low pH compromises tumor cell membranes, making them brittle
        ctc_rigidity_index = 1.0 + (5.5 * acid_stress_factor)
        
        # Step 3: Compute mechanical entrapment odds (Generation 30 capillaries represent high hazard)
        vessel_diameter_micron = vessel_radius_m * 2.0 * 1e6
        if vessel_diameter_micron < 12.0: # Capillary boundary threshold check
            base_entrapment_prob = 0.35
            entrapment_probability = base_entrapment_prob * ctc_rigidity_index
        else:
            entrapment_probability = 0.01 * ctc_rigidity_index
        entrapment_probability = min(0.98, entrapment_probability)
        
        # Step 4: Model endothelial biochemical adhesion upregulations (Integrin/Selectin binding affinity)
        # Inflammatory response to acid conditions enhances receptor binding chances
        adhesion_probability = 0.05 * (1.0 + (3.0 * acid_stress_factor)) if entrapment_probability < 0.5 else 0.85
        adhesion_probability = min(0.95, adhesion_probability)
        
        # Combine probabilities to output dynamic seeding yield metrics
        total_seeding_probability = entrapment_probability + (1.0 - entrapment_probability) * adhesion_probability
        successfully_seeded_cells = int(input_ctc_count * total_seeding_probability)
        surviving_circulating_cells = input_ctc_count - successfully_seeded_cells
        
        return {
            "vessel_generation": generation,
            "vessel_diameter_microns": vessel_diameter_micron,
            "calculated_ctc_rigidity": ctc_rigidity_index,
            "entrapment_risk_percent": entrapment_probability * 100.0,
            "endothelial_adhesion_affinity_percent": adhesion_probability * 100.0,
            "net_seeding_probability_percent": total_seeding_probability * 100.0,
            "cells_seeded_count": successfully_seeded_cells,
            "cells_remaining_in_flow": surviving_circulating_cells
        }

# =====================================================================
# Full Verification Loop Execution
# =====================================================================
if __name__ == "__main__":
    universe = CompleteMetabolicCTCUniverse(height_cm=175.0, weight_kg=72.0, hydration_level=0.92)
    
    print("=========================================================================")
    print("INTEGRATED KINETIC, RESPIRATORY, AND ONCOLOGICAL SYSTEM ENGINE")
    print("=========================================================================\n")
    
    # Context Phase 1: Acidosis onset with high CO2 pooling in tissues
    test_co2 = 2.4   # mmol/L
    test_hco3 = 22.0 # mmol/L
    acidic_ph = 7.15 # Severely compromised organ zone
    
    kinetic_report = universe.calculate_ca_kinetics(co2_mmol_L=test_co2, hco3_mmol_L=test_hco3, local_ph=acidic_ph)
    print("--- 1. RBC CARBONIC ANHYDRASE BOUNDARY KINETICS ---")
    print(f" Carbonic Anhydrase Acceleration Multiplier: {kinetic_report['kinetic_acceleration_factor']}x")
    print(f" Accelerated Protons Generated inside RBC Layer:  {kinetic_report['net_proton_generation_rate']:.2f} mmol/L/s\n")
    
    # Context Phase 2: Chemoreceptors detect pH crash and drive hyperventilation rescue
    resp_report = universe.simulate_respiratory_compensation(current_arterial_ph=acidic_ph, baseline_pco2=58.0)
    print("--- 2. CENTRAL CHEMORECEPTOR RESPIRATORY FEEDBACK LOOP ---")
    print(f" Acid-Triggered Minute Ventilation Demand: {resp_report['induced_minute_ventilation_L_min']:.1f} L/min (Hyperventilation Active)")
    print(f" CO2 Expiration Washout Performance Factor: {resp_report['washout_efficiency_multiplier']:.2f}x speed")
    print(f" Compensated Downstream Central Arterial pCO2: {resp_report['post_compensation_pco2_mmHg']:.1f} mmHg\n")
    
    # Context Phase 3: Connect metrics directly to the Metastasis Tracker Seeding Logic
    print("--- 3. ENVIRONMENTAL TUMOR-CELL METASTASIS SEEDING LAYER ---")
    sample_ctc_load = 10000 # Cells entered into regional flow vector
    
    # Trace macro-vessel vs capillary entrapment properties under acid stress
    macro_vessel_seeding = universe.predict_ctc_seeding_matrix(generation=4, local_ph=acidic_ph, vessel_radius_m=0.0025, input_ctc_count=sample_ctc_load)
    micro_capillary_seeding = universe.predict_ctc_seeding_matrix(generation=30, local_ph=acidic_ph, vessel_radius_m=0.0000045, input_ctc_count=sample_ctc_load)
    
    print(f" Large Artery Node (Gen 4 | Diameter: {macro_vessel_seeding['vessel_diameter_microns']:.1f} um):")
    print(f"  -> Adhesion Risk: {macro_vessel_seeding['endothelial_adhesion_affinity_percent']:.1f}% | Total Seeded: {macro_vessel_seeding['cells_seeded_count']} cells")
    
    print(f"\n Micro Capillary Bed Node (Gen 30 | Diameter: {micro_capillary_seeding['vessel_diameter_microns']:.1f} um):")
    print(f"  -> Rigid Mechanical Entrapment Risk: {micro_capillary_seeding['entrapment_risk_percent']:.1f}%")
    print(f"  -> Total Metastatic Colonization Yield:   {micro_capillary_seeding['cells_seeded_count']} cells / {sample_ctc_load} transit pool input.")


class PatientSimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the anatomical engine.
        :param height_cm: Patient height in centimeters
        :param weight_kg: Patient weight in kilograms
        :param body_build: 'ectomorph' (slender), 'mesomorph' (average), 'endomorph' (heavy)
        :param hydration_level: Relative plasma volume factor (1.0 = normal, 0.85 = dehydrated, 1.15 = overhydrated)
        """
        self.height_m = height_cm / 100.0
        self.height_cm = height_cm
        self.weight = weight_kg
        self.build = body_build.lower()
        self.chi = hydration_level  # Hydration scaling factor
        
        # Core blood viscosity (Pascal-seconds) - scales inversely with hydration (hemoconcentration)
        self.mu = 0.0035 * (1.0 / (self.chi ** 0.5)) 
        
        # Calculate baseline anthropometrics
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight ** 0.425)
        self.lbm = self._calculate_lbm()
        self.total_blood_volume = 0.0656 * (self.weight ** 1.02) * self.chi
        self.cardiac_output = (self.bsa * 3.0 / 60.0) * (self.chi ** 0.5) # Liters per second

        import math

class AdvancedMetabolicEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        self.height_m = height_cm / 100.0
        self.height_cm = height_cm
        self.weight = weight_kg
        self.build = body_build.lower()
        self.chi = hydration_level  # Hydration tracking constant
        
        # Human baseline constants
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight ** 0.425)
        self.cardiac_output = (self.bsa * 3.0 / 60.0) * (self.chi ** 0.5) # L/sec
        self.hb = 150.0  # Hemoglobin grams/L
        
        # Calculate Kidney volume early to map renal retention dependencies
        self.kidney_volume_cm3 = 0.0003 * self.weight + 124.0 # Baseline single kidney
        
    def calculate_renal_bicarbonate_handling(self, plasma_hco3_mEq_L: float) -> dict:
        """
        Links calculated kidney volume dimensions directly to bicarbonate retention 
        and filtration capacity under homeostatic conditions.
        """
        # GFR scales linearly with total functioning renal parenchymal volume
        total_renal_volume = self.kidney_volume_cm3 * 2.0
        gfr_L_min = 0.00055 * total_renal_volume  # ~120 mL/min standard baseline
        
        # Bicarbonate filtration rate calculation
        hco3_filtered_rate = gfr_L_min * plasma_hco3_mEq_L  # mEq/min
        
        # Transport Maximum (Tm) scales with structural cellular mass of nephrons
        tm_hco3 = 0.022 * total_renal_volume  # mEq/min limit
        
        # Mass balance evaluation
        hco3_reabsorbed = min(hco3_filtered_rate, tm_hco3)
        hco3_excreted = max(0.0, hco3_filtered_rate - tm_hco3)
        retention_efficiency = (hco3_reabsorbed / hco3_filtered_rate) * 100.0 if hco3_filtered_rate > 0 else 100.0
        
        return {
            "total_kidney_volume_cm3": total_renal_volume,
            "calculated_gfr_L_min": gfr_L_min,
            "bicarbonate_filtered_mEq_min": hco3_filtered_rate,
            "renal_transport_maximum_tm": tm_hco3,
            "bicarbonate_reabsorbed_mEq_min": hco3_reabsorbed,
            "bicarbonate_excreted_urine_mEq_min": hco3_excreted,
            "retention_efficiency_percent": retention_efficiency
        }

    def compute_bohr_oxygen_offloading(self, generation: int, ph: float, po2_mmHg: float) -> dict:
        """
        Applies a modified Hill Equation with dynamic P50 shifts to calculate 
        localized oxygen saturation and offloading capacity along the vascular paths.
        """
        # Estimate regional pCO2 based on generation transition (arterial to capillary)
        pco2_z = 40.0 + (6.0 * (generation / 30.0))  # Scales 40mmHg to 46mmHg
        temp_c = 37.0
        
        # The Bohr Effect Formula: Shift P50 from standard baseline (26.8 mmHg)
        pH_delta = ph - 7.40
        pco2_delta = math.log10(pco2_z / 40.0)
        
        p50_shifted = 26.8 * math.pow(10, (-0.48 * pH_delta) + (0.06 * pco2_delta) + (0.024 * (temp_c - 37.0)))
        
        # Hill equation configuration for dynamic context execution
        hill_n = 2.7
        if po2_mmHg <= 0:
            so2 = 0.0
        else:
            so2 = math.pow(po2_mmHg, hill_n) / (math.pow(po2_mmHg, hill_n) + math.pow(p50_shifted, hill_n))
            
        # Total unbound gas availability metric calculation
        oxygen_content_mL_L = (1.34 * self.hb * so2) + (0.003 * po2_mmHg)
        
        return {
            "vessel_generation": generation,
            "local_p50_mmHg": p50_shifted,
            "oxygen_saturation_percent": so2 * 100.0,
            "total_oxygen_content_mL_L": oxygen_content_mL_L
        }

    def simulate_strenuous_exertion_lactate_curve(self, exertion_intensity: float) -> dict:
        """
        Calculates dynamic blood lactic acid production curves during exercise 
        and updates microvascular blood thickness overrides.
        
        :param exertion_intensity: Factor scaling from 0.0 (rest) to 1.0 (maximal failure)
        """
        exertion_intensity = max(0.0, min(1.0, exertion_intensity))
        
        # Anaerobic Threshold sigmoidal transition profile modeling
        j_basal = 1.0   # mmol/L baseline resting lactate pool
        j_max = 18.0    # Maximal anaerobic cap
        k_slope = 12.0  # Steeper inflection past threshold boundaries
        omega_threshold = 0.65  # Standard human aerobic limit point
        
        # Logistic sigmoidal curve execution
        lactate_mmol_L = j_basal + (j_max / (1.0 + math.exp(-k_slope * (exertion_intensity - omega_threshold))))
        
        # pH reduction secondary to anaerobic lactic proton production accumulation
        ph_drop_mod = 0.3 * (lactate_mmol_L / (j_basal + j_max))
        systemic_arterial_ph = 7.40 - ph_drop_mod
        
        # Viscosity multiplier coupling factor tracking erythrocyte stiffness shifts
        erythrocyte_rigidity_multiplier = 1.0 + (0.022 * lactate_mmol_L)
        
        return {
            "exertion_workload_factor": exertion_intensity,
            "circulating_lactate_mmol_L": lactate_mmol_L,
            "induced_acidosis_ph_drop": ph_drop_mod,
            "projected_arterial_ph": systemic_arterial_ph,
            "blood_viscosity_rigidity_multiplier": erythrocyte_rigidity_multiplier
        }

# =====================================================================
# Pipeline Diagnostics Sandbox Validation
# =====================================================================
if __name__ == "__main__":
    # Initialize engine for an average athletic build patient
    engine = AdvancedMetabolicEngine(height_cm=180.0, weight_kg=78.0, body_build="mesomorph", hydration_level=1.0)
    
    print("=========================================================================")
    print("PHYSIOLOGICAL MODEL UPGRADE BREAKDOWNS")
    print("=========================================================================\n")
    
    # 1. Test Renal Retention Linked directly to Kidney Dimensions
    print("--- 1. RENAL BICARBONATE HANDLING AND RETENTION MATRIX ---")
    renal_data = engine.calculate_renal_bicarbonate_handling(plasma_hco3_mEq_L=28.0) # High bicarbonate pool
    print(f" Total Combined Kidney Volume:  {renal_data['total_kidney_volume_cm3']:.1f} cm³")
    print(f" Glomerular Filtration (GFR):   {renal_data['calculated_gfr_L_min']*1000:.1f} mL/min")
    print(f" Reabsorption Capacity (Tm):    {renal_data['renal_transport_maximum_tm']:.3f} mEq/min")
    print(f" Urinary Bicarbonate Waste:     {renal_data['bicarbonate_excreted_urine_mEq_min']:.3f} mEq/min")
    print(f" Systemic Retention Efficiency: {renal_data['retention_efficiency_percent']:.1f}%\n")
    
    # 2. Test Bohr Effect Oxy-Saturation Curves across Generations
    print("--- 2. GENERATIONAL BOHR EFFECT SATURATION SHIFTS ---")
    # Simulate high oxygen drop arriving inside acidic muscle tissue capillaries (Gen 30)
    arterial_node = engine.compute_bohr_oxygen_offloading(generation=0, ph=7.41, po2_mmHg=95.0)
    capillary_node = engine.compute_bohr_oxygen_offloading(generation=30, ph=7.32, po2_mmHg=38.0)
    
    print(f" Aorta (Gen 0)   -> Local P50: {arterial_node['local_p50_mmHg']:.1f} mmHg | Saturation: {arterial_node['oxygen_saturation_percent']:.1f}%")
    print(f" Capillary (Gen 30) -> Local P50: {capillary_node['local_p50_mmHg']:.1f} mmHg | Saturation: {capillary_node['oxygen_saturation_percent']:.1f}% (Bohr Shift Offloading Driven)")
    print(f" Total Gas Delivered to Tissue Space: {arterial_node['total_oxygen_content_mL_L'] - capillary_node['total_oxygen_content_mL_L']:.2f} mL O2 per Liter of Blood Flow\n")
    
    # 3. Test Anaerobic Exertion Spikes and Viscosity Overrides
    print("--- 3. ANAEROBIC LACTIC ACID CURVE OVER EXERTION FIELDS ---")
    resting_metrics = engine.simulate_strenuous_exertion_lactate_curve(exertion_intensity=0.1)
    stressed_metrics = engine.simulate_strenuous_exertion_lactate_curve(exertion_intensity=0.85) # High exercise intensity
    
    print(f" Rest Exertion (10%)  -> Lactate: {resting_metrics['circulating_lactate_mmol_L']:.2f} mmol/L | Blood pH: {resting_metrics['projected_arterial_ph']:.2f}")
    print(f" Peak Exertion (85%) -> Lactate: {stressed_metrics['circulating_lactate_mmol_L']:.2f} mmol/L | Blood pH: {stressed_metrics['projected_arterial_ph']:.2f}")
    print(f" Erythrocyte Rigidity Vector: Viscosity scaled up by factor of * {stressed_metrics['blood_viscosity_rigidity_multiplier']:.3f} inside systemic microcirculatory paths.")

        def generate_systemic_ph_matrix(self, salivary_ph: float) -> dict:
        """
        Estimates localized pH levels across all vascular generations, airway trees, 
        and organs using a baseline salivary pH reading.
        
        :param salivary_ph: Measured pH from a standard oral swab (typically 6.2 - 7.6)
        :return: Comprehensive anatomical dictionary containing mapped pH values
        """
        # Clamp input to physiolgically viable limits to avoid engine crashes
        salivary_ph = max(5.5, min(8.0, salivary_ph))
        
        # Step 1: Calibrate central arterial blood pH baseline
        # Healthy reference baseline shift: Saliva 6.7 -> Arterial Blood 7.40
        blood_baseline_ph = 7.40 + 0.5 * (salivary_ph - 6.7)
        
        # Tight homeostatic clamp checking to simulate high-level biological buffering
        blood_baseline_ph = max(6.8, min(7.8, blood_baseline_ph))
        
        # Step 2: Compute Circulatory Path pH Degradation (Arterial vs. Venous Shift)
        # As blood drops down systemic trees, metabolic pCO2 increases, dropping pH.
        systemic_ph_profile = []
        pulmonary_ph_profile = []
        
        for z in range(31):
            # Systemic loop starts at clean arterial baseline, shifts toward venous (~ -0.05 pH) at capillary line
            systemic_z_ph = blood_baseline_ph - (0.05 * (z / 30.0))
            systemic_ph_profile.append({
                "generation": z,
                "vessel_class": "Arterial" if z < 20 else ("Capillary" if z == 30 else "Arteriolar"),
                "estimated_ph": round(systemic_z_ph, 3)
            })
            
            # Pulmonary loop carries acidic venous return, purging CO2 as it climbs to alveolar gas interface
            pulmonary_z_ph = (blood_baseline_ph - 0.05) + (0.05 * (z / 30.0))
            pulmonary_ph_profile.append({
                "generation": z,
                "vessel_class": "Pulmonary Venous Transition" if z > 20 else "Pulmonary Arterial Trunk",
                "estimated_ph": round(pulmonary_z_ph, 3)
            })
            
        # Step 3: Compute Airway Path pH Profile (Mucosal Surface / Fluid Lining Layer)
        # Airway surface liquid (ASL) drops in pH from the humid trachea down to terminal gas exchange centers.
        airway_ph_profile = []
        # Upper trachea aligns closely with oral/salivary baseline environment
        tracheal_base_ph = salivary_ph 
        
        for z in range(24):
            # ASL becomes more acidic down the tree due to local cellular metabolic acid secretion
            airway_z_ph = tracheal_base_ph - (0.4 * (z / 23.0))
            airway_ph_profile.append({
                "generation": z,
                "zone": "Conducting" if z <= 16 else "Respiratory",
                "estimated_ph": round(airway_z_ph, 3)
            })
            
        # Step 4: Map Organ Interstitial Matrix Microenvironments
        # Config values scale relative to current central blood buffering capabilities
        organ_ph_shifts = {
            "heart": -0.04,        # Myocardium matches central arterial blood closely
            "brain": -0.02,        # Protected strictly by the blood-brain barrier (BBB)
            "liver": -0.15,        # Highly metabolic hepatic tissue generates structural lactic/keto acids
            "kidney_each": -0.20,   # Renal parenchymal cells actively pump and excrete hydronium ions (H+)
            "spleen": -0.08,       # Sluggish pooling loops increase standard venous acid holding pools
            "pancreas": 0.35        # Alkaline outlier due to high production of bicarbonate fluids (HCO3-)
        }
        
        organ_ph_matrix = {}
        for organ_name, shift in organ_ph_shifts.items():
            estimated_organ_ph = blood_baseline_ph + shift
            organ_ph_matrix[organ_name] = {
                "estimated_interstitial_ph": round(estimated_organ_ph, 3),
                "cellular_state": "Normal Buffering" if 7.2 <= estimated_organ_ph <= 7.5 else "Acid Stress Alert"
            }
            
        return {
            "input_salivary_ph": salivary_ph,
            "calculated_arterial_baseline_ph": round(blood_baseline_ph, 3),
            "circulatory_paths": {
                "systemic_loop": systemic_ph_profile,
                "pulmonary_loop": pulmonary_ph_profile
            },
            "airway_paths": airway_ph_profile,
            "organ_matrix": organ_ph_matrix
        }

    def _calculate_lbm(self) -> float:
        # Boer formula for lean body mass
        if self.build == "ectomorph":
            return self.weight * 0.85
        # Standard fallback approximation
        return 1.10 * self.weight - 128 * ((self.weight / self.height_cm) ** 2)

    def generate_circulatory_tree(self) -> dict:
        """
        Generates dimensions, non-Newtonian regional viscosity, and pressure drops 
        across 31 generations (0 to 30) of the vascular networks.
        """
        # Base Aorta dimensions (Generation 0) scaled by BSA and hydration
        r_aorta = math.sqrt(self.bsa / (2.0 * math.pi)) * 0.01 * (self.chi ** 0.5) 
        l_aorta = 0.25 * math.sqrt(self.bsa) 
        
        # Base input pressures (Pascals)
        p_systemic_in = 13332.0 
        p_pulmonary_in = 2000.0
        
        systemic_tree = []
        pulmonary_tree = []
        q_total = self.cardiac_output / 1000.0  # m^3/s

        # Baseline hematocrit scaled directly by hydration state
        base_hct = 0.45 * (1.0 / self.chi)
        # Dynamic plasma viscosity base (Pascal-seconds)
        mu_plasma = 0.0012 * (1.0 / (self.chi ** 0.3))

        for z in range(31):
            num_vessels = 2 ** z
            
            # Geometry matrices (WBE fractal tracking)
            r_sys = r_aorta * (2.0 ** (-z / 3.0))
            l_sys = l_aorta * (2.0 ** (-z / 3.0))
            
            r_pulm = (r_aorta * 1.1) * (2.0 ** (-z / 3.0))
            l_pulm = (l_aorta * 0.2) * (2.0 ** (-z / 3.0))
            
            # Flow partitioning per individual vessel segment
            q_seg = q_total / num_vessels
            
            # 1. COMPUTE REGIONAL SHEAR RATES (gamma = 4 * Q / (pi * r^3))
            shear_sys = (4.0 * q_seg) / (math.pi * (r_sys ** 3)) if r_sys > 0 else 1000.0
            shear_pulm = (4.0 * q_seg) / (math.pi * (r_pulm ** 3)) if r_pulm > 0 else 1000.0
            
            # 2. APPLY REGIONAL VISCOSITY LAYER (Fåhræus-Lindqvist & Carreau-Yasuda Model)
            mu_sys = self._calculate_regional_viscosity(r_sys, base_hct, shear_sys, mu_plasma)
            mu_pulm = self._calculate_regional_viscosity(r_pulm, base_hct, shear_pulm, mu_plasma)
            
            # 3. POISEUILLE'S RESISTANCE USING THE DYNAMIC REGIONAL VISCOSITY
            r_hydro_sys = (8.0 * mu_sys * l_sys) / (math.pi * (r_sys ** 4))
            r_hydro_pulm = (8.0 * mu_pulm * l_pulm) / (math.pi * (r_pulm ** 4))
            
            # 4. PRESSURE DROP TRANSLATION
            delta_p_sys = q_seg * r_hydro_sys
            delta_p_pulm = q_seg * r_hydro_pulm
            
            p_systemic_in -= delta_p_sys
            p_pulmonary_in -= delta_p_pulm
            
            systemic_tree.append({
                "generation": z, "count": num_vessels, "radius_m": r_sys, "length_m": l_sys,
                "viscosity_Pa_s": mu_sys, "shear_rate_s1": shear_sys,
                "pressure_out_mmHg": max(0.0, p_systemic_in / 133.322)
            })
            pulmonary_tree.append({
                "generation": z, "count": num_vessels, "radius_m": r_pulm, "length_m": l_pulm,
                "viscosity_Pa_s": mu_pulm, "shear_rate_s1": shear_pulm,
                "pressure_out_mmHg": max(0.0, p_pulmonary_in / 133.322)
            })
            
        return {"systemic_arterial_tree": systemic_tree, "pulmonary_tree": pulmonary_tree}

    def _calculate_regional_viscosity(self, radius_m: float, hct: float, shear_rate: float, mu_plasma: float) -> float:
        """
        Mathematical helper combining structural confinement and velocity profiles.
        """
        d_micron = radius_m * 2.0 * 1e6
        
        # Guard rail for large macrovessels or macro-scaling defaults
        if d_micron <= 0:
            return 0.0035

        # Phase 1: Fåhræus-Lindqvist Effect (Confinement reduction of high shear viscosity)
        # Empirical Pries et al. formulation for effective structural hematocrit alignment
        if d_micron < 300.0:
            # Drop in relative discharge hematocrit due to cell migration to the centerline
            h_relative = hct * (0.4 + 0.6 * (1.0 - math.exp(-0.06 * d_micron)))
            mu_inf = mu_plasma * (1.0 + 2.5 * h_relative + 6.0 * (h_relative ** 2))
        else:
            mu_inf = mu_plasma * (1.0 + 2.5 * hct + 6.2 * (hct ** 2)) # Macro baseline

        # Phase 2: Carreau-Yasuda Low-Shear Thickening (Non-Newtonian erythrocyte aggregation)
        # Parameters configured for realistic red blood cell bridging mechanics
        mu_zero = mu_inf * 4.5    # Zero-shear limit viscosity (high aggregation)
        lambda_t = 3.313          # Relaxation time constant (seconds)
        n_index = 0.358           # Power-law index (shear-thinning behavior)
        a_index = 2.0             # Transition zone geometry parameter
        
        # Carreau-Yasuda formula combining micro-confinement limit and localized velocity profile
        viscosity = mu_inf + (mu_zero - mu_inf) * (1.0 + (lambda_t * abs(shear_rate)) ** a_index) ** ((n_index - 1.0) / a_index)
        return viscosity

    def generate_airway_tree(self) -> list:
        """
        Generates structural metrics for 24 generations (0 to 23) of the airway 
        using the Weibel Morphometric Model.
        """
        r_trachea = 0.006 * self.height_m # meters
        l_trachea = 0.07 * self.height_m # meters
        
        airway_tree = []
        for z in range(24):
            num_airways = 2 ** z
            r_z = r_trachea * (2.0 ** (-z / 3.0))
            l_z = l_trachea * (2.0 ** (-z / 3.0))
            vol_z = num_airways * (math.pi * (r_z ** 2) * l_z)
            
            airway_tree.append({
                "generation": z,
                "count": num_airways,
                "radius_m": r_z,
                "length_m": l_z,
                "total_volume_L": vol_z * 1000.0
            })
        return airway_tree

    def calculate_starling_forces(self, capillary_generation_data: dict) -> dict:
        """
        Calculates dynamic transcapillary fluid filtration flux using Starling's Equation.
        Jv = Kf * [(Pc - Pi) - sigma * (p_c - p_i)]
        """
        # Extract capillary hydrostatic pressure from systemic generation 30
        p_c = capillary_generation_data["pressure_out_mmHg"] 
        
        # Interstitial hydrostatic pressure (normally slightly negative to flat)
        p_i = -2.0 if self.chi >= 1.0 else -5.0 * (1.0 / self.chi)
        
        # Oncotic Pressures (mmHg) - Plasma oncotic pressure spikes during dehydration
        pi_c = 25.0 * (1.0 / self.chi) 
        pi_i = 5.0 # Interstitial oncotic pressure
        
        sigma = 0.95 # Reflection coefficient of capillary wall to plasma proteins
        
        # Capillary Filtration Coefficient (mL/min/mmHg/100g tissue baseline scaled to BSA)
        k_f = 0.5 * self.bsa 
        
        # Net Driving Pressure (NDP)
        ndp = (p_c - p_i) - sigma * (pi_c - pi_i)
        
        # Transcapillary fluid flux (Filtration rate: positive = filtration, negative = reabsorption)
        j_v = k_f * ndp
        
        return {
            "capillary_hydrostatic_pressure_mmHg": p_c,
            "interstitial_hydrostatic_pressure_mmHg": p_i,
            "plasma_oncotic_pressure_mmHg": pi_c,
            "interstitial_oncotic_pressure_mmHg": pi_i,
            "net_driving_pressure_mmHg": ndp,
            "net_fluid_flux_mL_min": j_v
        }

    def generate_organ_matrix(self) -> dict:
        """
        Calculates the complete organ mass, volume, and bounding boxes via allometrics.
        """
        w = self.weight
        organs = {}
        
        # Organ configs: { Name: (Mass_Eq, Density_g_cm3, L_scale, W_scale) }
        configs = {
            "heart": (lambda: 5.8 * (w ** 0.98), 1.06, 1.4, 1.0),
            "liver": (lambda: 878.0 * self.bsa - 262.0, 1.05, 2.3, 1.5),
            "kidney_each": (lambda: 1.45 * (w ** 0.95), 1.05, 2.2, 1.1),
            "spleen": (lambda: 2.6 * (w ** 0.94), 1.06, 2.4, 1.0),
            "pancreas": (lambda: 1.4 * (w ** 0.90), 1.04, 3.5, 0.8),
            "brain": (lambda: 230.0 * math.sqrt(self.height_m), 1.03, 1.45, 1.2)
        }
        
        for name, (mass_fn, density, l_sc, w_sc) in configs.items():
            mass = max(10.0, mass_fn())
            vol = mass / density
            linear_root = vol ** (1.0 / 3.0)
            
            organs[name] = {
                "mass_g": mass,
                "volume_cm3": vol,
                "approx_length_cm": linear_root * l_sc,
                "approx_width_cm": linear_root * w_sc
            }
        return organs

    def build_complete_dataset(self) -> dict:
        circ = self.generate_circulatory_tree()
        capillaries = circ["systemic_arterial_tree"][-1] # Generation 30
        
        return {
            "patient_metrics": {
                "bsa_m2": self.bsa,
                "lbm_kg": self.lbm,
                "blood_volume_L": self.total_blood_volume
            },
            "circulatory_network": circ,
            "airway_network": self.generate_airway_tree(),
            "organ_matrix": self.generate_organ_matrix(),
            "capillary_starling_forces": self.calculate_starling_forces(capillaries)
        }

# =====================================================================
# Execution & Sample Output Verification
# =====================================================================
if __name__ == "__main__":
    # Simulate a dehydrated, athletic patient (Height: 180cm, Weight: 80kg, Hydration: 88%)
    engine = PatientSimulationEngine(height_cm=180.0, weight_kg=80.0, body_build="mesomorph", hydration_level=0.88)
    dataset = engine.build_complete_dataset()
    
    print(f"--- PATIENT BASELINE METRICS ---")
    print(f"BSA: {dataset['patient_metrics']['bsa_m2']:.2f} m² | Blood Volume: {dataset['patient_metrics']['blood_volume_L']:.2f} L\n")
    
    print(f"--- VASCULAR TREE ANALYSIS SAMPLE ---")
    aorta = dataset["circulatory_network"]["systemic_arterial_tree"][0]
    cap = dataset["circulatory_network"]["systemic_arterial_tree"][-1]
    print(f"Gen 0 (Aorta): Count = {aorta['count']}, Radius = {aorta['radius_m']*100:.2f} cm, Mean Pressure = {aorta['pressure_out_mmHg']:.1f} mmHg")
    print(f"Gen 30 (Capillaries): Count = {cap['count']:,}, Radius = {cap['radius_m']*1e6:.1f} µm, Mean Pressure = {cap['pressure_out_mmHg']:.1f} mmHg\n")
    
    print(f"--- AIRWAY MODEL SAMPLE ---")
    trachea = dataset["airway_network"][0]
    alv_duct = dataset["airway_network"][23]
    print(f"Gen 0 (Trachea): Radius = {trachea['radius_m']*100:.2f} cm, Total Generation Vol = {trachea['total_volume_L']:.3f} L")
    print(f"Gen 23 (Alveolar Ducts): Count = {alv_duct['count']:,}, Radius = {alv_duct['radius_m']*1e6:.1f} µm\n")
    
    print(f"--- ORGAN DIMENSIONAL MATRIX ---")
    for organ, data in dataset["organ_matrix"].items():
    print(f" - {organ.upper()}: Mass = {data['mass_g']:.1f}g | Box: {data['approx_length_cm']:.1f} x {data['approx_width_cm']:.1f} cm")
    print(f"\n--- DYNAMIC CAPILLARY FLUID EXCHANGE (STARLING) ---")
    sf = dataset["capillary_starling_forces"]
    print(f" Net Driving Pressure: {sf['net_driving_pressure_mmHg']:.2f} mmHg")
    print(f" Dynamic Fluid Transudation Flux: {sf['net_fluid_flux_mL_min']:.3f} mL/min")

    
    ### Fluid Mechanics and Scaling Formulations Applied

    #### 1. Vascular Resistance & Pressure Decays (Poiseuille's Law)
    The fluid resistance of a singular blood vessel segment is derived via:
    \[R_{z} = \frac{8\mu l_z}{\pi r_z^4}\]
    Where \(\mu\) is fluid viscosity, \(l_z\) is segment length, and \(r_z\) is segment radius. The cumulative volume flow rate \(Q\) scales across each generation via \(Q_z = \frac{Q_{total}}{2^z}\). The pressure loss per tree level drops by:
    \[\Delta P_z = Q_z \times R_z\]

    #### 2. Transcapillary Equilibrium (Starling's Equation)
    The net movement of fluid between intravascular networks and the tissue spaces is calculated at Generation 30 via:
    \[J_v = K_f \cdot \left[ (P_c - P_i) - \sigma(\pi_c - \pi_i) \right]\]

    * \(P_c\): Capillary Hydrostatic Pressure (derived directly from vascular tree calculation)
    * \(P_i\): Interstitial Hydrostatic Pressure
    * \(\pi_c\): Plasma Oncotic Pressure (scaled inversely with the patient's hydration coefficient \(\chi\))
    * \(\pi_i\): Interstitial Oncotic Pressure
    * \(K_f\): Capillary Filtration Coefficient (scaled relative to total tissue mass via \(BSA\))
    * \(\sigma\): Reflection coefficient of the capillary barrier to standard systemic proteins

    ### ✅ Simulated Architectural Dataset Completed
    The script provides a baseline implementation that outputs structural dimensions for every organ, airway, and vascular generation based on explicit allometric equations and fluid dynamics.

    <FollowUp>
    If you want to integrate this architecture into a broader simulation loop, I can provide:
    * The adjustments needed to model **turbulent flow** in the upper airways (Reynolds Number checks)
    * Equations to simulate **varying heart rates** (dynamic blood pressure tracking)
    * Modifications to scale this model for **pediatric patients**

    Let me know how you would like to **extend the simulation**.
    </FollowUp>
