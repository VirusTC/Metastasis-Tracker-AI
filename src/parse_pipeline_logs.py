import os
import math
import unittest

try:
    import h5py
    H5PY_AVAILABLE = True
except ImportError:
    H5PY_AVAILABLE = False
    import json

class PipelineLogDiagnosticParser:
    def __init__(self, target_h5_path: str = "tests/pipeline_telemetry.h5"):
        self.path = target_h5_path
        self.expected_dataset = "time_series_log"

    def execute_diagnostic_scan(self) -> dict:
        """
        Unpacks simulation logs and checks real-time tracking variables
        against clinical coronary ischemia boundaries.
        """
        records = []
        if not H5PY_AVAILABLE:
            mock_json = self.path + ".mockjson"
            if os.path.exists(mock_json):
                with open(mock_json, "r") as f:
                    records = json.load(f)["data"]
        else:
            if os.path.exists(self.path):
                with h5py.File(self.path, "r") as h5f:
                    records = h5f[self.expected_dataset][:]

        print("\n" + "="*95)
        print(f" METASTASIS-TRACKER-AI :: CRITICAL PERFUSION LOG DIAGNOSTIC PARSER RUN")
        print("="*95)
        
        critical_ischemia_frames = 0
        total_frames = len(records)
        
        print(f"| {'STEP':4} | {'PLASMA pH':9} | {'COLLAPSE P':10} | {'DBP (mmHg)':10} | {'CORONARY FLOW':15} | {'MYO-STATE':20} |")
        print("|" + "-"*6 + "|" + "-"*11 + "|" + "-"*12 + "|" + "-"*12 + "|" + "-"*17 + "|" + "-"*22 + "|")

        for row in records:
            step = int(row[0])
            ph = row[1]
            p_collapse = row[5]
            
            # Formulate Diastolic Blood Pressure decay coupled to systemic collapse models
            # Mimics dropping systemic pressures under escalating septic shock
            dbp_calc = max(10.0, 80.0 - (step * 9.5)) 
            
            # Solve coronary perfusion kinematics: CPP = DBP - LVEDP (assume constant LVEDP=8mmHg)
            cpp = dbp_calc - 8.0
            cbf_basal = 250.0 # mL/min reference resting coronary flow
            
            if cpp >= 55.0:
                cbf_dynamic = cbf_basal
            elif 7.5 < cpp < 55.0:
                cbf_dynamic = cbf_basal * ((cpp - 7.5) / (55.0 - 7.5))
            else:
                cbf_dynamic = 0.0
                
            # Ischemia limit check: flow dropped below 35% of basal minimums
            is_ischemic = cbf_dynamic <= (0.35 * cbf_basal)
            if is_ischemic:
                critical_ischemia_frames += 1
                state_str = "CRITICAL_ISCHEMIA"
            else:
                state_str = "AUTO_REGULATED_STABLE"

            print(f"| {step:<4} | {ph:<9.2f} | {p_collapse:<12.1f} | {dbp_calc:<10.1f} | {cbf_dynamic:<15.2f} | {state_str:20} |")

        print("="*95)
        status_summary = "CRITICAL INSULT / ARREST RISK" if critical_ischemia_frames >= 3 else "PERFUSION SECURE"
        print(f" [PARSING OUTCOME]: {status_summary} (Ischemic Frames: {critical_ischemia_frames}/{total_frames})")
        print("="*95 + "\n")
        
        return {
            "total_frames_evaluated": total_frames,
            "ischemic_anomaly_count": critical_ischemia_frames,
            "system_arrest_risk_tripped": critical_ischemia_frames >= 3
        }

# =====================================================================
# CONTINUOUS INTEGRATION SCHEMA VERIFICATIONS
# =====================================================================
class TestCoronaryPerfusionParser(unittest.TestCase):
    def test_ischemia_diagnostic_trap(self):
        """VERIFICATION: Confirms parser catches and logs low-pressure shock anomalies."""
        parser = PipelineLogDiagnosticParser("tests/pipeline_telemetry.h5")
        # Ensure data is mock serialized to run verification loops cleanly
        if not H5PY_AVAILABLE:
            with open("tests/pipeline_telemetry.h5.mockjson", "w") as f:
                f.write('{"data": [[0,7.4,1,1,2,150],[1,7.3,1.2,0.9,7,550],[2,7.1,1.5,0.8,12,1200],[3,6.9,2.0,0.5,25,3100]]}')
        else:
            with h5py.File("tests/pipeline_telemetry.h5", "w") as h5f:
                h5f.create_dataset("time_series_log", data=[[0,7.4,1,1,2,150],[1,7.3,1.2,0.9,7,550],[2,7.1,1.5,0.8,12,1200],[3,6.9,2.0,0.5,25,3100]])
                
        metrics = parser.execute_diagnostic_scan()
        self.assertTrue(metrics["ischemic_anomaly_count"] > 0)

if __name__ == "__main__":
    unittest.main()
