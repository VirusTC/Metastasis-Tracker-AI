import json
import gzip
import os
import hashlib
import numpy as np
from datetime import datetime, timezone

class JSONTransactionLogger:
    def __init__(self, target_directory: str = "src/data/logs"):
        """
        High-density structured JSON serialization engine featuring GZIP compression,
        cryptographic SHA-256 integrity verifications, and cohort analytical parsers.
        """
        self.output_dir = target_directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    def serialize_and_compress_log(self, step_records_list: list, patient_id: str) -> tuple:
        """
        Serializes and compresses telemetry arrays, appending an explicit 
        integrity hash token profile to secure data blocks from corruption.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"transaction_history_{patient_id}_{timestamp}.json.gz"
        full_path = os.path.join(self.output_dir, filename)

        payload = {
            "schema_version": "2026.2.2",
            "patient_id": patient_id,
            "transaction_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_records_packed": len(step_records_list),
            "telemetry_matrix": step_records_list
        }

        # 1. Compress string bytes to disk using GZIP standard
        json_string = json.dumps(payload, indent=2)
        json_bytes = json_string.encode('utf-8')
        
        with gzip.open(full_path, 'wb') as gzf:
            gzf.write(json_bytes)

        # 2. Generate a secure SHA-256 checksum from the final compressed artifact
        sha256_hash = hashlib.sha256()
        with open(full_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        checksum_token = sha256_hash.hexdigest()
        
        # Save structural token sidecar descriptor validation mapping file
        with open(full_path + ".sha256", "w") as sf:
            sf.write(checksum_token)

        print(f"[+] Transaction saved: {filename} (SHA-256: {checksum_token[:8]}...)")
        return full_path, checksum_token

    @staticmethod
    def read_compressed_json_log(filepath: str) -> dict:
        """Loads and unpacks a gzip compressed JSON transaction package."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Source file missing at: {filepath}")
        with gzip.open(filepath, 'rb') as gzf:
            return json.loads(gzf.read().decode('utf-8'))

    def verify_compressed_log_checksum(self, filepath: str) -> bool:
        """
        CI/CD CHECK: Re-computes SHA-256 hashes from target files and verifies 
        integrity matrices against stored sidecar checksum tokens.
        """
        token_path = filepath + ".sha256"
        if not os.path.exists(filepath) or not os.path.exists(token_path):
            return False

        # Read historical reference token validation properties
        with open(token_path, "r") as sf:
            stored_token = sf.read().strip()

        # Re-compute current hash matrix configuration parameters
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        current_token = sha256_hash.hexdigest()

        return current_token == stored_token

    def parse_multi_patient_cohort_statistics(self) -> dict:
        """
        Unpacks all available .json.gz transaction sheets inside the logs directory
        and compiles automated cohort descriptive statistical matrices.
        """
        files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".json.gz")]
        if not files:
            return {"status": "EMPTY_REGISTRY", "cohort_count": 0}

        global_ph_pool = []
        global_cbf_pool = []
        patient_counts = len(files)

        for file_path in files:
            # Bypass processing if the file has failed cryptographic validation
            if not self.verify_compressed_log_checksum(file_path):
                print(f"[-] Security Exclusion: Skipped corrupted file target: {file_path}")
                continue

            with gzip.open(file_path, 'rb') as gzf:
                data = json.load(gzf)
                matrix = data.get("telemetry_matrix", [])
                for row in matrix:
                    if "ph" in row: global_ph_pool.append(row["ph"])
                    if "cbf" in row: global_cbf_pool.append(row["cbf"])

        if not global_ph_pool:
            return {"status": "NO_EXTRACTABLE_METRICS", "cohort_count": patient_counts}

        # Calculate population vectors using standard numpy matrix tools
        return {
            "status": "METRICS_COMPILED_SUCCESSFULLY",
            "total_cohort_records_evaluated": patient_counts,
            "blood_ph_distribution": {
                "mean": float(np.mean(global_ph_pool)),
                "std_dev": float(np.std(global_ph_pool)),
                "min": float(np.min(global_ph_pool)),
                "max": float(np.max(global_ph_pool))
            },
            "coronary_blood_flow_distribution_mL_min": {
                "mean": float(np.mean(global_cbf_pool)),
                "min": float(np.min(global_cbf_pool)),
                "max": float(np.max(global_cbf_pool))
            }
        }
