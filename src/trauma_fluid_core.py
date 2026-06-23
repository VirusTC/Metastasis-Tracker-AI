import math
import unittest

class VascularHemorrhageDynamicsEngine:
    def __init__(self, tip_radius_microns: float, blood_density_kg_m3: float = 1060.0):
        """
        Initializes the dynamic fluid hemorrhage decay simulator.
        """
        self.r_tip_m = tip_radius_microns * 1e-6
        self.a_lesion_m2 = math.pi * (self.r_tip_m ** 2)
        self.rho = blood_density_kg_m3
        self.c_d = 0.62  # Standard sharp-edged orifice discharge coefficient

        # Baseline ultimate tensile strength conversions (Pascals)
        self.tissue_ceilings = {
            "capillary_vein": 1.1 * 1e6,
            "macro_artery":   2.8 * 1e6,
            "brain_neural":   0.03 * 1e6,
            "cortical_bone":  135.0 * 1e6
        }

    def simulate_active_bleeding_cascade(self, initial_p_vessel_mmHg: float, p_interstitial_mmHg: float, time_steps_sec: int) -> dict:
        """
        Models the dynamic bleeding volume rates cascading through a ruptured vessel 
        over a discrete timeline matrix based on pressure decays.
        """
        # Convert inputs from mmHg to Pascals (1 mmHg = 133.322 Pa)
        p_vessel_pa = initial_p_vessel_mmHg * 133.322
        p_int_pa = p_interstitial_mmHg * 133.322
        
        cumulative_volume_lost_mL = 0.0
        time_series_log = []
        
        # Exponential blood pressure drop scaling factor
        lambda_decay = 0.0015 

        for t in range(time_steps_sec):
            # Dynamic local blood pressure decay calculation
            current_p_pa = p_vessel_pa * math.exp(-lambda_decay * cumulative_volume_lost_mL)
            current_p_mmHg = current_p_pa / 133.322
            
            delta_p_pa = current_p_pa - p_int_pa
            
            if delta_p_pa <= 0:
                leak_rate_m3_s = 0.0
                current_p_mmHg = p_interstitial_mmHg
            else:
                # Torricelli fluid velocity mapping
                leak_rate_m3_s = self.c_d * self.a_lesion_m2 * math.sqrt((2.0 * delta_p_pa) / self.rho)
                
            # Convert m^3/s to mL/s (1 m^3 = 1,000,000 mL)
            leak_rate_mL_s = leak_rate_m3_s * 1e6
            cumulative_volume_lost_mL += leak_rate_mL_s
            
            time_series_log.append({
                "seconds_elapsed": t,
                "vessel_pressure_mmHg": round(current_p_mmHg, 2),
                "instantaneous_bleeding_rate_mL_s": round(leak_rate_mL_s, 4)
            })

        return {
            "orifice_lesion_area_um2": round(self.a_lesion_m2 * 1e12, 2),
            "total_cumulative_blood_loss_mL": round(cumulative_volume_lost_mL, 3),
            "dynamic_time_series": time_series_log
        }


# =====================================================================
# AUTOMATED UNIT TESTING SUITE
# =====================================================================
class TestTraumaMaterialAndFluidBoundaries(unittest.TestCase):
    def setUp(self):
        # Set up an intruder profile with a 5.0-micron sharp point apex
        self.engine = VascularHemorrhageDynamicsEngine(tip_radius_microns=5.0)

    def test_physiological_material_bounds(self):
        """
        VERIFICATION: Ensures ultimate tensile strengths are positive 
        and remain within known physiological boundary ceilings.
        """
        for tissue, strength in self.engine.tissue_ceilings.items():
            self.assertGreater(strength, 0, f"Error: {tissue} has non-positive strength.")
            # Cortical bone represents maximum somatic density cap (135 MPa)
            self.assertLessEqual(strength, 150.0 * 1e6, f"Error: {tissue} exceeds structural limits.")

    def test_hemorrhage_pressure_decay(self):
        """
        VERIFICATION: Assures bleeding rates drop deterministically 
        over time as internal vascular pressure decays.
        """
        report = self.engine.simulate_active_bleeding_cascade(
            initial_p_vessel_mmHg=100.0, p_interstitial_mmHg=5.0, time_steps_sec=10
        )
        timeline = report["dynamic_time_series"]
        
        # Bleeding rate at t=0 must be strictly greater than t=9 due to decay mechanics
        initial_rate = timeline[0]["instantaneous_bleeding_rate_mL_s"]
        terminal_rate = timeline[-1]["instantaneous_bleeding_rate_mL_s"]
        
        self.assertGreater(initial_rate, terminal_rate, "Error: Pressure decay cascade failure.")
        self.assertGreaterEqual(report["total_cumulative_blood_loss_mL"], 0.0)

if __name__ == "__main__":
    print("Executing Pipeline Diagnostic Assertions...")
    unittest.main()
