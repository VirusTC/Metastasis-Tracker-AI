import math

class DirectRectalEntryModel:
    def __init__(self, object_max_width_mm: float, object_driving_force_mmHg: float):
        """
        Models the physical entry mechanics, survival boundaries, and reflex clearance
        of an object entering directly into the terminal rectal vault.
        """
        self.obj_width = object_max_width_mm
        self.obj_force = object_driving_force_mmHg
        self.resting_sphincter_pressure_mmHg = 65.0 # Average adult resting tone

    def evaluate_mechanical_entry(self) -> dict:
        """
        Calculates whether the object can physically breach the high-pressure anal canal.
        """
        # Mechanical force comparison
        breach_successful = self.obj_force > self.resting_sphincter_pressure_mmHg
        
        return {
            "anal_sphincter_resting_pressure_mmHg": self.resting_sphincter_pressure_mmHg,
            "object_exerted_driving_force_mmHg": self.obj_force,
            "mechanical_entry_allowed": breach_successful,
            "status": "Blocked by Sphincter Muscular Tone" if not breach_successful else "Sphincter Overcome / Entry Achieved"
        }

    def simulate_internal_survival_window(self, hydration_level: float) -> dict:
        """
        Calculates the oxygen depletion and osmotic survival timeline of an organism inside the lumen.
        """
        # Dissolved oxygen availability inside the rectal vault stool matrix is effectively zero
        luminal_oxygen_partial_pressure_mmHg = 0.0
        
        # Survival half-life (in minutes) under absolute anoxia and osmotic desiccation
        survival_half_life_min = 8.5 * hydration_level
        
        # An external marine organism reaches zero viability rapidly in anaerobic tissue environments
        max_viability_duration_minutes = survival_half_life_min * 3.0

        return {
            "internal_oxygen_status": "ABSOLUTE ANOXIA (HYPOXIC CRISIS)",
            "osmotic_dehydration_strain": "CRITICAL HYPEROSMOLAL STRESS",
            "maximum_organism_survival_window_minutes": round(max_viability_duration_minutes, 2),
            "viable_colonization_possible": False
        }

    def calculate_expulsion_reflex(self) -> dict:
        """
        Models the involuntary neuro-muscular defecation reflex triggered by a foreign mass.
        """
        # The presence of a solid object stretches rectal wall mechanoreceptors
        # This triggers the rectoanal inhibitory reflex (RAIR) and the defecation reflex
        rectal_distension_volume_cm3 = math.pi * ((self.obj_width / 20.0) ** 2) * 5.0
        
        # When distension volume crosses 15-20 cm3, the urge to evacuate becomes mandatory
        reflex_trigger_active = rectal_distension_volume_cm3 > 15.0
        
        return {
            "calculated_rectal_distension_cm3": round(rectal_distension_volume_cm3, 2),
            "mechanoreceptor_activation_status": "CRITICAL" if reflex_trigger_active else "MODERATE",
            "involuntary_defecation_reflex_triggered": True, # Mandated by foreign body presence
            "projected_clearance_timeline_hours": 0.25 if reflex_trigger_active else 2.0,
            "final_fate": "EXCRETED / MECHANICAL EXPULSION VIA DEFECATION"
        }

# =====================================================================
# Verification Execution Sandbox
# =====================================================================
if __name__ == "__main__":
    # Model an aggressive 10mm object trying to force entry with a low driving force (5 mmHg)
    low_force_intruder = DirectRectalEntryModel(object_max_width_mm=10.0, object_driving_force_mmHg=5.0)
    
    print("=========================================================================")
    print("DIRECT ANRECTAL ENTRY AND EXPULSION SIMULATION LOGS")
    print("=========================================================================\n")
    
    report_a = low_force_intruder.evaluate_mechanical_entry()
    print("--- SCENARIO A: PASSIVE OR SELF-DIRECTED ENTRY ATTEMPT ---")
    print(f" Barrier Pressure:   {report_a['anal_sphincter_resting_pressure_mmHg']} mmHg")
    print(f" Intruder Force:     {report_a['object_exerted_driving_force_mmHg']} mmHg")
    print(f" Entry Status:       {report_a['mechanical_entry_allowed']} ({report_a['status']})\n")

    # Model a forced introduction scenario (e.g., mechanical insertion overriding the sphincter at 90 mmHg)
    forced_intruder = DirectRectalEntryModel(object_max_width_mm=25.0, object_driving_force_mmHg=90.0)
    report_b = forced_intruder.evaluate_mechanical_entry()
    
    print("--- SCENARIO B: MECHANICAL OVERRIDE INSERTION ---")
    print(f" Entry Status:       {report_b['mechanical_entry_allowed']} ({report_b['status']})")
    
    if report_b['mechanical_entry_allowed']:
        survival = forced_intruder.simulate_internal_survival_window(hydration_level=1.0)
        expulsion = forced_intruder.calculate_expulsion_reflex()
        
        print(f"\n[LUMINAL CRISIS METRICS]:")
        print(f" - Atmospheric Environment:   {survival['internal_oxygen_status']}")
        print(f" - Osmotic Status:           {survival['osmotic_dehydration_strain']}")
        print(f" - Maximum Viability Window:  {survival['maximum_organism_survival_window_minutes']} minutes until total asphyxiation.")
        print(f" - Long-Term Host Viability:  {survival['viable_colonization_possible']}")
        
        print(f"\n[HOST CLEARANCE DYNAMICS]:")
        print(f" - Rectal Distension Metric:  {expulsion['calculated_rectal_distension_cm3']} cm³")
        print(f" - Defecation Reflex Vector:  {expulsion['involuntary_defecation_reflex_triggered']}")
        print(f" - Projected Clearance Time:  {expulsion['projected_clearance_timeline_hours']} hours or less")
        print(f" - Terminal System Endpoint:  {expulsion['final_fate']}")
