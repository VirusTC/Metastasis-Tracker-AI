import os
import json
from src.data.logs.json_transaction_logger import JSONTransactionLogger

class WikiMarkdownTableGenerator:
    def __init__(self, log_directory: str = "src/data/logs", output_md_path: str = "docs/cohort_analytics_report.md"):
        """
        Ingests parsed cohort statistical dictionaries and compiles them
        into a clear, structured Markdown data table formatting layout.
        """
        self.logger = JSONTransactionLogger(log_directory)
        self.output_md = output_md_path

    def compile_stats_to_markdown_table(self) -> bool:
        """
        Triggers cohort calculations, extracts target keys, and writes 
        the flattened text blocks straight into the wiki index page assets.
        """
        stats = self.logger.parse_multi_patient_cohort_statistics()
        
        if stats.get("status") != "METRICS_COMPILED_SUCCESSFULLY":
            print(f"[-] Table compilation aborted: Reason: {stats.get('status')}")
            return False

        ph_data = stats["blood_ph_distribution"]
        cbf_data = stats["coronary_blood_flow_distribution_mL_min"]

        # Build Markdown file text blocks
        md_lines = [
            "# Systemic Cohort Telemetry Descriptive Statistical Summary",
            f"**Report Compilation Timestamp (UTC)**: {os.popen('date -u').read().strip()}",
            f"**Total Validated Cohort Records Evaluated**: {stats['total_cohort_records_evaluated']} patient records",
            "",
            "## 📊 Population Distribution Matrix Table",
            "",
            "| PHYSIOLOGICAL METRIC PROPERTY | MEAN VECTOR | STANDARD DEV | MINIMUM BOUND | MAXIMUM BOUND |",
            "| :--- | :--- | :--- | :--- | :--- |",
            f"| Systemic Arterial Blood pH    | {ph_data['mean']:.3f} | {ph_data['std_dev']:.4f} | {ph_data['min']:.2f} | {ph_data['max']:.2f} |",
            f"| Coronary Blood Flow (mL/min)  | {cbf_data['mean']:.1f} | N/A | {cbf_data['min']:.1f} | {cbf_data['max']:.1f} |",
            "",
            "***",
            "### 🛠️ Execution Pipeline Footnote",
            "- Loose or corrupted datasets failing SHA-256 validation criteria were safely excluded from this table.",
            "- Output compiled automatically via `WikiMarkdownTableGenerator` engine routines."
        ]

        # Verify target documentation folder pathways are present
        dir_name = os.path.dirname(self.output_md)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(self.output_md, "w") as md_file:
            md_file.write("\n".join(md_lines) + "\n")

        print(f"[+] Wiki documentation markdown table generated successfully at: {self.output_md}")
        return True

if __name__ == "__main__":
    generator = WikiMarkdownTableGenerator("tests/scratch_logs", "docs/cohort_analytics_report.md")
    # Execute a test compile pass leveraging sandbox logger directory setups
    generator.compile_stats_to_markdown_table()
