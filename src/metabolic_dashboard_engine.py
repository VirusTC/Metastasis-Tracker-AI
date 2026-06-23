import math
import time
import os
import unittest

class AdvancedMetabolicKineticEngine:
    def __init__(self, hydration_level: float):
        self.chi = max(0.5, min(1.5, hydration_level))
        self.k_accel_base = 18500.0  # Reference CA velocity multiplier
        self.v_max_hydration = 1.25   # mmol/L/sec base enzymatic ceiling
        self.km_co2 = 12.0            # Michaelis constant for CO2 substrate (mmol/L)

    def calculate_ca_velocity_efficiency(self, current_ph: float, co2_mmol_L: float) -> dict:
        """
        Calculates non-linear enzyme denaturation limits and adjusted 
        carbonic anhydrase hydration velocities.
        """
        # Step 1: Compute conformation denaturation factor based on proton stress
        ph_mid = 6.80
        k_denat = 8.5
        
        # Logistic enzyme performance efficiency curve
        eta_ca = max(0.05, 1.0 / (1.0 + math.exp(-k_denat * (current_ph - ph_mid))))
        
        # Step 2: Apply Michaelis-Menten accelerated conversion velocity math
        effective_k_accel = self.k_accel_base * eta_ca * self.chi
        v_hyd = effective_k_accel * ((self.v_max_hydration * co2_mmol_L) / (self.km_co2 + co2_mmol_L))
        
        return {
            "enzyme_efficiency_coefficient": round(eta_ca, 3),
            "effective_catalytic_acceleration": round(effective_k_accel, 1),
            "instantaneous_hydration_velocity_mmol_L_s": round(v_hyd, 4),
            "catalytic_state": "OPTIMAL" if eta_ca > 0.85 else ("DENATURING_STRAIN" if eta_ca >= 0.3 else "CATALYTIC_COLLAPSE")
        }


class RealTimeCommandLineDashboard:
    @staticmethod
    def render_dashboard(cohort_profiles: list, current_timestep: int):
        """
        Renders a production-grade, ANSI-scannable real-time dashboard tracking 
        the system-wide biochemical states across multiple patient builds.
        """
        # Clear terminal screen dynamically for true real-time display loop properties
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*92)
        print(f" METASTASIS-TRACKER-AI :: METABOLIC & BIOENERGETIC ECOSYSTEM REAL-TIME DASHBOARD")
        print(f" Sim Timestep Tracking Frame: {current_timestep}s | Active Execution Context: Stable")
        print("="*92)
        
        # Dashboard Table Header Grid formatting
        header_template = f"| {'COHORT PATIENT ID':26} | {'pH':5} | {'HCO3-':6} | {'Ca2+':5} | {'MyoForce':8} | {'CA Eff%':8} | {'STATUS':20} |"
        print(header_template)
        print("|" + "-"*28 + "|" + "-"*7 + "|" + "-"*8 + "|" + "-"*7 + "|" + "-"*10 + "|" + "-"*10 + "|" + "-"*22 + "|")
        
        for patient in cohort_profiles:
            pid = patient["id"]
            ph = patient["ph"]
            hco3 = patient["hco3"]
            ca = patient["ca"]
            force = patient["force"]
            ca_eff = patient["ca_eff"]
            status = patient["status"]
            
            # Formulate layout string variables
            row_str = f"| {pid:26} | {ph:<5.2f} | {hco3:<6.1f} | {ca:<5.1f} | {force:<8.2f} | {ca_eff:<8.1f} | {status:20} |"
            print(row_str)
            
        print("="*92)
        print(" [KEY INDICATORS]: MyoForce: Newtons | Ca2+: mg/dL | HCO3-: mEq/L | CA Eff%: Catalyst Capacity")
        print("============================================================================================")


# =====================================================================
# INTEGRATION TESTING AND DEMONSTRATION RUNNER
# =====================================================================
class TestCarbonicAnhydraseKinetics(unittest.TestCase):
    def test_acid_denaturation_collapse(self):
        engine = AdvancedMetabolicKineticEngine(hydration_level=1.0)
        
        # Test optimal physiologic state vs extreme lactic acid septic crash
        optimal_run = engine.calculate_ca_velocity_efficiency(current_ph=7.41, co2_mmol_L=1.2)
        acidotic_run = engine.calculate_ca_velocity_efficiency(current_ph=6.45, co2_mmol_L=1.2)
        
        self.assertEqual(optimal_run["catalytic_state"], "OPTIMAL")
        self.assertEqual(acidotic_run["catalytic_state"], "CATALYTIC_COLLAPSE")
        self.assertLess(acidotic_run["enzyme_efficiency_coefficient"], optimal_run["enzyme_efficiency_coefficient"])

if __name__ == "__main__":
    # 1. Instantiate testing core loops to preserve code baseline health
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCarbonicAnhydraseKinetics)
    runner = unittest.TextTestRunner(verbosity=0)
    test_result = runner.run(suite)
    
    if test_result.wasSuccessful():
        # 2. If tests pass, execute the live dashboard real-time data stream step loop
        kinetic_calc = AdvancedMetabolicKineticEngine(hydration_level=1.0)
        
        # Configure initial raw conditions for 3 contrasting cohort profiles
        mock_cohorts = [
            {"id": "COHORT_01_HEALTHY_ATHLETE", "ph": 7.40, "hco3": 24.2, "ca": 9.5,  "force": 5.0,  "co2": 1.2, "status": "STABLE_PHYSIOLOGY"},
            {"id": "COHORT_02_SEVERE_SEPSIS",   "ph": 7.05, "hco3": 14.5, "ca": 14.8, "force": 6.8,  "co2": 2.8, "status": "CRITICAL_HYPERCALC"},
            {"id": "COHORT_03_CALCIUM_RIGOR",   "ph": 6.88, "hco3": 11.2, "ca": 18.2, "force": 1.2,  "co2": 3.5, "status": "MYOCARDIAL_RIGOR"}
        ]
        
        print("Launching dashboard telemetry stream loop...")
        time.sleep(1)
        
        # Simulate a real-time sequential 5-second matrix execution cascade
        for tick in range(1, 6):
            for patient in mock_cohorts:
                # Dynamic enzyme scaling update variables
                ca_metrics = kinetic_calc.calculate_ca_velocity_efficiency(patient["ph"], patient["co2"])
                patient["ca_eff"] = ca_metrics["enzyme_efficiency_coefficient"] * 100.0
                
                # Introduce subtle real-time state drift alterations over each slice iteration
                if patient["status"] == "CRITICAL_HYPERCALC":
                    patient["ph"] -= 0.02
                    patient["ca"] += 0.4
                elif patient["status"] == "MYOCARDIAL_RIGOR":
                    patient["hco3"] -= 0.3
                    patient["force"] = max(0.5, patient["force"] - 0.12)
            
            # Print state matrices to console terminal layout
            RealTimeCommandLineDashboard.render_dashboard(mock_cohorts, current_timestep=tick)
            time.sleep(1) # Exact 1-second interval refresh pause delay
