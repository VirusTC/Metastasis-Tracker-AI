import struct
import os
import sys

class MedbinTerminalParser:
    def __init__(self, medbin_filepath: str):
        """
        Parses and decodes high-density .medbin binary files, printing 
        structured data frames directly to the terminal console layout.
        """
        self.filepath = medbin_filepath

    def execute_console_stream(self):
        """
        Reads binary segments, verifies the structural validation header, 
        and decodes packed data structures into clean text rows.
        """
        if not os.path.exists(self.filepath):
            print(f"[-] Execution error: Source binary file missing at {self.filepath}")
            return False

        print("\n" + "="*95)
        print(f" METASTASIS-TRACKER-AI :: LIVE MEDBIN PARSER STREAM (File: {os.path.basename(self.filepath)})")
        print("="*95)
        
        # Table structural row header mapping
        print(f"| {'STEP':5} | {'PATIENT ID':10} | {'pH':5} | {'HCO3-':6} | {'Ca2+':5} | {'MYO-FORCE':9} | {'CA-EFF%':7} | {'pCO2':5} |")
        print("|" + "-"*7 + "|" + "-"*12 + "|" + "-"*7 + "|" + "-"*8 + "|" + "-"*7 + "|" + "-"*11 + "|" + "-"*9 + "|" + "-"*6 + "|")

        with open(self.filepath, "rb") as f:
            # Read and verify the 4-byte Magic Identity Header marker
            magic = f.read(4)
            if len(magic) < 4 or struct.unpack(">I", magic)[0] != 0x4D454442:
                print("[-] Fatal Format Error: Corrupt or unverified binary file header context.")
                return False

            count = 0
            # Read 36-byte packed data row blocks (Format: >IIfffffff)
            while True:
                chunk = f.read(36)
                if len(chunk) < 36:
                    break
                
                unpacked = struct.unpack(">IIfffffff", chunk)
                step = unpacked[0]
                pid = unpacked[1]
                ph = unpacked[2]
                hco3 = unpacked[3]
                ca = unpacked[4]
                force = unpacked[5]
                ca_eff = unpacked[6]
                pco2 = unpacked[7]

                # Print human-readable formatted string rows
                print(f"| {step:<5} | {pid:<10} | {ph:<5.2f} | {hco3:<6.1f} | {ca:<5.1f} | {force:<9.2f} | {ca_eff*100:<7.1f} | {pco2:<5.1f} |")
                count += 1

        print("="*95)
        print(f" [PARSING COMPLETED]: Total Extracted Log Lines: {count}")
        print("="*95 + "\n")
        return True

if __name__ == "__main__":
    # Self-contained validation helper
    sample_bin = "tests/diagnostic_telemetry.medbin"
    if os.path.exists(sample_bin):
        parser = MedbinTerminalParser(sample_bin)
        parser.execute_console_stream()
    else:
        # Create a transient binary file to demonstrate operational compliance
        if not os.path.exists("tests"): os.makedirs("tests")
        with open(sample_bin, "wb") as bf:
            bf.write(struct.pack(">I", 0x4D454442))
            bf.write(struct.pack(">IIfffffff", 1, 5005, 7.38, 22.5, 9.6, 5.1, 0.92, 42.0))
        parser = MedbinTerminalParser(sample_bin)
        parser.execute_console_stream()
