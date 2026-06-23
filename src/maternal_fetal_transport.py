import math

class MaternalFetalTransportEngine:
    def __init__(self, maternal_hydration: float, fetal_mass_kg: float):
        """
        Models the prenatal gestational transport network connecting maternal 
        organs to a developing fetal anatomy template.
        """
        self.chi_mat = max(0.5, min(1.5, maternal_hydration))
        self.fetal_mass = fetal_mass_kg
        
        # Fetal physiological baselines (scaled to gestational size)
        # Umbilical vein radius averages approx 2.5 mm near term
        self.r_umbilical_m = 0.0025 
        self.fetal_cardiac_output_L_min = 0.22 * self.fetal_mass # ~220 mL/min/kg baseline

        # Absolute structural gating limit of the placental syncytiotrophoblast barrier
        self.placental_pore_cutoff_microns = 1.0 

    def evaluate_placental_filtration_gate(self, particle_diameter_um: float) -> dict:
        """
        Applies mechanical size-exclusion sorting to check if a structural mass matrix 
        can cross the placental tissue barrier into the child's bloodstream.
        """
        is_excluded = particle_diameter_um > self.placental_pore_cutoff_microns
        
        return {
            "input_particle_diameter_microns": particle_diameter_um,
            "barrier_pore_ceiling_microns": self.placental_pore_cutoff_microns,
            "mechanical_crossing_allowed": not is_excluded,
            "gating_status": "BLOCKED / SIZE EXCLUSION" if is_excluded else "PASSAGE SCHEMATICALLY FEASIBLE"
        }

    def calculate_fetal_delivery_velocity(self) -> dict:
        """
        Solves the forward fluid advection velocity driving allowed micro-particles 
        along the umbilical vein toward the child's central organs.
        """
        # Convert fetal flow rate from Liters/minute to m^3/second
        q_fetal_m3_s = (self.fetal_cardiac_output_L_min / 1000.0) / 60.0
        
        # Umbilical vein cross-sectional flow area
        area_m2 = math.pi * (self.r_umbilical_m ** 2)
        
        # Advection speed profile: v = Q / A
        v_advection_m_s = q_fetal_m3_s / area_m2
        
        # Average umbilical cord length tracking parameter: 50 cm (0.50 meters)
        cord_length_m = 0.50
        time_of_flight_seconds = cord_length_m / v_advection_m_s

        return {
            "fetal_umbilical_flow_rate_L_min": round(self.fetal_cardiac_output_L_min, 3),
            "umbilical_vein_velocity_m_s": round(v_advection_m_s, 4),
            "transit_time_across_cord_seconds": round(time_of_flight_seconds, 2),
            "primary_fetal_delivery_sink": "Ductus Venosus -> Right Atrium -> Systemic Scaling Tree"
        }

    def execute_maternal_fetal_pipeline(self, particle_diameter_um: float) -> dict:
        """
        Runs the full structural mapping loop combining the filtration filter 
        and fluid transport timelines.
        """
        gate = self.evaluate_placental_filtration_gate(particle_diameter_um)
        
        if gate["mechanical_crossing_allowed"]:
            transit = self.calculate_fetal_delivery_velocity()
            resolution = f"Successful delivery to child via Umbilical Vein in {transit['transit_time_across_cord_seconds']}s"
        else:
            transit = {}
            resolution = "Transport aborted at Placental Wall: " + gate["gating_status"]

        return {
            "filtration_gate_metrics": gate,
            "hydrodynamic_transit_metrics": transit,
            "terminal_simulation_outcome": resolution
        }

# =====================================================================
# Operational Verification Pipeline Loop
# =====================================================================
if __name__ == "__main__":
    # Simulate a third-trimester fetal template context (Mass: 3.0 kg)
    pipeline = MaternalFetalTransportEngine(maternal_hydration=1.0, fetal_mass_kg=3.0)
    
    print("=========================================================================")
    print("MATERNAL-TO-CHILD GESTATIONAL TRANSIT SIMULATION LOGS")
    print("=========================================================================\n")
    
    # Test Node A: A macroscopic 15-micron fragment trying to navigate the vascular loop
    macro_test = pipeline.execute_maternal_fetal_pipeline(particle_diameter_um=15.0)
    print("--- SCENARIO A: MACROSCOPIC PARTICLE TRANSIT ---")
    print(f" Mechanical Gate Allowance: {macro_test['filtration_gate_metrics']['mechanical_crossing_allowed']}")
    print(f" Simulation Terminal Fate:  {macro_test['terminal_simulation_outcome']}\n")

    # Test Node B: A sub-micron 0.2-micron (200 nm) particle navigating the loop
    micro_test = pipeline.execute_maternal_fetal_pipeline(particle_diameter_um=0.2)
    print("--- SCENARIO B: SUB-MICRON PARTICULATE TRANSIT ---")
    print(f" Mechanical Gate Allowance: {micro_test['filtration_gate_metrics']['mechanical_crossing_allowed']}")
    print(f" Fluid Speed in Umbilical Core: {micro_test['hydrodynamic_transit_metrics']['umbilical_vein_velocity_m_s']} m/s")
    print(f" Cord Flight Vector Time:       {micro_test['hydrodynamic_transit_metrics']['transit_time_across_cord_seconds']} seconds")
    print(f" Child Distribution Target Sink: {micro_test['hydrodynamic_transit_metrics']['primary_fetal_delivery_sink']}")
    print(f" Simulation Terminal Fate:       {micro_test['terminal_simulation_outcome']}")
