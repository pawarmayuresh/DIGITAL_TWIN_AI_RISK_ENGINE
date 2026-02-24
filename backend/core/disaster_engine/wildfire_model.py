"""Wildfire Model — simulates fire spread and combustion dynamics."""

from typing import Dict, List
import math
import random

from .base_disaster import BaseDisaster, DisasterEvent


class WildfireModel(BaseDisaster):
    """
    Wildfire disaster model.
    
    - Fire spreads to ignitable neighboring cells
    - Spread depends on fuel, wind, vegetation
    - Cells burn out and become less combustible
    - Primarily affects transport and power infrastructure (lines, poles)
    - Fast-moving and aggressive spread
    """

    INFRASTRUCTURE_IMPACT = {
        "power": 0.9,         # Power lines ignite
        "transport": 0.8,     # Roads blocked by fire
        "healthcare": 0.5,    # Smoke impacts health
        "water": 0.3,         # Water systems less affected
        "communication": 0.4,
    }

    def __init__(
        self,
        event: DisasterEvent,
        wind_direction: float = 0.0,  # degrees (0=N, 90=E, 180=S, 270=W)
        wind_speed: float = 10.0,     # km/h
    ):
        """
        Initialize wildfire model.
        
        Args:
            event: DisasterEvent specification
            wind_direction: Wind direction in degrees
            wind_speed: Wind speed in km/h
        """
        super().__init__(event)
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        
        # Cells currently burning
        self.burning_cells: Dict[str, float] = {}  # cell_id -> burn_time (ticks)
        
        # Fuel content per cell
        self.fuel_remaining: Dict[str, float] = {}

    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one tick of wildfire:
        1. Advance burn time in burning cells
        2. Cells burnout when fuel exhausted
        3. Spread to unburned neighbors based on wind + fuel
        4. Apply damage to infrastructure
        """
        x_epicenter, y_epicenter = self.event.epicenter
        
        # Initialize epicenter burning
        if self.current_tick == 0:
            radius = max(1, int(self.event.radius_km / grid_manager.cell_size * 0.3))
            for cell in grid_manager.get_neighborhood_radius(x_epicenter, y_epicenter, radius):
                cell_id = cell.cell_id
                self.burning_cells[cell_id] = 0
                self.fuel_remaining[cell_id] = 1.0  # Full fuel
        
        # Advance burning cells
        burned_out = []
        for cell_id in list(self.burning_cells.keys()):
            self.burning_cells[cell_id] += 1
            fuel = self.fuel_remaining.get(cell_id, 0.0)
            fuel -= 0.15  # Burn rate per tick
            self.fuel_remaining[cell_id] = max(0.0, fuel)
            
            if fuel <= 0:
                burned_out.append(cell_id)
        
        # Remove burned out cells
        for cell_id in burned_out:
            del self.burning_cells[cell_id]
        
        # Spread fire to neighbors
        self._spread_fire(grid_manager)
        
        # Apply damage
        self._apply_fire_damage(grid_manager)
        
        self.affected_cells = {**self.burning_cells}
        self.total_impact = len(self.burning_cells)

    def _spread_fire(self, grid_manager) -> None:
        """Spread fire to neighboring cells based on wind and fuel."""
        new_burns = []
        
        for cell_id in list(self.burning_cells.keys()):
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Get neighbors (especially downwind)
            neighbors = grid_manager.get_neighbors(x, y, neighborhood="moore")
            
            for neighbor in neighbors:
                if neighbor.cell_id in self.burning_cells:
                    continue  # Already burning
                
                # Wind effect: fire spreads faster downwind
                wind_boost = self._calculate_wind_boost(cell, neighbor)
                
                # Fuel content (vegetation): natural areas burn faster
                fuel_factor = self._get_fuel_factor(neighbor)
                
                # Ignition probability
                distance_factor = 0.5  # Adjacent cell
                ignition_prob = min(
                    1.0,
                    distance_factor * wind_boost * fuel_factor * self.event.severity
                )
                
                if random.random() < ignition_prob:
                    new_burns.append(neighbor.cell_id)
                    self.fuel_remaining[neighbor.cell_id] = 1.0
        
        # Add new burns
        for cell_id in new_burns:
            self.burning_cells[cell_id] = 0

    def _calculate_wind_boost(self, source_cell, target_cell) -> float:
        """Calculate wind-based fire spread boost."""
        # Simple wind: boost if target is downwind of source
        dx = target_cell.x - source_cell.x
        dy = target_cell.y - source_cell.y
        
        # Convert wind direction to unit vector
        wind_rad = math.radians(self.wind_direction)
        wind_x = math.cos(wind_rad)
        wind_y = math.sin(wind_rad)
        
        # Dot product: how aligned target is with wind direction
        alignment = (dx * wind_x + dy * wind_y) / max(
            math.sqrt(dx**2 + dy**2), 0.1
        )
        
        # Boost if downwind (alignment > 0)
        return 1.0 + max(0.0, alignment) * (self.wind_speed / 20.0)

    def _get_fuel_factor(self, cell) -> float:
        """Get flammability based on land use."""
        land_use = cell.metadata.land_use.lower()
        
        fuel_map = {
            "natural": 1.0,      # Forests, grasslands burn easily
            "suburban": 0.6,     # Some trees, buildings
            "urban": 0.3,        # Buildings, less vegetation
            "water": 0.0,        # No burn
            "agricultural": 0.8,  # Crops burn
        }
        
        return fuel_map.get(land_use, 0.5)

    def _apply_fire_damage(self, grid_manager) -> None:
        """Apply damage from fire."""
        for cell_id in self.burning_cells.keys():
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Fire intensity based on burn time
            burn_time = self.burning_cells[cell_id]
            intensity = min(1.0, burn_time / 10.0)  # Max intensity after 10 ticks
            
            # Power lines especially vulnerable
            cell.power_grid_health = max(0.0, cell.power_grid_health - intensity * 0.3)
            cell.transport_network_health = max(
                0.0, cell.transport_network_health - intensity * 0.25
            )
            
            # Update spatial engine
            cell.wildfire_intensity = max(cell.wildfire_intensity, intensity)

    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """Calculate impact on a specific cell."""
        cell_id = f"{cell_x},{cell_y}"
        burn_time = self.burning_cells.get(cell_id, 0)
        intensity = min(1.0, burn_time / 10.0)
        
        impacts = {}
        for infra, base_impact in self.INFRASTRUCTURE_IMPACT.items():
            impacts[infra] = base_impact * intensity
        
        return impacts

    def affected_infrastructure_types(self) -> List[str]:
        """Return list of affected infrastructure types."""
        return list(self.INFRASTRUCTURE_IMPACT.keys())
