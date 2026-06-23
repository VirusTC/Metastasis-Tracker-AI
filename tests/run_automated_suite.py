import yaml
from src.trauma_coagulation_core import AdvancedCoagulationHemorrhageEngine

def execute_automated_repository_testing():
    # Read the standardized patient profile matrix config
    with open("tests/patient_profiles.yaml", "r") as stream:
        config = yaml.safe_load(stream)
        
    steps = config["global_test_metadata"]["default_time_steps_sec"]
    print("=========================================================================")
    print(f"LAUNCHING PIPELINE RUNNER DEPLOYMENT ENGINE (STEPS: {steps}s)")
    print("=========================================================================\n")

    for cohort in config["patient_cohorts"]:
        pid = cohort["profile_id"]
        labs = cohort["clinical_labs"]
        
        # Instantiate the physiology engine using configured variables directly
        engine = AdvancedCoagulationHemorrhageEngine(
            tip_radius_microns=5.0, # Test tracking with a static standard 5um apex
            plt_count_uL=labs["platelet_count_uL"],
            clotting_factor_index=labs["clotting_factor_efficiency"]
        )
        
        # Run active leakage and occlusion simulation
        report = engine.simulate_clotted_hemorrhage(initial_p_vessel_mmHg=95.0, time_steps_sec=steps)
        
        print(f" [COHORT TEST RUN: {pid}]")
        print(f"  -> Input Platelets: {labs['platelet_count_uL']:,} uL | Factor Rating: {labs['clotting_factor_efficiency']}")
        print(f"  -> Hemostasis Sealed: {report['clotting_achieved_successfully']} | Cumulative Fluid Blood Loss: {report['total_blood_loss_volume_mL']} mL")
        print(f"  -> Effective Residual Hole Open Size: {report['timeline_logs'][-1]['effective_orifice_area_um2']} um²\n")

if __name__ == "__main__":
    execute_automated_repository_testing()
