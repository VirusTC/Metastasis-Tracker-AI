import math
import unittest

class MetabolicAndContractilityBridgeEngine:
    def __init__(self, total_blood_volume_L: float, baseline_hco3_mEq_L: float = 24.0):
        """
        Engine module balancing bicarbonate chemical neutralizations 
        and hypercalcemic myocardial contraction force profiles.
        """
        self.v_blood = total_blood_volume_L
        self.hco3 = baseline_hco3_mEq_L # Clinical normal: 22 - 26 mEq/L
        self.pka = 6.10
        self.f_baseline_newtons = 5.0 # Reference baseline ventricular contraction force

    def calculate_bicarbonate_buffering(self, lactic_acid_influx_mmol_L: float, current_pco2_mmHg: float) -> dict:
        """
        Models the chemical buffer balance neutralizing proton loads to protect systemic pH.
        """
        pco2 = max(10.0, current_pco2_mmHg)
        
        # Stoichiometric 1:1 depletion of bicarbonate ions by accumulating hydrogen protons
        self.hco3 -= lactic_acid_influx_mmol_L
        self.hco3 = max(1.0, self.hco3) # Prevent chemical collapse beneath absolute structural bounds
        
        # Apply Henderson-Hasselbalch equation: pH = 6.1 + log10(HCO3 / (0.03 * pCO2))
        alpha_solubility = 0.03
        calculated_ph = self.pka + math.log10(self.hco3 / (alpha_solubility * pco2))
        
        return {
            "residual_bicarbonate_mEq_L": round(self.hco3, 2),
            "current_environmental_pco2_mmHg": pco2,
            "calculated_buffered_plasma_ph": round(calculated_ph, 3),
            "acidosis_state": "METABOLIC_ACIDOSIS_CRISIS" if calculated_ph < 7.35 else "COMPENSATED_BUFFER_ZONE"
        }

    def calculate_myocardial_force_scaling(self, serum_calcium_mg_dL: float) -> dict:
        """
        Calculates inotropic force amplification and calcium rigor lusitropy drops.
        """
        ca = max(0.1, serum_calcium_mg_dL)
        
        # Hill equation scaling parameters for Troponin-C binding kinematics
        km_myo = 9.5
        hill_n = 2.2
        
        inotropic_multiplier = math.pow(ca, hill_n) / (math.pow(ca, hill_n) + math.pow(km_myo, hill_n))
        # Normalize multiplier against healthy baseline serum calcium levels (~9.5 mg/dL)
        normalized_inotropy = inotropic_multiplier / 0.50 
        
        # Sarcoplasmic reticulum overload relaxation failure (Calcium Rigor) modeling
        # Lusitropy degrades non-linearly if concentrations cross 14.0 mg/dL
        beta_rigor = 0.04
        ca_excess = max(0.0, ca - 14.0)
        lusitropy_factor = max(0.1, 1.0 - beta_rigor * (ca_excess ** 2))
        
        # Net operational force = Baseline * Inotropy * Lusitropy
        final_force_newtons = self.f_baseline_newtons * normalized_inotropy * lusitropy_factor

        return {
            "serum_calcium_input_mg_dL": round(ca, 2),
            "isolated_inotropic_scaling_factor": round(normalized_inotropy, 3),
            "diastolic_lusitropy_efficiency": round(lusitropy_factor, 3),
            "net_myocardial_contraction_force_newtons": round(final_force_newtons, 3),
            "mechanical_cardiac_state": "CALCIUM_RIGOR_CONTRACTURE" if lusitropy_factor < 0.7 else ("HYPERDYNAMIC_INOTROPY" if ca > 11.5 else "NORMAL_CONTRACTILITY")
        }


# =====================================================================
# PIPELINE STABILITY SYSTEM VERIFICATIONS
# =====================================================================
class TestMetabolicCardiacBridge(unittest.TestCase):
    def test_bicarbonate_depletion_mechanics(self):
        engine = MetabolicAndContractilityBridgeEngine(total_blood_volume_L=5.0, baseline_hco3_mEq_L=24.0)
        report = engine.calculate_bicarbonate_buffering(lactic_acid_influx_mmol_L=5.0, current_pco2_mmHg=40.0)
        self.assertLess(report["residual_bicarbonate_mEq_L"], 24.0)
        self.assertLess(report["calculated_buffered_plasma_ph"], 7.41)

    def test_calcium_rigor_inversion(self):
        engine = MetabolicAndContractilityBridgeEngine(total_blood_volume_L=5.0)
        # Verify that extreme hypercalcemia (18.0 mg/dL) causes a contracture force drop compared to mild elevation
        mild_calcemia = engine.calculate_myocardial_force_scaling(serum_calcium_mg_dL=12.0)
        extreme_calcemia = engine.calculate_myocardial_force_scaling(serum_calcium_mg_dL=18.0)
        
        self.assertEqual(extreme_calcemia["mechanical_cardiac_state"], "CALCIUM_RIGOR_CONTRACTURE")
        self.assertLess(extreme_calcemia["net_myocardial_contraction_force_newtons"], mild_calcemia["net_myocardial_contraction_force_newtons"])

if __name__ == "__main__":
    unittest.main()
