# Conceptual layout of the crawling loop updating the joint motors every frame:
target_velocity = math.sin(current_game_time * crawl_speed + leg_phase_offset) * max_swing_speed
physics_constraint.set_angular_velocity_target([target_velocity, 0, 0])
