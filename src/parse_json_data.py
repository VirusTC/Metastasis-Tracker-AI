import json
import os
from src.sepsis_redox_engine import SepsisRedoxSimulationEngine

class JSONDataMappingPipeline:
    def __init__(self, target_json_filename: str):
        """
        Manages the automated parsing and data routing of enzymatic data structures.
        """
        self.filename = target_json_filename
        self.raw_data = self._load_json_file()

    def _load_json_file(self) -> dict:
        """
        Safely opens and handles decoding exceptions for target data objects.
        """
        if not os.path.exists(self.filename):
            # Fallback error mapping framework matching platform protocols
            raise FileNotFoundError(f"Critical Error: Data target missing at path: {self.filename}")
            
        with open(self.filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as err:
                raise ValueError(f"Mismatched data alignment or corrupt schema in file: {err}")

    def execute_sepsis_tracking_run(self, engine_instance: SepsisRedoxSimulationEngine, exposure_seconds: int) -> dict:
        """
        Iterates over loaded JSON configurations, feeds base activity parameters into 
        the covalent decay engine, and maps active osteolysis tracking profiles.
        """
        # Read the target array block from your json file schema
        enzyme_list = self.raw_data.get("enzymes", [])
        pipeline_run_results = {}

        print("=========================================================================")
        print(f"PIPELINE INGESTION: PARSING ACTIVE MATRIX CONFIGURATIONS ({len(enzyme_list)} Found)")
        print("=========================================================================\n")

        for enzyme in enzyme_list:
            # Extract standard naming keys from your data file fields
            name = enzyme.get("name", "unidentified_agent")
            class_type = enzyme.get("class", "protease")
            # Ingest activity rate, default to a baseline fallback if null
            concentration_proxy = enzyme.get("base_activity_uM_sec", 10.0)
            substrate_target = enzyme.get("target_substrate", "Soft-Tissue-Matrix")

            # Run the dynamic covalent electron-transfer subtraction differential loop
            report = engine_instance.simulate_enzyme_redox_degradation(
                enzyme_type=class_type,
                enzyme_concentration_uM=concentration_proxy,
                initial_covalent_density=0.98, # Start simulation with near-perfect initial bond density
                exposure_time_sec=exposure_seconds
            )

            # Store the resulting output objects keyed by unique enzyme identity
            pipeline_run_results[name] = {
                "enzyme_functional_class": class_type,
                "targeted_structural_substrate": substrate_target,
                "residual_covalent_electron_score": report["final_covalent_density_rating"],
                "pathological_liquefaction_active": report["pathological_liquefaction_detected"],
                "last_logged_cleavage_flux_val": report["timeline_logs"][-1]["instantaneous_cleavage_flux"]
            }

            # Print active tracking register metrics to console logs
            print(f" 🔍 [MAPPED OBJECT VECTOR]: {name.upper()}")
            print(f"    -> Functional Class:   {class_type:18} | Target: {substrate_target}")
            print(f"    -> Remaining e- Score: {report['final_covalent_density_rating']:.4f} (Ceiling limit: {report['critical_osteolysis_threshold']})")
            print(f"    -> Osteolysis / Resorption Alert Status: {report['pathological_liquefaction_detected']}")
            print(f"    " + "-"*65)

        return pipeline_run_results

# =====================================================================
# Main Integration Entry Vector (Verification Execution Sandbox)
# =====================================================================
if __name__ == "__main__":
    # Setup step 1: Instantiate the sepsis redox engine with an active clinical shock profile
    # Severe systemic infection context: Hydration depletion (0.85), Elevated sepsis WBC (16,500 uL)
    sepsis_tracker = SepsisRedoxSimulationEngine(baseline_hydration=0.85, wbc_count_uL=16500.0)

    # Setup step 2: Define your data file path location target relative to your execution directory
    # Points straight to your target repository repository data path schema structure
    target_data_filepath = "src/data/parasite_enzymes.json"

    # NOTE: For local verification running before you clone/pull your json data tree, 
    # the script creates a mock local mirror if the file isn't instantly detected.
    if not os.path.exists("src/data"):
        os.makedirs("src/data")
    if not os.path.exists(target_data_filepath):
        sample_db = {
            "enzymes": [
                {"name": "hyaluronidase_v1", "class": "mmp_protease", "base_activity_uM_sec": 15.0, "target_substrate": "Bone-Lattice-Collagen-Helices"},
                {"name": "phospholipase_c", "class": "phospholipase", "base_activity_uM_sec": 28.5, "target_substrate": "Epithelial-Cell-Lipid-Borders"},
                {"name": "elastase_delta", "class": "protease", "base_activity_uM_sec": 8.0, "target_substrate": "Tendon-Cartilage-Matrices"}
            ]
        }
        with open(target_data_filepath, "w") as f:
            json.dump(sample_db, f, indent=2)

    # Setup step 3: Launch the pipeline execution map
    try:
        pipeline = JSONDataMappingPipeline(target_json_filename=target_data_filepath)
        master_run_logs = pipeline.execute_sepsis_tracking_run(engine_instance=sepsis_tracker, exposure_seconds=15)
        print(f"\n [EXECUTION SUCCESS]: Pipeline loops completed. Master data mapping array logged.")
    except Exception as error_msg:
        print(f"\n Pipeline processing aborted: {error_msg}")
