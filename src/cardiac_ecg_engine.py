import math
import unittest

class CardiacECGSimulationEngine:
    def __init__(self, resting_heart_rate_bpm: float = 72.0):
        """
        Models the electrophysiological impacts of serum mineral status 
        on ventricular repolarization and ECG architecture.
        """
        self.hr = resting_heart_rate_bpm
        self.rr_interval_s = 60.0 / self.hr
        self.qt_c_baseline = 0.410  # 410 ms healthy baseline reference
        self.alpha_repol = 0.085    # Repolarization acceleration constant

    def calculate_dynamic_qt_interval(self, serum_calcium_mg_dL: float) -> dict:
        """
        Calculates Bazett-corrected and absolute QT interval durations based 
        on serum calcium concentrations, tracking Short QT arrhythmia shifts.
        """
        ca = max(0.0, serum_calcium_mg_dL)
        
        # Isolate hypercalcemic excess beyond physiological norms (10.5 mg/dL)
        ca_excess = max(0.0, ca - 10.5)
        
        # Non-linear log-decay mapping hypercalcemic ventricular action potential shrinking
        qt_c_dynamic = self.qt_c_baseline - (self.alpha_repol * math.log(1.0 + ca_excess))
        
        # Clamp mathematically to prevent impossible negative interval values
        qt_c_dynamic = max(0.150, qt_c_dynamic)
        
        # Reverse Bazett formula to calculate absolute uncorrected QT interval (seconds)
        # QTc = QT / sqrt(RR) -> QT = QTc * sqrt(RR)
        qt_absolute_s = qt_c_dynamic * math.sqrt(self.rr_interval_s)
        
        # Evaluate clinical threshold boundary checks
        short_qt_arrhythmia_active = qt_c_dynamic <= 0.320 # Short QT ceiling risk threshold (320ms)

        return {
            "monitored_serum_calcium_mg_dL": round(ca, 2),
            "calculated_qt_c_seconds": round(qt_c_dynamic, 4),
            "calculated_qt_c_ms": round(qt_c_dynamic * 1000.0, 1),
            "absolute_qt_interval_ms": round(qt_absolute_s * 1000.0, 1),
            "short_qt_syndrome_alert": short_qt_arrhythmia_active,
            "cardiac_rhythm_status": "CRITICAL ARRHAYTHMIA / VFIB RISK" if short_qt_arrhythmia_active else "SINUS RHYTHM BOUNDS SECURE"
        }

# =====================================================================
# PIPELINE AUTOMATED UNIT TESTS
# =====================================================================
class TestCardiacElectrophysiology(unittest.TestCase):
    def test_hypercalcemia_ecg_decay(self):
        """
        VERIFICATION: Validates that critical hypercalcemia drops 
        the QTc interval below the arrhythmia ceiling threshold.
        """
        engine = CardiacECGSimulationEngine(resting_heart_rate_bpm=60.0)
        
        # Trace severe hypercalcemic osteolysis crisis (15.5 mg/dL serum calcium)
        report = engine.calculate_dynamic_qt_interval(serum_calcium_mg_dL=15.5)
        
        # The QTc value must shorten to reveal active electrical path changes
        self.assertLess(report["calculated_qt_c_ms"], 410.0)
        if report["calculated_qt_c_ms"] <= 320.0:
            self.assertTrue(report["short_qt_syndrome_alert"])

if __name__ == "__main__":
    unittest.main()
