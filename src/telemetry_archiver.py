import os
import zipfile
from datetime import datetime

class TelemetryDataArchiver:
    def __init__(self, target_directory: str = "tests", archive_directory: str = "archive"):
        """
        Manages file cleanup and ZIP compression for historical .medbin telemetry data logs.
        """
        self.target_dir = target_directory
        self.archive_dir = archive_directory

    def compress_historical_medbin_logs(self) -> str:
        """
        Scans, compresses, and archives present .medbin streams to optimize storage footprints.
        """
        if not os.path.exists(self.target_dir):
            print(f"[-] Cleanup aborted: Target directory path missing at {self.target_dir}")
            return ""

        # Scan folder for target binary telemetry files
        files_to_compress = [f for f in os.listdir(self.target_dir) if f.endswith(".medbin")]
        if not files_to_compress:
            print("[*] Storage optimization complete: No loose .medbin files detected.")
            return ""

        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

        # Generate unique timestamped archive file identity naming conventions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"telemetry_history_bak_{timestamp}.zip"
        archive_filepath = os.path.join(self.archive_dir, archive_filename)

        print("=========================================================================")
        print(f"LAUCHING DISK HYGIENE SYSTEM: ARCHIVING {len(files_to_compress)} LOG DATASETS")
        print("=========================================================================")

        with zipfile.ZipFile(archive_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_compress:
                source_path = os.path.join(self.target_dir, file)
                # Pack file into the zip compression envelope container
                zipf.write(source_path, file)
                print(f" -> Compressed and packed: {file}")
                # Remove loose uncompressed file to release active storage blocks
                os.remove(source_path)

        print("-------------------------------------------------------------------------")
        print(f"[+] Archive package successfully generated at: {archive_filepath}")
        print("=========================================================================\n")
        return archive_filepath

if __name__ == "__main__":
    # Create fake binary logs to verify archiving loop mechanics
    if not os.path.exists("tests"):
        os.makedirs("tests")
    with open("tests/stale_run_data_01.medbin", "wb") as f: f.write(b"MEDB_MOCK_DATA")
    with open("tests/stale_run_data_02.medbin", "wb") as f: f.write(b"MEDB_MOCK_DATA")

    archiver = TelemetryDataArchiver()
    archiver.compress_historical_medbin_logs()
