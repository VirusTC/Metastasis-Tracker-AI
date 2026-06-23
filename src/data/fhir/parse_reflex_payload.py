import json
import os

class FHIRReflexPayloadParser:
    def __init__(self, fhir_json_path: str = "src/data/fhir/reflex_observation.json"):
        """
        Parses HL7 FHIR R4 Observation JSON payloads to output clean, 
        human-readable diagnostic summaries directly to the terminal shell.
        """
        self.path = fhir_json_path

    def execute_terminal_summary(self) -> bool:
        if not os.path.exists(self.path):
            print(f"[-] Parsing aborted: Target FHIR payload missing at {self.path}")
            return False

        with open(self.path, "r") as f:
            try:
                payload = json.load(f)
            except json.JSONDecodeError as err:
                print(f"[-] Format Error: Invalid JSON structural framing: {err}")
                return False

        # Extract core properties safely matching standard schema paths
        obs_id = payload.get("id", "UNKNOWN_OBS_ID")
        timestamp = payload.get("effectiveDateTime", "N/A")
        patient_ref = payload.get("subject", {}).get("reference", "Patient/UNKNOWN")
        reflex_status_outcome = payload.get("valueString", "TRIGGER_FAILED")
        
        # Parse text identifiers inside loinc structures
        code_text = payload.get("code", {}).get("text", "Respiratory Observation")

        components = payload.get("component", [])
        air_velocity = 0.0
        trigger_probability = 0.0

        for comp in components:
            display_name = comp.get("code", {}).get("coding", [{}])[0].get("display", "")
            val = comp.get("valueQuantity", {}).get("value", 0.0)
            if "Velocity" in display_name:
                air_velocity = val
            elif "Probability" in display_name:
                trigger_probability = val

        print("\n" + "="*80)
        print(f" 📋 [FHIR DIAGNOSTIC METRIC REPORT]: {obs_id.upper()}")
        print("="*80)
        print(f"  -> TARGET CLINICAL SUBJECT  : {patient_ref}")
        print(f"  -> TRANSACTION TIMESTAMP     : {timestamp}")
        print(f"  -> SOURCE DIAGNOSTIC CODE    : LOINC 9279-1 ({code_text})")
        print(f"  " + "-"*70)
        print(f"  -> REFLEX RESPONSE STATUS    : {reflex_status_outcome}")
        print(f"  -> RECEPTOR ACTIVATION PROB  : {trigger_probability * 100.0:.2f}%")
        print(f"  -> EXPULSION AIR JET VELOCITY: {air_velocity:.2f} m/s")
        
        # Calculate approximate velocity miles-per-hour translation mapping variables
        mph_conversion = air_velocity * 2.23694
        if air_velocity > 0:
            print(f"  -> FLUID DYNAMICS PEAK INTENSITY : {mph_conversion:.1f} mph (EXPLOSIVE CASCADING JET)")
        else:
            print(f"  -> FLUID DYNAMICS PEAK INTENSITY : 0.0 mph (STAGNANT CLEARANCE CAP)")
            
        print("="*80 + "\n")
        return True

if __name__ == "__main__":
    parser = FHIRReflexPayloadParser()
    parser.execute_terminal_summary()
