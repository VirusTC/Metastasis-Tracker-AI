import math
import os
import yaml
import unittest

class FibrinolysisSimulationEngine:
    def __init__(self, initial_clot_area_um2: float, baseline_plasminogen_uM: float = 2.0):
        """
        Models the enzymatic degradation kinetics of fibrin clots by plasmin over time.
        """
        self.a_clot_m2 = initial_clot_area_um2 * 1e-12
        self.plasminogen = baseline_plasminogen_uM
        self.plasmin = 0.0
        
        # Kinetic constants for enzymatic loop execution
        self.v_max_tpa = 0.05
        self.km_tpa = 0.8
        self.lambda_antiplasmin = 0.012
        self.v_max_lytic = 2.5e-14  # m^2 per uM per second
        self.km_fibrin_m2 = 1.0e-12

    def simulate_clot_dissolution_step(self, t_pa_activation_index: float, local_ph: float, dt_sec: float = 1.0) -> dict:
        """
        Advances the state matrix by one time increment, solving plasmin conversion
        and corresponding effective clot area reduction.
        """
        # 1. Solve Plasmin conversion differential equation
        eta_tpa = max(0.0, t_pa_activation_index)
        d_plasmin = (eta_tpa * (self.v_max_tpa * self.plasminogen) / (self.km_tpa + self.plasminogen)) - (self.lambda_antiplasmin * self.plasmin)
        self.plasmin += d_plasmin * dt_sec
        self.plasmin = max(0.0, self.plasmin)

        # 2. Apply microenvironmental pH modulation
        eta_ph = 1.0 if local_ph >= 7.35 else max(0.1, 1.0 - 4.0 * (7.35 - local_ph))

        # 3. Calculate Fibrinolysis: Orifice Area reduction math
        if self.a_clot_m2 > 0:
            lytic_rate = (self.v_max_lytic * self.plasmin * self.a_clot_m2) / (self.km_fibrin_m2 + self.a_clot_m2) * eta_ph
            self.a_clot_m2 -= lytic_rate * dt_sec
            self.a_clot_m2 = max(0.0, self.a_clot_m2)
        else:
            lytic_rate = 0.0

        return {
            "current_plasmin_uM": round(self.plasmin, 4),
            "remaining_clot_area_um2": round(self.a_clot_m2 * 1e12, 2),
            "instantaneous_lysis_velocity_um2_s": round(lytic_rate * 1e12, 4),
            "vessel_occlusion_cleared": self.a_clot_m2 <= 1e-15
        }


# =====================================================================
# CI/CD SCHEMA ENFORCEMENT & INTEGRATION TESTS
# =====================================================================
class TestYamlSchemaAndFibrinolysis(unittest.TestCase):
    def test_yaml_config_schema_compliance(self):
        """
        VERIFICATION: Automatically loads and validates target YAML files 
        to verify that required parameter keys exist and remain within data limits.
        """
        target_yaml = "tests/voxel_settings.yaml"
        self.assertTrue(os.path.exists(target_yaml), f"Critical File Missing: {target_yaml}")
        
        with open(target_yaml, "r") as stream:
            config = yaml.safe_load(stream)
            
        # Assert schema keys exist structural branches
        self.assertIn("view_parameters", config, "Schema Violation: Missing 'view_parameters' root key.")
        params = config["view_parameters"]
        
        required_keys = ["default_elevation", "total_rotation_steps", "animation_fps"]
        for key in required_keys:
            self.assertIn(key, params, f"Schema Violation: Missing expected parameter key: {key}")
            
        # Assert data typing and safe numerical limits bounds
        self.assertIsInstance(params["default_elevation"], (int, float))
        self.assertTrue(0.0 <= params["default_elevation"] <= 90.0, "Boundary Breach: Elevation angle out of range.")
        self.assertTrue(4 <= params["total_rotation_steps"] <= 120, "Boundary Breach: Rotation steps outside stable caps.")

    def test_fibrinolysis_acid_suppression(self):
        """VERIFICATION: Confirms that severe localized acidosis restricts enzymatic lysis speed."""
        # Baseline check under healthy physiologic conditions (pH 7.40)
        engine_healthy = FibrinolysisSimulationEngine(initial_clot_area_um2=500.0)
        step_healthy = engine_healthy.simulate_clot_dissolution_step(t_pa_activation_index=1.0, local_ph=7.40)
        
        # Sepsis/Acid crisis checkpoint (pH 6.90)
        engine_acidic = FibrinolysisSimulationEngine(initial_clot_area_um2=500.0)
        step_acidic = engine_acidic.simulate_clot_dissolution_step(t_pa_activation_index=1.0, local_ph=6.90)
        
        self.assertGreater(step_healthy["instantaneous_lysis_velocity_um2_s"], step_acidic["instantaneous_lysis_velocity_um2_s"])

if __name__ == "__main__":
    unittest.main()
