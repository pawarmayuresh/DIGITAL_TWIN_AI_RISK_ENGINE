"""Earthquake Model — simulates seismic waves and structural damage."""

from typing import Dict, List
import math

from .base_disaster import BaseDisaster, DisasterEvent


class EarthquakeModel(BaseDisaster):
    """
    Earthquake disaster model.
    
    - Seismic waves propagate from epicenter outward
    - Larger radius (regional earthquake)
    - Intensity decreases with distance (seismic attenuation)
    - Peak occurs early, then subsides quickly
    - Causes damage to rigid structures (buildings, infrastructure)
    """

    INFRASTRUCTURE_IMPACT = {
        "power": 0.7,         # Transmission towers, substations
        "water": 0.8,         # Pipelines rupture
        "transport": 0.9,     # Bridges, tunnels, overpasses
        "healthcare": 0.85,   # Hospital structural damage
        "communication": 0.6,  # Cell towers, fiber
    }

    def __init__(self, event: DisasterEvent):
        """
        Initialize earthquake model.
        
        Args:
            event: DisasterEvent specification (severity = magnitude proxy)
        """
        super().__init__(event)
        self.peak_tick = int(event.duration_ticks * 0.2)  # Peak at 20% of duration
        self.affected_cells_snapshot: Dict[str, float] = {}

    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one tick of earthquake:
        1. Calculate current shaking intensity (peaks early)
        2. Apply damage to all cells based on distance and shaking
        3. Track which cells experience strong motion
        """
        x_epicenter, y_epicenter = self.event.epicenter
        
        # Shaking intensity peaks early then decays
        time_factor = self._calculate_time_factor()
        
        current_damage = {}
        all_cells = grid_manager.get_all_cells()
        
        for cell in all_cells:
            distance_km = (
                math.sqrt((cell.x - x_epicenter)**2 + (cell.y - y_epicenter)**2) 
                * grid_manager.cell_size / 1000.0
            )
            
            # Seismic attenuation: intensity ~ 1/distance
            spatial_factor = self.get_intensity_at_location(distance_km)
            if spatial_factor < 0.01:
                continue
            
            # Combined intensity
            shaking_intensity = spatial_factor * time_factor
            current_damage[cell.cell_id] = shaking_intensity
            
            # Apply infrastructure damage based on shaking
            self._damage_infrastructure(cell, shaking_intensity)
            
            # Update spatial engine
            cell.seismic_intensity = max(cell.seismic_intensity, shaking_intensity)
        
        self.affected_cells_snapshot = current_damage
        self.total_impact = sum(current_damage.values())

    def _calculate_time_factor(self) -> float:
        """Earthquake shaking peaks quickly then decays."""
        if self.event.duration_ticks == 0:
            return 0.0
        
        progress = self.current_tick / self.event.duration_ticks
        
        if progress < 0.1:
            # Main shock: ramp up rapidly
            return progress / 0.1
        elif progress < 0.3:
            # Aftershocks decay
            return 1.0 - (progress - 0.1) * 2.5
        else:
            # Tail off
            return max(0.0, 1.0 - progress)

    def _damage_infrastructure(self, cell, shaking_intensity: float) -> None:
        """Apply damage to infrastructure based on shaking intensity."""
        # Shaking > 0.5 (Modified Mercalli ~VI+) causes significant damage
        if shaking_intensity > 0.3:
            # Buildings damaged, power lines down
            cell.power_grid_health = max(0.0, cell.power_grid_health - shaking_intensity * 0.4)
            cell.communication_health = max(
                0.0, cell.communication_health - shaking_intensity * 0.3
            )
        
        if shaking_intensity > 0.5:
            # Heavy damage: bridges collapse, pipelines rupture
            cell.transport_network_health = max(
                0.0, cell.transport_network_health - shaking_intensity * 0.6
            )
            cell.water_network_health = max(0.0, cell.water_network_health - shaking_intensity * 0.5)
        
        if shaking_intensity > 0.7:
            # Severe structural damage
            cell.healthcare_capacity = max(0.0, cell.healthcare_capacity - shaking_intensity * 0.5)

    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """Calculate impact on a specific cell."""
        cell_id = f"{cell_x},{cell_y}"
        shaking = self.affected_cells_snapshot.get(cell_id, 0.0)
        
        impacts = {}
        for infra, base_impact in self.INFRASTRUCTURE_IMPACT.items():
            if shaking > 0.2:
                impacts[infra] = base_impact * shaking
            else:
                impacts[infra] = 0.0
        
        return impacts

    def affected_infrastructure_types(self) -> List[str]:
        """Return list of affected infrastructure types."""
        return list(self.INFRASTRUCTURE_IMPACT.keys())
