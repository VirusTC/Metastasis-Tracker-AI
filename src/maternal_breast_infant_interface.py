import math

class MaternalInfantInterfaceEngine:
    def __init__(self, maternal_hydration: float, infant_hydration: float):
        """
        Initializes the biophysical fluid interface network between maternal
        mammary systems and infant upper conducting respiratory zones.
        """
        self.chi_mat = max(0.5, min(1.5, maternal_hydration))
        self.chi_inf = max(0.5, min(1.5, infant_hydration))
        
        # Microvascular milk viscosity calculation (Pascal-seconds)
        # Viscosity spikes if maternal hydration falls (hemoconcentration correlation)
        self.mu_milk = 0.0020 * (1.0 / (self.chi_mat ** 0.4))
        
        # Microscopic terminal ductal constraints
        self.max_duct_orifice_diameter_mm = 0.5

    def calculate_interface_fluid_dynamics(self, maternal_sinus_pressure_mmHg: float, infant_vacuum_mmHg: float) -> dict:
        """
        Solves the pressure-driven advection velocity profile running across 
        the interface boundaries during a transient feeding loop cycle.
        """
        # Ensure pressure vectors conform to normal somatic ranges
        p_mat = max(5.0, min(30.0, maternal_sinus_pressure_mmHg))
        p_inf = min(-10.0, max(-200.0, infant_vacuum_mmHg)) # Must be a vacuum (negative)
        
        # Total pressure differential across the nipple barrier interface (mmHg to Pascals)
        delta_p_mmHg = p_mat - p_inf
        delta_p_pascals = delta_p_mmHg * 133.322
        
        # Single duct terminal line dimensions (meters)
        r_duct = (self.max_duct_orifice_diameter_mm / 2.0) * 1e-3
        l_duct = 0.015 # 1.5 cm terminal channel line length
        
        # Poiseuille equation for fluid advection speed inside the channel
        v_fluid_m_s = (delta_p_pascals * (r_duct ** 2)) / (8.0 * self.mu_milk * l_duct)

        return {
            "pressure_differential_mmHg": round(delta_p_mmHg, 1),
            "dynamic_milk_viscosity_Pa_s": round(self.mu_milk, 5),
            "outward_fluid_advection_velocity_m_s": round(v_fluid_m_s, 3),
            "duct_orifice_size_exclusion_limit_microns": self.max_duct_orifice_diameter_mm * 1000.0
        }

    def evaluate_particle_retrograde_ingress(self, particle_diameter_um: float, particle_propulsion_m_s: float, fluid_dynamics: dict) -> dict:
        """
        Evaluates the mathematical possibility of reverse transport crossing 
        the interface boundary against the active outward fluid current.
        """
        v_milk = fluid_dynamics["outward_fluid_advection_velocity_m_s"]
        d_limit_um = fluid_dynamics["duct_orifice_size_exclusion_limit_microns"]
        
        # Criterion 1: Geometrical filtering test
        size_exclusion_active = particle_diameter_um > d_limit_um
        
        # Criterion 2: Hydrodynamic velocity vector balance test
        # To travel backward, the item must swim faster than the fluid velocity output
        hydrodynamic_block_active = particle_propulsion_m_s <= v_milk
        
        if size_exclusion_active or hydrodynamic_block_active:
            successful_ingress = False
            if size_exclusion_active:
                failure_mode = "Physical Size Exclusion (Exceeds 500um Orifice Matrix)"
            else:
                failure_mode = "Hydrodynamic Washout (Swept into Infant Pharyngeal Sink)"
        else:
            successful_ingress = True
            failure_mode = "None - Ingress Vector Feasible"

        return {
            "target_particle_diameter_microns": particle_diameter_um,
            "autonomous_propulsion_velocity_m_s": particle_propulsion_m_s,
            "size_exclusion_gate_triggered": size_exclusion_active,
            "hydrodynamic_washout_triggered": hydrodynamic_block_active,
            "net_retrograde_ingress_allowed": successful_ingress,
            "terminal_structural_resolution": failure_mode
        }

# =====================================================================
# Pipeline Network Verification Sandbox
# =====================================================================
if __name__ == "__main__":
    # Instantiate interface tracking configuration layer
    interface = MaternalInfantInterfaceEngine(maternal_hydration=1.0, infant_hydration=1.0)
    
    print("=========================================================================")
    print("MATERNAL-INFANT INTERFACE FLUID TRANSPORT MATRIX LOGS")
    print("=========================================================================\n")
    
    # 1. Compute dynamic fluid flow velocities during an active suckling cycle
    # Maternal positive pressure = +20 mmHg, Infant suction vacuum = -80 mmHg
    flow_profile = interface.calculate_interface_fluid_dynamics(maternal_sinus_pressure_mmHg=20.0, infant_vacuum_mmHg=-80.0)
    print("--- 1. PRESSURE GRADIENT HYDRODYNAMICS ---")
    print(f" Total Active Interface Delta P: {flow_profile['pressure_differential_mmHg']} mmHg")
    print(f" Outward Fluid Jet Flow Velocity: {flow_profile['outward_fluid_advection_velocity_m_s']} m/s")
    print(f" Microscopic Duct Filter Ceiling: {flow_profile['duct_orifice_size_exclusion_limit_microns']} microns\n")
    
    # 2. Test particle kinematics against the calculated fluid barriers
    # Test item: A 1200-micron macro-particle attempting low-velocity movement
    macro_particle = interface.evaluate_particle_retrograde_ingress(
        particle_diameter_um=1200.0, particle_propulsion_m_s=0.01, fluid_dynamics=flow_profile
    )
    print("--- 2. SCENARIO A: MACROSCOPIC INTERCEPT ENTRY ATTEMPT ---")
    print(f" Net Retrograde Ingress Status:  {macro_particle['net_retrograde_ingress_allowed']}")
    print(f" Terminal Extraction Failure:    {macro_particle['terminal_structural_resolution']}\n")

    # Test item: A microscopic 50-micron particle attempting movement against the jet stream
    micro_particle = interface.evaluate_particle_retrograde_ingress(
        particle_diameter_um=50.0, particle_propulsion_m_s=0.02, fluid_dynamics=flow_profile
    )
    print("--- 3. SCENARIO B: MICROSCOPIC INTERCEPT ENTRY ATTEMPT ---")
    print(f" Net Retrograde Ingress Status:  {micro_particle['net_retrograde_ingress_allowed']}")
    print(f" Terminal Extraction Failure:    {micro_particle['terminal_structural_resolution']}")
