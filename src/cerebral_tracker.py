import math

class CerebralTransportTracker:
    def __init__(self, patient_metrics: dict, target_particle_diameter_um: float):
        """
        Extended Tracker Module compatible with the Metastasis-Tracker-AI platform.
        Tracks, routes, and logs entry probabilities directly into the brain matrix.
        """
        self.metrics = patient_metrics
        self.d_particle = target_particle_diameter_um
        self.chi = patient_metrics.get("hydration_level", 1.0)
        
        # Pull baseline spatial scale constants from core anatomy engine properties
        self.spinal_length_cm = 0.35 * patient_metrics.get("height_cm", 175.0)
        self.wbc_pool = patient_metrics.get("wbc_count_uL", 6500.0)

    def track_arterial_route_extravasation(self, cerebral_generation_node: dict) -> dict:
        """
        Tracks Route A: Determines if a traveling particle can survive microvascular 
        shear fields and breach the Blood-Brain Barrier (BBB) tight junctions.
        """
        v_local = cerebral_generation_node.get("velocity_m_s", 0.15)
        mu_local = cerebral_generation_node.get("viscosity_Pa_s", 0.0035)
        local_ph = cerebral_generation_node.get("local_ph", 7.40)
        
        # Calculate localized wall shear rate to determine endothelial lining strain
        r_vessel = cerebral_generation_node.get("radius_m", 4.5e-6)
        shear_rate = (4.0 * v_local) / r_vessel if r_vessel > 0 else 150.0
        
        # Permeability scaling: Acidosis or dehydration weakens endothelial seals
        acid_deviation = max(0.0, 7.40 - local_ph)
        barrier_weakening_factor = 1.0 + (3.5 * acid_deviation)
        
        # Sub-micron entities exhibit a tiny baseline passive permeability coefficient (cm/s)
        if self.d_particle  0.1 else "BARRIER CONFINEMENT SECURE"
        }

    def track_batsons_plexus_shunt(self, intra_abdominal_pressure_mmHg: float, initial_load_count: int) -> dict:
        """
        Tracks Route B: Evaluates if pelvic pressure switches the tracking array 
        from systemic venous loops into the valveless spinal venous columns.
        """
        # Critical abdominal pressure override threshold (e.g. coughing or intense straining context)
        pressure_threshold = 25.0
        
        if intra_abdominal_pressure_mmHg > pressure_threshold:
            # Overriding pressure reverses normal downward tracking vectors
            shunt_efficiency = 0.08 * (intra_abdominal_pressure_mmHg / pressure_threshold)
            shunt_efficiency = min(0.90, shunt_efficiency)
            
            # Compute retrograde velocity vector along the spine
            v_retrograde_m_s = 0.012 * (intra_abdominal_pressure_mmHg / pressure_threshold)
            time_of_flight_s = (self.spinal_length_cm / 100.0) / v_retrograde_m_s
            
            successfully_routed_cells = int(initial_load_count * shunt_efficiency)
        else:
            shunt_efficiency = 0.0
            v_retrograde_m_s = 0.0
            time_of_flight_s = float('inf')
            successfully_routed_cells = 0

        return {
            "pathway_identity": "Route B: Axial Valveless Shunt (Batson's Plexus)",
            "shunt_activation_status": "ACTIVE / REVERSED ADVECTION" if shunt_efficiency > 0 else "INACTIVE / LOCKED",
            "retrograde_velocity_m_s": round(v_retrograde_m_s, 4),
            "spinal_column_transit_time_seconds": round(time_of_flight_s, 2) if shunt_efficiency > 0 else "Infinity",
            "cells_successfully_translocated_to_dural_sinuses": successfully_routed_cells
        }

    def track_spinal_csf_drift(self, initial_load_count: int) -> dict:
        """
        Tracks Route C: Processes passive long-term migration parameters 
        along the continuous subarachnoid cerebrospinal fluid column.
        """
        # CSF bulk flow velocity is steady but exceptionally slow
        v_csf_m_s = (0.35 / 1e6) / 60.0 * self.chi
        time_to_cranium_hours = ((self.spinal_length_cm / 100.0) / v_csf_m_s) / 3600.0
        
        # Immunological clearing factor inside the subarachnoid space (WBC cytotoxicity)
        immune_survival_rate = math.exp(-0.00002 * self.wbc_pool * time_to_cranium_hours)
        surviving_seeded_cells = int(initial_load_count * immune_survival_rate)

        return {
            "pathway_identity": "Route C: Ventricular-Spinal Subarachnoid Fluid Column",
            "bulk_fluid_drift_velocity_m_s": v_csf_flow_m_s := v_csf_m_s,
            "lumbar_to_cranial_transit_duration_hours": round(time_to_cranium_hours, 1),
            "immunological_survival_fraction_percent": round(immune_survival_rate * 100.0, 2),
            "cells_surviving_to_reach_ventricles": surviving_seeded_cells
        }

    def track_glymphatic_sinus_gate(self, paranasal_load_count: int) -> dict:
        """
        Tracks Route D: Models the physical sieve gate separating the nasal 
        mucosa layer from the perivascular channels of the cribriform matrix.
        """
        # Absolute structural mesh boundary limit
        cribriform_pore_limit_um = 2.0
        
        if self.d_particle  Extravasation Breach Prob: {report_a['extravasation_breach_probability_percent']}% | Status: {report_a['tracking_state_status' if 'tracking_state_status' in report_a else 'tracking_status']}")
    
    # Track Route B (Simulating high coughing stress of 40 mmHg)
    report_b = tracker_a.track_batsons_plexus_shunt(intra_abdominal_pressure_mmHg=40.0, initial_load_count=sub_micron_load)
    print(f" [{report_b['pathway_identity'].upper()}]:")
    print(f"  -> Status: {report_b['shunt_activation_status']} | Shunted Yield: {report_b['cells_successfully_translocated_to_dural_sinuses']:,} nodes")
    
    # Track Route C
    report_c = tracker_a.track_spinal_csf_drift(initial_load_count=sub_micron_load)
    print(f" [{report_c['pathway_identity'].upper()}]:")
    print(f"  -> Passive Transit Flight: {report_c['lumbar_to_cranial_transit_duration_hours']} hours | Surviving Yield: {report_c['cells_surviving_to_reach_ventricles']:,} nodes")
    
    # Track Route D
    report_d = tracker_a.track_glymphatic_sinus_gate(paranasal_load_count=sub_micron_load)
    print(f" [{report_d['pathway_identity'].upper()}]:")
    print(f"  -> Mechanical Sieve Resolution: {report_d['gating_resolution']} | Seeding Yield: {report_d['cells_colonizing_brain_interstitium']:,} nodes\n")

    # Trace a macro-particle (50 microns) load tracking through the same nodes
    print(f"--- INITIALIZING MACROSCOPIC TRACKER POOL (Size: 50.0 um | Input Load: {sub_micron_load:,} nodes) ---")
    tracker_b = CerebralTransportTracker(patient_metrics=mock_patient, target_particle_diameter_um=50.0)
    
    macro_report_a = tracker_b.track_arterial_route_extravasation(mock_cerebral_capillary)

    macro_report_d = tracker_b.track_glymphatic_sinus_gate(paranasal_load_count=sub_micron_load)
print(f" [ARTERIAL LOOP]: Extravasation Probability: {macro_report_a['extravasation_breach_probability_percent']}% ({macro_report_a['tracking_status']})")
print(f" [GLYMPHATIC GATE]: Mechanical Resolution: {macro_report_d['gating_resolution']}")

--

### 3. Repository Integration Flow

This tracking suite links cleanly into your master execution models:
1. **The State Fetcher:** The loop queries the baseline patient parameters (`height_cm`, `weight_kg`, `hydration_level`) to establish length vectors and fluid capacities.
2. **The Dynamic Switch:** When executing your pathfinding tracking loop, if an elevated pressure value occurs (e.g. `intra_abdominal_pressure_mmHg > 25`), the simulation switches nodes dynamically, updating the tracking arrays to log Route B translocation loops.
3. **The Yield Logger:** The resulting output dictionary integers (`cells_colonizing_brain_interstitium`, `cells_surviving_to_reach_ventricles`, and `cells_successfully_translocated_to_dural_sinuses`) plug directly back into the secondary organ-seeding matrices of your platform to map terminal brain colonization values.
