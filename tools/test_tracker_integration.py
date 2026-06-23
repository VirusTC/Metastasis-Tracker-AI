#!/usr/bin/env python3
import unittest
import os
import json
import sys

# Append src to path to ensure clean command-line discovery
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from biomass_scaler import PycnogonidBiomassEngine
from population_engine import PycnogonidPopulationEngine
from tracker_bridge import TrackerBiomassOrchestrator

class TestTrackerBioenergeticIntegration(unittest.TestCase):
    
    def setUp(self):
        """
        Initializes test components, directories, and mock tracking payload configurations.
        """
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.protein_path = os.path.join(self.base_dir, "src", "data", "target_proteins.json")
        self.thermal_path = os.path.join(self.base_dir, "src", "data", "pycnogonid_thermal_profiles.json")
        
        # Guard clause: Ensure configuration assets exist before running assertions
        if not os.path.exists(self.protein_path) or not os.path.exists(self.thermal_path):
            self.skipTest("Missing configuration data JSON fixtures inside src/data/")

        with open(self.protein_path, "r") as pf:
            self.protein_config = json.load(pf)
        with open(self.thermal_path, "r") as tf:
            self.thermal_config = json.load(tf)

        # Initialize the bioenergetic cores
        self.bio_core = PycnogonidBiomassEngine({
            "base_femur_length_mm": 8.0, 
            "base_leg_radius_mm": 0.5
        })
        
        species_key = "Pycnogonidae_shallow_profile"
        self.pop_config = {
            "breeding_matrix_config": self.thermal_config["pycnogonid_thermal_development_matrix"][species_key]
        }
        self.pop_core = PycnogonidPopulationEngine(self.pop_config)
        
        # Establish the data bridge
        self.orchestrator = TrackerBiomassOrchestrator(
            biomass_engine=self.bio_core,
            population_engine=self.pop_core,
            protein_config=self.protein_config
        )

    def test_tracker_pipeline_flow_and_reproduction_gate(self):
        """
        Asserts that moving through high-protein tracking nodes updates biomass 
        correctly and triggers the population matrix without throwing exceptions.
        """
        # Seed an optimal starting reserve to trigger activation bounds quickly
        self.bio_core.accumulated_protein_vol = 4.80
        
        mock_env = {"temperature": 14.0, "turbulence": 0.0, "ph": 8.1}
        target_node = "cerebral_capillary_bed_alpha"
        time_step = 2.0
        
        # First step: Foraging and nutrient absorption check
        report_1 = self.orchestrator.process_tracker_location_step(
            location_id=target_node,
            local_env_context=mock_env,
            delta_time=time_step
        )
        
        self.assertIn("status", report_1)
        self.assertIn("protein_reserves_remaining", report_1)
        self.assertGreater(report_1["protein_reserves_remaining"], 0.0)

        # Second step: Force nutrient saturation past the gonopore activation trigger limit
        self.bio_core.accumulated_protein_vol = 15.0
        
        report_2 = self.orchestrator.process_tracker_location_step(
            location_id=target_node,
            local_env_context=mock_env,
            delta_time=time_step
        )
        
        # Verify reproduction matrix successfully updates and populates stage-tensors
        self.assertEqual(report_2["status"], "REPRODUCTION_CYCLING")
        self.assertIn("larval_pool_generation", report_2)
        self.assertEqual(len(report_2["larval_pool_generation"]), 4) # Must return 4 vector stages [L, J, A, B]

if __name__ == "__main__":
    unittest.main()
