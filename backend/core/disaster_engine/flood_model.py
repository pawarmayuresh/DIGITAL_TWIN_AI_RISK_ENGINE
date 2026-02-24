"""Flood Model — simulates flood propagation using water diffusion."""

from typing import Dict, List
import numpy as np
import math

from .base_disaster import BaseDisaster, DisasterEvent


class FloodModel(BaseDisaster):
    """
    Flood disaster model.
    
    - Water depth spreads to neighboring cells
    - Elevation affects flow (water flows downhill)
    - Drainage reduces standing water over time
    - Higher water depths cause infrastructure damage
    """

    INFRASTRUCTURE_IMPACT = {
        "power": 0.8,      # Power grid vulnerable to flooding
        "water": 0.7,      # Water systems contaminated
        "transport": 0.9,  # Roads impassable
        "healthcare": 0.6,  # Hospitals damaged
        "communication": 0.4,
    }

    def __init__(self, event: DisasterEvent, rainfall_mm_per_tick: float = 5.0):
        """
        Initialize flood model.
        
        Args:
            event: DisasterEvent specification
            rainfall_mm_per_tick: Rainfall added at epicenter per tick (mm)
        """
        super().__init__(event)
        self.rainfall_mm = rainfall_mm_per_tick
        self.drainage_rate = 0.02  # Fraction of water drained per tick
        self.flow_rate = 0.15  # Fraction of water flowing to neighbors
        
        # Track water depth per cell
        self.water_depth: Dict[str, float] = {}

    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one tick of flood propagation:
        1. Add rainfall to epicenter region
        2. Diffuse water to lower-elevation neighbors
        3. Apply natural drainage
        4. Update cell risk levels
        """
        x_epicenter, y_epicenter = self.event.epicenter
        
        # 1. Add rainfall (convert mm to depth in cell)
        radius = max(1, int(self.event.radius_km / grid_manager.cell_size * 0.5))
        for cell in grid_manager.get_neighborhood_radius(x_epicenter, y_epicenter, radius):
            distance = math.sqrt((cell.x - x_epicenter)**2 + (cell.y - y_epicenter)**2)
            intensity = self.get_intensity_at_location(distance * grid_manager.cell_size / 1000.0)
            rainfall = self.rainfall_mm * intensity / 1000.0  # Convert mm to m
            cell_id = cell.cell_id
            
            if cell_id not in self.water_depth:
                self.water_depth[cell_id] = 0.0
            self.water_depth[cell_id] = min(self.water_depth[cell_id] + rainfall, 10.0)
        
        # 2. Diffuse water to neighbors (especially downhill)
        self._diffuse_water(grid_manager)
        
        # 3. Apply drainage
        self._apply_drainage()
        
        # 4. Update cell infrastructure impacts
        self._update_cell_impacts(grid_manager)
        
        self.total_impact = sum(self.water_depth.values())

    def _diffuse_water(self, grid_manager) -> None:
        """Water flows from high to low flood_depth cells, especially downhill."""
        water_deltas = {}
        
        for cell_id, depth in list(self.water_depth.items()):
            if depth <= 0.01:
                continue
            
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            neighbors = grid_manager.get_neighbors(x, y, neighborhood="moore")
            if not neighbors:
                continue
            
            # Prioritize lower-elevation neighbors
            lower_neighbors = [
                n for n in neighbors 
                if n.metadata.elevation < cell.metadata.elevation
            ]
            
            if not lower_neighbors:
                lower_neighbors = neighbors
            
            # Distribute flow
            flow_per_neighbor = (depth * self.flow_rate) / len(lower_neighbors)
            
            for neighbor in lower_neighbors:
                n_id = neighbor.cell_id
                if n_id not in water_deltas:
                    water_deltas[n_id] = 0.0
                water_deltas[n_id] += flow_per_neighbor
            
            # Reduce source cell depth
            self.water_depth[cell_id] -= flow_per_neighbor * len(lower_neighbors)
        
        # Apply deltas
        for cell_id, delta in water_deltas.items():
            if cell_id not in self.water_depth:
                self.water_depth[cell_id] = 0.0
            self.water_depth[cell_id] = min(self.water_depth[cell_id] + delta, 10.0)

    def _apply_drainage(self) -> None:
        """Natural drainage reduces standing water over time."""
        for cell_id in list(self.water_depth.keys()):
            self.water_depth[cell_id] = max(
                0.0,
                self.water_depth[cell_id] * (1.0 - self.drainage_rate)
            )
            if self.water_depth[cell_id] < 0.01:
                del self.water_depth[cell_id]

    def _update_cell_impacts(self, grid_manager) -> None:
        """Update infrastructure damage based on water depth."""
        self.affected_cells = {}
        
        for cell_id, depth in self.water_depth.items():
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Risk proportional to depth
            risk = min(1.0, depth / 2.0)  # >2m is critical
            self.affected_cells[cell_id] = risk
            
            # Infrastructure damage
            if depth > 0.3:  # 30cm already affects roads
                cell.transport_network_health = max(0.0, cell.transport_network_health - 0.2)
            
            if depth > 0.5:  # 50cm affects power
                cell.power_grid_health = max(0.0, cell.power_grid_health - 0.15)
            
            if depth > 1.0:  # 1m affects water systems
                cell.water_network_health = max(0.0, cell.water_network_health - 0.25)
            
            if depth > 1.5:  # 1.5m affects healthcare
                cell.healthcare_capacity = max(0.0, cell.healthcare_capacity - 0.3)
            
            # Mark as affected in spatial engine
            cell.flood_intensity = risk

    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """Calculate impact on a specific cell."""
        cell_id = f"{cell_x},{cell_y}"
        depth = self.water_depth.get(cell_id, 0.0)
        
        # Risk scales with depth
        risk = min(1.0, depth / 2.0)
        
        impacts = {}
        for infra, base_impact in self.INFRASTRUCTURE_IMPACT.items():
            # Damage increases with depth
            if depth > 0.3:
                impacts[infra] = base_impact * min(1.0, depth / 2.0)
            else:
                impacts[infra] = 0.0
        
        return impacts

    def affected_infrastructure_types(self) -> List[str]:
        """Return list of affected infrastructure types."""
        return list(self.INFRASTRUCTURE_IMPACT.keys())
