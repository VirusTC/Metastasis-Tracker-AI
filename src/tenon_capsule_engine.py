import math
import unittest

class TenonsCapsuleDynamicsEngine:
    def __init__(self, height_cm: float, weight_kg: float, hydration_level: float):
        """
        Initializes the dynamic Tenon's Capsule (Fascia bulbi) Engine.
        Fascial thickness and tensile thresholds adjust to global patient parameters.
        """
        self.chi = max(0.5, min(1.5, hydration_level))
        self.bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
        
        # Base mechanical parameters
        self.h_baseline_mm = 0.50       # Average resting thickness of the fascia
        self.sigma_base_pa = 2.4 * 1e6   # ~2.4 MPa baseline ultimate tensile strength
        
        # Surface area of one eye globe proxy based on BSA scaling (~18.0 cm2 baseline)
        self.a_capsule_m2 = (18.0 * (self.bsa / 1.73)) * 1e-4

    def calculate_capsular_mechanics(self, current_iop_mmHg: float, movement_strain: float) -> dict:
        """
        Computes dynamic thickness expansion, trans-capsular fluid flux,
        and the structural puncture threshold of the Fascia bulbi.
        """
        iop_pa = current_iop_mmHg * 133.322
        p_orbit_pa = 5.0 * 133.322  # Resting retrobulbar orbital tissue pressure
        
        # 1. Dynamic Thickness equation coupled to hydration profile
        h_dynamic = self.h_baseline_mm * math.pow(self.chi, 0.4)
        
        # 2. Fluid Flux: Starling trans-capsular filtration calculation
        k_trans = 1.2e-11  # Filtration coefficient matrix constant
        delta_p = iop_pa - p_orbit_pa
        
        if delta_p <= 0:
            flux_m3_s = 0.0
        else:
            flux_m3_s = k_trans * self.a_capsule_m2 * delta_p * self.chi
            
        # 3. Dynamic Tensile Strength: Wolff's soft-tissue adaptation
        # Local structural cross-linking tightens under mechanical strain forces
        strain_factor = max(1.0, movement_strain)
        sigma_uts_dynamic = self.sigma_base_pa * (1.0 + 0.15 * (strain_factor - 1.0))

        return {
            "dynamic_capsule_thickness_mm": round(h_dynamic, 3),
            "trans_capsular_fluid_flux_mL_min": round(flux_m3_s * 1e6 * 60.0, 5),
            "dynamic_tensile_strength_threshold_MPa": round(sigma_uts_dynamic / 1e6, 2),
            "interstitial_fluid_pooling_risk": "HIGH_CHEMOSIS_RISK" if self.chi > 1.2 else "NORMAL_RETENTION_ZONE"
        }

    def evaluate_capsule_puncture_risk(self, contact_force_newtons: float, tip_radius_microns: float, capsular_report: dict) -> dict:
        """
        Checks for mechanical boundary puncture failure at the fascial wall substrate.
        """
        r_m = tip_radius_microns * 1e-6
        a_tip_m2 = math.pi * (r_m ** 2)
        
        # Point Stress Formula: Sigma = Force / Area
        applied_stress_pa = contact_force_newtons / a_tip_m2 if a_tip_m2 > 0 else 0.0
        sigma_uts_pa = capsular_report["dynamic_tensile_strength_threshold_MPa"] * 1e6
        
        rupture_active = applied_stress_pa > sigma_uts_pa

        return {
            "applied_point_stress_MPa": round(applied_stress_pa / 1e6, 2),
            "fascial_wall_rupture_status": "CAPSULAR_PERFORATION_CRISIS" if rupture_active else "SECURE_ELASTIC_CONTAINMENT",
            "compartment_leakage_destination": "Retrobulbar Orbital Space Infiltration" if rupture_active else "None"
        }

# =====================================================================
# SYSTEM AUTOMATION VALIDATION SUITE
# =====================================================================
class TestTenonCapsuleKinetics(unittest.TestCase):
    def test_hydration_and_strain_adaptation(self):
        """VERIFICATION: Confirms tissue parameters scale deterministically with inputs."""
        engine_hydrated = TenonsCapsuleDynamicsEngine(height_cm=175.0, weight_kg=72.0, hydration_level=1.3)
        engine_dehydrated = TenonsCapsuleDynamicsEngine(height_cm=175.0, weight_kg=72.0, hydration_level=0.8)
        
        report_h = engine_hydrated.calculate_capsular_mechanics(current_iop_mmHg=22.0, movement_strain=1.0)
        report_d = engine_dehydrated.calculate_capsular_mechanics(current_iop_mmHg=12.0, movement_strain=1.0)
        
        # Hyperhydration must expand fascial thickness and pool fluid
        self.assertGreater(report_h["dynamic_capsule_thickness_mm"], report_d["dynamic_capsule_thickness_mm"])
        self.assertEqual(report_h["interstitial_fluid_pooling_risk"], "HIGH_CHEMOSIS_RISK")

if __name__ == "__main__":
    unittest.main()
