import json
import os
import time
from datetime import datetime, timezone

# Optional dependency fallback handling matching repository protocols
try:
    from jsonschema import validate as validate_json_schema
    JSON_SCHEMA_AVAILABLE = True
except ImportError:
    JSON_SCHEMA_AVAILABLE = False

class FHIRPipelineAutomationEngine:
    def __init__(self, output_directory: str = "src/data/fhir/logs"):
        """
        Manages real-time timestamped FHIR JSON payload generation and 
        executes schema structural compliance rule validation checks.
        """
        self.output_dir = output_directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Baseline minimal FHIR R4 Bundle validation schema template rule structure
        self.base_fhir_schema = {
            "type": "object",
            "required": ["resourceType", "id", "type", "entry"],
            "properties": {
                "resourceType": {"type": "string", "enum": ["Bundle"]},
                "id": {"type": "string"},
                "type": {"type": "string", "enum": ["transaction", "batch", "collection", "history"]},
                "entry": {"type": "array"}
            }
        }

    def generate_timestamped_payload(self, patient_id: str, platelets: float, heparin_inhibition: float) -> str:
        """
        Auto-generates separate, timestamped individual payload entries 
        during real-time tracking loops.
        """
        # Generate ISO-8601 compliant UTC timestamp string
        now = datetime.now(timezone.utc)
        timestamp_str = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]
        iso_timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        filename = f"payload_{patient_id}_{timestamp_str}.json"
        full_path = os.path.join(self.output_dir, filename)

        fhir_bundle = {
            "resourceType": "Bundle",
            "id": f"bundle-{patient_id}-{timestamp_str}",
            "type": "transaction",
            "entry": [
                {
                    "fullUrl": f"urn:uuid:patient-{patient_id}",
                    "resource": {
                        "resourceType": "Patient",
                        "id": patient_id,
                        "active": True
                    },
                    "request": {"method": "POST", "url": "Patient"}
                },
                {
                    "fullUrl": "urn:uuid:observation-coag",
                    "resource": {
                        "resourceType": "Observation",
                        "id": f"obs-{patient_id}",
                        "status": "final",
                        "code": {
                            "coding": [{"system": "http://loinc.org", "code": "26515-7", "display": "Platelets count"}],
                            "text": "Platelet Concentration Count"
                        },
                        "subject": {"reference": f"urn:uuid:patient-{patient_id}"},
                        "effectiveDateTime": iso_timestamp,
                        "valueQuantity": {"value": platelets, "unit": "cells/uL"},
                        "component": [
                            {
                                "code": {"coding": [{"system": "http://identifiers/codes", "code": "ANTICOAG_IDX"}]},
                                "valueQuantity": {"value": heparin_inhibition, "unit": "fraction"}
                            }
                        ]
                    },
                    "request": {"method": "POST", "url": "Observation"}
                }
            ]
        }

        # Validate structure against rules prior to disk commit operation
        if JSON_SCHEMA_AVAILABLE:
            try:
                validate_json_schema(instance=fhir_bundle, schema=self.base_fhir_schema)
            except Exception as schema_err:
                print(f"[-] Schema Compliance Breach: Validation aborted. Error: {schema_err}")
                raise

        with open(full_path, "w") as out_file:
            json.dump(fhir_bundle, out_file, indent=2)

        return full_path

    def compile_logs_to_tabular_csv(self, output_csv_path: str = "src/data/fhir/hemostasis_summary.csv"):
        """
        Parses all generated timeline individual JSON logs inside the directory tree,
        extracts target metrics, and flattens them into a flat tabular CSV file.
        """
        files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".json")]
        if not files:
            print("[-] CSV Compilation aborted: Zero log files found inside path.")
            return

        # Initialize CSV structure header row
        csv_rows = ["TIMESTAMP,PATIENT_ID,PLATELET_COUNT,HEPARIN_INHIBITION"]

        for file_path in files:
            with open(file_path, "r") as json_data:
                try:
                    data = json.load(json_data)
                    # Extract variables safely from structured array loops
                    obs_res = data["entry"][1]["resource"]
                    ts = obs_res["effectiveDateTime"]
                    pid = obs_res["subject"]["reference"].split("-")[-1]
                    plt = obs_res["valueQuantity"]["value"]
                    heparin = obs_res["component"][0]["valueQuantity"]["value"]
                    
                    csv_rows.append(f"{ts},{pid},{plt},{heparin}")
                except Exception:
                    continue # Skip structural drift files cleanly

        with open(output_csv_path, "w") as csv_file:
            csv_file.write("\n".join(csv_rows) + "\n")
        print(f"[+] Tabular configuration compiled successfully at: {output_csv_path}")

if __name__ == "__main__":
    engine = FHIRPipelineAutomationEngine()
    print("Simulating real-time timeline ingestion loops...")
    
    # Generate 3 sequential tracking states over tiny execution delays
    for i in range(3):
        p = engine.generate_timestamped_payload(patient_id="pat-04", platelets=240000.0 - (i*5000), heparin_inhibition=0.85)
        print(f" -> Log entry written: {os.path.basename(p)}")
        time.sleep(0.1)

    engine.compile_logs_to_tabular_csv()
