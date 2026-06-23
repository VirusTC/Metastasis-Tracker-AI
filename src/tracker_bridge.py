import math

class TrackerBiomassOrchestrator:
    def __init__(self, biomass_engine, population_engine, protein_config):
        """
        Coordinates path tracking location inputs with bioenergetic growth and breeding matrices.
        """
        self.biomass_core = biomass_engine        # Instance of PycnogonidBiomassEngine
        self.population_core = population_engine  # Instance of PycnogonidPopulationEngine
        self.protein_matrix = protein_config      # Data parsed from target_proteins.json

    def process_tracker_location_step(self, location_id, local_env_context, delta_time):
        """
        Called continuously by tracking modules (e.g., cerebral_tracker.py) during execution loops.
        """
        # 1. Look up the localized protein composition matching the current tracking node
        protein_profile = self.protein_matrix.get("marine_protein_profiles", {})
        
        # Determine local substrate availability mapped to this specific destination
        # Defaulting to a baseline structural protein if the specific location key is unmapped
        target_substrate = "mesogleal_collagen_type_i"
        if "cerebral" in location_id or "brain" in location_id:
            target_substrate = "actinoporin_complex" # High-affinity signature mapping
            
        substrate_data = protein_profile.get(target_substrate, {})
        substrate_density = substrate_data.get("structural_density_mg_mm3", 0.10)

        # 2. Compute current structural condition factor (Thick vs Skinny)
        # Main simulation logic scales condition factor based on ongoing nutrient satisfaction
        current_cf = 1.0
        if self.biomass_core.accumulated_protein_vol > 5.0:
            current_cf = 1.3  # Transitions to a 'thick' morphology profile
        elif self.biomass_core.accumulated_protein_vol < 0.2:
            current_cf = 0.7  # Contracts to a 'skinny' morphology profile

        # 3. Execute the pre-oral digestion calculations for this step
        # Base conversion velocity (Vmax) simulated from substrate matching
        mock_v_max = 5.8e-6
        raw_liq_rate = (mock_v_max * substrate_density) / (0.012 * (1.0 + substrate_density) + substrate_density)
        
        # Feed the output back into the live metabolic reserve pool
        updated_reserves = self.biomass_core.process_nutrient_tick(
            dynamic_liquefaction_rate=raw_liq_rate,
            delta_time=delta_time,
            condition_factor=current_cf
        )

        # 4. Evaluate Gonopore Activation Conditions
        # Check if the accumulated protein volume permits an automatic reproductive replication wave
        replication_report = self.biomass_core.calculate_replication_yield(condition_factor=current_cf)
        egg_output = replication_report.get("eggs_extruded_via_gonopores", 0)

        # 5. Inject Yield Data into the Lefkovitch Population Tensor if output is achieved
        if egg_output > 0:
            print(f"⚡ [ACTIVATION] Target conditions met at node [{location_id}].")
            print(f"   Extruding {egg_output} units via gonopores based on {target_substrate} absorption matrix.")
            
            # Construct a single step timeline vector matching current local parameters
            current_timeline = [{
                "temperature": local_env_context.get("temperature", 14.0),
                "turbulence": local_env_context.get("turbulence", 0.0),
                "ph": local_env_context.get("ph", 8.1)
            }]
            
            # Initialize the population stage vector with the newly generated egg/larval output
            initial_stages = [float(egg_output), 0.0, 0.0, 0.0]
            
            # Project the generation wave forward through the population engine matrix
            population_history = self.population_core.run_projection(
                initial_population=initial_stages,
                time_steps=1,
                env_timeline=current_timeline
            )
            return {
                "status": "REPRODUCTION_CYCLING",
                "larval_pool_generation": population_history[:, -1].tolist(),
                "protein_reserves_remaining": updated_reserves
            }

        return {
            "status": "FORAGING_FEEDING",
            "protein_reserves_remaining": updated_reserves
        }
