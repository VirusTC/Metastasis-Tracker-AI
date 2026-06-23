import os
import yaml
from datetime import datetime, timedelta
from src.telemetry_archiver import TelemetryDataArchiver

class ArchiveConfigWrapper:
    def __init__(self, config_yaml_path: str = "tests/archive_settings.yaml"):
        """
        Wrapper script parsing YAML configuration rules to automate 
        customization profiles for the telemetry archival network.
        """
        self.config_path = config_yaml_path
        self.settings = self._load_yaml_config()

    def _load_yaml_config(self) -> dict:
        if not os.path.exists(self.config_path):
            # Fallback configuration default mapping if file missing
            return {
                "archive_policies": {
                    "retention_threshold_days": 7,
                    "compression_level": "DEFLATED",
                    "auto_cleanup_raw_medbin": True
                }
            }
        with open(self.config_path, "r") as stream:
            return yaml.safe_load(stream)

    def enforce_retention_and_archive(self, target_dir: str = "tests", archive_dir: str = "archive"):
        """
        Evaluates file tracking timestamps against configured dynamic retention bounds, 
        selectively pushing files into zipped archive packages.
        """
        policies = self.settings.get("archive_policies", {})
        retention_days = policies.get("retention_threshold_days", 7)
        auto_clean = policies.get("auto_cleanup_raw_medbin", True)

        if not os.path.exists(target_dir):
            return

        now = datetime.now()
        files = [f for f in os.listdir(target_dir) if f.endswith(".medbin")]
        execution_pool = []

        for file in files:
            filepath = os.path.join(target_dir, file)
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            # Boundary threshold check vector
            if now - file_modified_time >= timedelta(days=retention_days):
                execution_pool.append(file)

        if not execution_pool:
            print(f"[*] Archiver context: 0 files passed the {retention_days}-day retention boundary limit.")
            return

        # Execute optimization zipping loops using base archiver hooks
        archiver = TelemetryDataArchiver(target_directory=target_dir, archive_directory=archive_dir)
        archiver.compress_historical_medbin_logs()

if __name__ == "__main__":
    # Self-test loop instantiation setup wrapper
    if not os.path.exists("tests"): os.makedirs("tests")
    
    # Generate mock YAML rule config file target
    mock_yaml = """
    archive_policies:
      retention_threshold_days: 0  # 0 days forces immediate archiving for testing
      compression_level: "DEFLATED"
      auto_cleanup_raw_medbin: true
    """
    with open("tests/archive_settings.yaml", "w") as f: f.write(mock_yaml)
    
    wrapper = ArchiveConfigWrapper()
    wrapper.enforce_retention_and_archive()
