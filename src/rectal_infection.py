import math
# ==============================================================================
# 🪝 PYCNOGONID BIOENERGETIC ENGINE INTEGRATION HOOK
# ==============================================================================
import os
import json
from src.biomass_scaler import PycnogonidBiomassEngine
from src.population_engine import PycnogonidPopulationEngine
from src.tracker_bridge import TrackerBiomassOrchestrator

# 1. Resolve relative directory paths for standard data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTEIN_DATA_PATH = os.path.join(BASE_DIR, "src", "data", "target_proteins.json")
THERMAL_DATA_PATH = os.path.join(BASE_DIR, "src", "data", "pycnogonid_thermal_profiles.json")

# 2. Safely parse JSON parameter files
with open(PROTEIN_DATA_PATH, "r") as pf:
    protein_configuration = json.load(pf)
with open(THERMAL_DATA_PATH, "r") as tf:
    thermal_profiles = json.load(tf)

# 3. Instantiate the sub-calculation blocks
# Baseline morphology: 8.0mm femur, 0.5mm baseline leg radius
biomass_calculation_core = PycnogonidBiomassEngine({
    "base_femur_length_mm": 8.0, 
    "base_leg_radius_mm": 0.5
})

# Extract target species profile constants for the Lefkovitch population tensor
species_key = "Pycnogonidae_shallow_profile"
population_config_wrapper = {
    "breeding_matrix_config": thermal_profiles["pycnogonid_thermal_development_matrix"][species_key]
}
population_calculation_core = PycnogonidPopulationEngine(population_config_wrapper)

# 4. Initialize the communication orchestrator bridge
biomass_tracker_orchestrator = TrackerBiomassOrchestrator(
    biomass_engine=biomass_calculation_core,
    population_engine=population_calculation_core,
    protein_config=protein_configuration
)

# 5. Pre-seed the agent's internal nutrient pool to enable reproduction calculations
# Adjust this value (in mm3) depending on the initial state of the tracker agent
biomass_calculation_core.accumulated_protein_vol = 6.20 

print("✅ Pycnogonid bioenergetic engine successfully hooked into tracking routing.")

# ==============================================================================
# 🔄 INNER LOOP INTEGRATION EXAMPLE (Insert inside your path navigation loops)
# ==============================================================================
# Inside your tracking loops where the agent jumps between nodes, paste this step block:

# Target Tracking Variables Mock (Ensure these match your live tracking outputs)
current_tracking_node_id = "cerebral_capillary_bed_alpha" # Live node ID string
time_delta_this_step = 1.0 # Duration spent at this coordinates node (seconds)

# Live climate context variables query
live_environment_context = {
    "temperature": 14.0, 
    "turbulence": 0.0, 
    "ph": 8.1
}

# RUNTIME EXECUTION CALL
biomass_step_report = biomass_tracker_orchestrator.process_tracker_location_step(
    location_id=current_tracking_node_id,
    local_env_context=live_environment_context,
    delta_time=time_delta_this_step
)

# Parse output telemetry results for automated diagnostic tracking
if biomass_step_report["status"] == "REPRODUCTION_CYCLING":
    print(f"🔥 ALERT: Gonopore activation confirmed at node [{current_tracking_node_id}].")
    print(f"   New generational output vector: {biomass_step_report['larval_pool_generation']}")
else:
    residual_reserves = biomass_step_report["protein_reserves_remaining"]
    print(f"🔹 Absorbing nutrients at node [{current_tracking_node_id}]. Current internal pool: {residual_reserves:.4f} mm3")
# ==============================================================================

# Insert this updated pattern inside your execution tracking scripts:

from src.biomass_scaler import PycnogonidBiomassEngine
from src.population_engine import PycnogonidPopulationEngine
from src.tracker_bridge import TrackerBiomassOrchestrator
from src.tracker_logger import TrackerDiagnosticLogger

# 1. Initialize core engines and communication paths
bio_eng = PycnogonidBiomassEngine({"base_femur_length_mm": 8.0, "base_leg_radius_mm": 0.5})
pop_eng = PycnogonidPopulationEngine({"breeding_matrix_config": {
    "leslie_matrix_coefficients": {"fecundity_adult_f": 15.0, "fecundity_brooding_f": 40.0, "survival_larva_to_juv": 0.25, "survival_juv_to_adult": 0.60, "adult_retention_rate": 0.92},
    "environmental_sensitivities": {"optimal_breeding_temp_c": 14.0, "thermal_exponential_limit_q10": 2.0, "turbulence_fertilization_penalty_exponent": 1.5, "optimal_ph": 8.1, "ph_tolerance_sigma": 0.35}
}})
orchestrator = TrackerBiomassOrchestrator(bio_eng, pop_eng, {})

# 2. Instantiate the new diagnostic logger module
diagnostic_logger = TrackerDiagnosticLogger(filename_prefix="cerebral_path_run")

# --- Inside your active node navigation loop ---
current_node = "cerebral_capillary_bed_alpha"
env_context = {"temperature": 14.2, "turbulence": 0.0, "ph": 8.1}

# Execute the bioenergetic tensor calculation step
step_report = orchestrator.process_tracker_location_step(
    location_id=current_node,
    local_env_context=env_context,
    delta_time=1.0
)

# Extract internal parameters to ensure total visibility inside the JSON file
current_cf = 1.3 if bio_eng.accumulated_protein_vol > 5.0 else 1.0
internal_telemetry = {
    "protein_vol": bio_eng.accumulated_protein_vol,
    "condition_factor": current_cf
}

# 3. Log the step payload seamlessly into outbound/
diagnostic_logger.log_step(
    location_id=current_node,
    local_env=env_context,
    report_output=step_report,
    internal_metrics=internal_telemetry
)

class DirectRectalEntryModel:
    def __init__(self, object_max_width_mm: float, object_driving_force_mmHg: float):
        """
        Models the physical entry mechanics, survival boundaries, and reflex clearance
        of an object entering directly into the terminal rectal vault.
        """
        self.obj_width = object_max_width_mm
        self.obj_force = object_driving_force_mmHg
        self.resting_sphincter_pressure_mmHg = 65.0 # Average adult resting tone

    def evaluate_mechanical_entry(self) -> dict:
        """
        Calculates whether the object can physically breach the high-pressure anal canal.
        """
        # Mechanical force comparison
        breach_successful = self.obj_force > self.resting_sphincter_pressure_mmHg
        
        return {
            "anal_sphincter_resting_pressure_mmHg": self.resting_sphincter_pressure_mmHg,
            "object_exerted_driving_force_mmHg": self.obj_force,
            "mechanical_entry_allowed": breach_successful,
            "status": "Blocked by Sphincter Muscular Tone" if not breach_successful else "Sphincter Overcome / Entry Achieved"
        }

    def simulate_internal_survival_window(self, hydration_level: float) -> dict:
        """
        Calculates the oxygen depletion and osmotic survival timeline of an organism inside the lumen.
        """
        # Dissolved oxygen availability inside the rectal vault stool matrix is effectively zero
        luminal_oxygen_partial_pressure_mmHg = 0.0
        
        # Survival half-life (in minutes) under absolute anoxia and osmotic desiccation
        survival_half_life_min = 8.5 * hydration_level
        
        # An external marine organism reaches zero viability rapidly in anaerobic tissue environments
        max_viability_duration_minutes = survival_half_life_min * 3.0

        return {
            "internal_oxygen_status": "ABSOLUTE ANOXIA (HYPOXIC CRISIS)",
            "osmotic_dehydration_strain": "CRITICAL HYPEROSMOLAL STRESS",
            "maximum_organism_survival_window_minutes": round(max_viability_duration_minutes, 2),
            "viable_colonization_possible": False
        }

    def calculate_expulsion_reflex(self) -> dict:
        """
        Models the involuntary neuro-muscular defecation reflex triggered by a foreign mass.
        """
        # The presence of a solid object stretches rectal wall mechanoreceptors
        # This triggers the rectoanal inhibitory reflex (RAIR) and the defecation reflex
        rectal_distension_volume_cm3 = math.pi * ((self.obj_width / 20.0) ** 2) * 5.0
        
        # When distension volume crosses 15-20 cm3, the urge to evacuate becomes mandatory
        reflex_trigger_active = rectal_distension_volume_cm3 > 15.0
        
        return {
            "calculated_rectal_distension_cm3": round(rectal_distension_volume_cm3, 2),
            "mechanoreceptor_activation_status": "CRITICAL" if reflex_trigger_active else "MODERATE",
            "involuntary_defecation_reflex_triggered": True, # Mandated by foreign body presence
            "projected_clearance_timeline_hours": 0.25 if reflex_trigger_active else 2.0,
            "final_fate": "EXCRETED / MECHANICAL EXPULSION VIA DEFECATION"
        }

# =====================================================================
# Verification Execution Sandbox
# =====================================================================
if __name__ == "__main__":
    # Model an aggressive 10mm object trying to force entry with a low driving force (5 mmHg)
    low_force_intruder = DirectRectalEntryModel(object_max_width_mm=10.0, object_driving_force_mmHg=5.0)
    
    print("=========================================================================")
    print("DIRECT ANRECTAL ENTRY AND EXPULSION SIMULATION LOGS")
    print("=========================================================================\n")
    
    report_a = low_force_intruder.evaluate_mechanical_entry()
    print("--- SCENARIO A: PASSIVE OR SELF-DIRECTED ENTRY ATTEMPT ---")
    print(f" Barrier Pressure:   {report_a['anal_sphincter_resting_pressure_mmHg']} mmHg")
    print(f" Intruder Force:     {report_a['object_exerted_driving_force_mmHg']} mmHg")
    print(f" Entry Status:       {report_a['mechanical_entry_allowed']} ({report_a['status']})\n")

    # Model a forced introduction scenario (e.g., mechanical insertion overriding the sphincter at 90 mmHg)
    forced_intruder = DirectRectalEntryModel(object_max_width_mm=25.0, object_driving_force_mmHg=90.0)
    report_b = forced_intruder.evaluate_mechanical_entry()
    
    print("--- SCENARIO B: MECHANICAL OVERRIDE INSERTION ---")
    print(f" Entry Status:       {report_b['mechanical_entry_allowed']} ({report_b['status']})")
    
    if report_b['mechanical_entry_allowed']:
        survival = forced_intruder.simulate_internal_survival_window(hydration_level=1.0)
        expulsion = forced_intruder.calculate_expulsion_reflex()
        
        print(f"\n[LUMINAL CRISIS METRICS]:")
        print(f" - Atmospheric Environment:   {survival['internal_oxygen_status']}")
        print(f" - Osmotic Status:           {survival['osmotic_dehydration_strain']}")
        print(f" - Maximum Viability Window:  {survival['maximum_organism_survival_window_minutes']} minutes until total asphyxiation.")
        print(f" - Long-Term Host Viability:  {survival['viable_colonization_possible']}")
        
        print(f"\n[HOST CLEARANCE DYNAMICS]:")
        print(f" - Rectal Distension Metric:  {expulsion['calculated_rectal_distension_cm3']} cm³")
        print(f" - Defecation Reflex Vector:  {expulsion['involuntary_defecation_reflex_triggered']}")
        print(f" - Projected Clearance Time:  {expulsion['projected_clearance_timeline_hours']} hours or less")
        print(f" - Terminal System Endpoint:  {expulsion['final_fate']}")
