import unittest
import os
import shutil
from src.metabolic_telemetry_core import MedicalTelemetryBinaryLogger
from src.graphics_matrix_mapper import GraphicsMatrixMapper

class TestEndToEndTelemetryGraphicsPipeline(unittest.TestCase):
    def setUp(self):
        """Sets up isolated testing environments and outputs."""
        self.test_dir = "tests/sandbox_run"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        self.bin_path = os.path.join(self.test_dir, "pipeline_test.medbin")
        self.chart_path = os.path.join(self.test_dir, "pipeline_chart.png")
        
        # Instantiate core software engines
        self.logger = MedicalTelemetryBinaryLogger(self.bin_path)
        self.mapper = GraphicsMatrixMapper(self.bin_path, self.chart_path)

    def tearDown(self):
        """Cleans up temporary directory paths and file outputs."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_pipeline_integration_flow(self):
        """
        INTEGRATION CHECK: Validates complete serialization-to-visualization loop.
        Ensures binary serialization formats cleanly match graphic parsing scopes.
        """
        # Step 1: Serialize a mock 5-second dynamic recovery dataset matrix
        print("\n[STEP 1]: Writing packed tracking arrays to binary storage...")
        for t in range(1, 6):
            self.logger.log_patient_record(
                timestep=t, patient_id_numeric=8804,
                ph=7.35 + (t * 0.01), hco3=18.0 + (t * 0.5),
                ca=13.5 - (t * 0.3), force=4.2 + (t * 0.2),
                ca_eff=0.65 + (t * 0.05), pco2=48.0 - (t * 1.5)
            )
            
        # Verify file existence on disk and check boundary sizes
        self.assertTrue(os.path.exists(self.bin_path))
        file_size = os.path.getsize(self.bin_path)
        # Expected size: 4 bytes (header) + 5 steps * 36 bytes = 184 bytes total
        self.assertEqual(file_size, 184, f"Mismatched size allocation found: {file_size} bytes")
        print(f" -> Binary file verified successfully at size: {file_size} bytes.")

        # Step 2: Pass binary output straight to the graphics matrix engine
        print("[STEP 2]: Executing graphics matrix engine parser loop...")
        render_success = self.mapper.parse_and_plot_history()
        
        # Assertions confirming both modules pass simultaneous runtime checks
        self.assertTrue(render_success, "Graphics engine failed to decode target binary file.")
        self.assertTrue(os.path.exists(self.chart_path), "Graphics engine completed execution but failed to output image file.")
        print(f" -> Integration verified. Visual chart rendered successfully at: {self.chart_path}")

if __name__ == "__main__":
    unittest.main()
