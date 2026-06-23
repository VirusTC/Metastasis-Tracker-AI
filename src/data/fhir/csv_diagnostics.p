import os
import csv
import yaml
from datetime import datetime, timedelta

class CSVDiagnosticsAndRetentionEngine:
    def __init__(self, csv_filepath: str = "src/data/fhir/hemostasis_summary.csv", config_yaml_path: str = "tests/fhir_retention_rules.yaml"):
        """
        Automated data hygiene and structural outlier diagnostic checking engine.
        """
        self.csv_path = csv_filepath
        self.config_path = config_yaml_path
        self.policies = self._load_retention_yaml()

    def _load_retention_yaml(self) -> dict:
        if not os.path.exists(self.config_path):
            return {"retention_policies": {"max_log_age_days": 14, "alert_outlier_threshold_platelets": 100000.0}}
        with open(self.config_path, "r") as stream:
            return yaml.safe_load(stream)

    def enforce_log_cleanup_retention(self, log_directory: str = "src/data/fhir/logs"):
        """
        Parses YAML configuration rules to dynamically clean up old JSON files.
        """
        max_days = self.policies.get("retention_policies", {}).get("max_log_age_days", 14)
        if not os.path.exists(log_directory):
            return
            
        now = datetime.now()
        purged_count = 0
        
        for file in os.listdir(log_directory):
            if file.endswith(".json"):
                filepath = os.path.join(log_directory, file)
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # Check if file age breaches the retention boundary limit
                if now - file_modified_time > timedelta(days=max_days):
                    os.remove(filepath)
                    purged_count += 1
        if purged_count > 0:
            print(f"[+] Data Hygiene: Purged {purged_count} loose raw files exceeding {max_days}-day limit.")

    def execute_spreadsheet_anomaly_check(self) -> bool:
        """
        Scans compiled spreadsheets and verifies that values match physiological normal boundaries.
        Returns False if parsing anomalies or critical structural errors infect data columns.
        """
        if not os.path.exists(self.csv_path):
            print(f"[-] Diagnostic Check Aborted: Missing source sheet asset at {self.csv_path}")
            return False

        critical_plt_floor = self.policies.get("retention_policies", {}).get("alert_outlier_threshold_platelets", 100000.0)
        row_count = 0
        anomaly_detected = False

        print("\n" + "="*85)
        print(f" LAUNCHING DIAGNOSTIC SPREADSHEET PROFILER :: SCANNING {os.path.basename(self.csv_path)}")
        print("="*85)

        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_count += 1
                try:
                    # Parse and extract string variables into typing floats
                    platelets = float(row["PLATELET_COUNT"])
                    inhibition = float(row["HEPARIN_INHIBITION"])
                    pid = row["PATIENT_ID"]
                    
                    # Statistical outlier assertion gates
                    if platelets < critical_plt_floor:
                        print(f" ⚠️ [ANOMALY DETECTED]: Patient {pid} flags critical Thrombocytopenia: {platelets} cells/uL")
                        anomaly_detected = True
                    if not (0.0 <= inhibition <= 1.0):
                        print(f" ⚠️ [PARSING ANOMALY]: Out-of-bounds drug factor: Patient {pid} -> {inhibition}")
                        anomaly_detected = True
                        
                except (ValueError, KeyError) as err:
                    print(f" ❌ [CRITICAL CORRUPTION]: Row {row_count} contains invalid schema formatting structures: {err}")
                    anomaly_detected = True

        print("-"*85)
        print(f" [SCAN COMPLETE]: Profiled Rows: {row_count} | Parsing Anomalies Flagged: {anomaly_detected}")
        print("="*85 + "\n")
        
        # Invert bool to pass clean return statuses to CI runners (True = Pass, False = Anomaly Found)
        return not anomaly_detected

if __name__ == "__main__":
    # Generate mock validation data profiles to test verification mechanics
    if not os.path.exists("tests"): os.makedirs("tests")
    if not os.path.exists("src/data/fhir"): os.makedirs("src/data/fhir")
    
    # 1. Instantiate YAML settings mock target
    with open("tests/fhir_retention_rules.yaml", "w") as f:
        f.write("retention_policies:\n  max_log_age_days: 0\n  alert_outlier_threshold_platelets: 50000.0\n")
        
    # 2. Instantiate a mock compiled CSV file tracking clean rows vs an anomalous record row
    with open("src/data/fhir/hemostasis_summary.csv", "w") as f:
        f.write("TIMESTAMP,PATIENT_ID,PLATELET_COUNT,HEPARIN_INHIBITION\n")
        f.write("2026-06-23T14:50:00Z,pat-01,250000.0,0.85\n")
        f.write("2026-06-23T14:51:00Z,pat-02,12000.0,0.90\n") # Critical outlier
        f.write("2026-06-23T14:52:00Z,pat-03,CORRUPT_STR,9.99\n") # Schema structural corruption
        
    diagnostician = CSVDiagnosticsAndRetentionEngine()
    diagnostician.enforce_log_cleanup_retention()
    is_clean = list_records_passed_check = diagnostician.execute_spreadsheet_anomaly_check()
