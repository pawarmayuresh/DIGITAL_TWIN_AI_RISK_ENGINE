"""Pandemic Model — simulates disease spread and population dynamics."""

from typing import Dict, List
import math
import random

from .base_disaster import BaseDisaster, DisasterEvent


class PandemicModel(BaseDisaster):
    """
    Pandemic disaster model.
    
    - Disease spreads exponentially in high-population areas
    - Transmission depends on transport connectivity and population density
    - Affects healthcare infrastructure + population mortality
    - Impacts cumulative over time (slow-burn, long-duration)
    - Healthcare infrastructure quality reduces infection spread
    """

    INFRASTRUCTURE_IMPACT = {
        "healthcare": 0.8,      # Healthcare systems overwhelmed
        "power": 0.2,           # Minimal power impact
        "transport": 0.4,       # Movement restrictions
        "water": 0.3,           # Water systems stressed
        "communication": 0.1,   # Comms actually help (info spread)
    }

    def __init__(
        self,
        event: DisasterEvent,
        transmission_rate: float = 0.3,  # 30% per day
        incubation_period: float = 5.0,  # days before symptoms
        recovery_rate: float = 0.95,     # 95% survival
    ):
        """
        Initialize pandemic model.
        
        Args:
            event: DisasterEvent specification
            transmission_rate: Base transmission probability
            incubation_period: Time before onset
            recovery_rate: Fraction who survive
        """
        super().__init__(event)
        self.transmission_rate = transmission_rate
        self.incubation_period = incubation_period
        self.recovery_rate = recovery_rate
        
        # Infection level per cell (0-1)
        self.infection_level: Dict[str, float] = {}
        
        # Cumulative mortality per cell
        self.mortality_per_cell: Dict[str, float] = {}

    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one tick of pandemic:
        1. Infection spreads from high-infection cells to neighbors
        2. Transmission varies by population density, transport, healthcare
        3. Infections resolve (recovery or mortality)
        4. Track cumulative health impacts
        """
        x_epicenter, y_epicenter = self.event.epicenter
        
        # Initialize infection at epicenter
        if self.current_tick == 0:
            cell = grid_manager.get_cell(x_epicenter, y_epicenter)
            if cell:
                self.infection_level[cell.cell_id] = 0.1  # 10% infected initially
        
        # Spread to neighbors
        self._spread_infection(grid_manager)
        
        # Advance infection in existing cells
        self._advance_infection(grid_manager)
        
        # Apply healthcare impact
        self._apply_healthcare_impact(grid_manager)
        
        self.affected_cells = {k: v for k, v in self.infection_level.items() if v > 0}
        self.total_impact = sum(self.infection_level.values())

    def _spread_infection(self, grid_manager) -> None:
        """Spread infection to neighboring cells."""
        new_infections = {}
        
        for cell_id, infection in self.infection_level.items():
            if infection < 0.01:
                continue  # Too low to spread
            
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Get neighbors (Moore neighborhood for transport connectivity)
            neighbors = grid_manager.get_neighbors(x, y, neighborhood="moore")
            
            for neighbor in neighbors:
                if neighbor.cell_id in self.infection_level:
                    continue  # Already infected
                
                # Transmission depends on:
                # 1. Population density (more people = faster spread)
                # 2. Transport connectivity (better = more spread)
                # 3. Healthcare quality (better = less spread)
                
                pop_factor = min(1.0, neighbor.metadata.population_density / 5000.0)  # Normalized
                transport_factor = neighbor.transport_network_health  # Good transport = spread
                healthcare_factor = 1.0 - neighbor.healthcare_capacity  # Poor healthcare = spread
                
                transmission_prob = min(
                    1.0,
                    self.transmission_rate
                    * infection
                    * pop_factor
                    * transport_factor
                    * healthcare_factor
                    * self.event.severity
                )
                
                if random.random() < transmission_prob:
                    new_infections[neighbor.cell_id] = 0.05  # Seed infection

        self.infection_level.update(new_infections)

    def _advance_infection(self, grid_manager) -> None:
        """Advance infection state and recovery."""
        to_remove = []
        
        for cell_id in list(self.infection_level.keys()):
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            current = self.infection_level[cell_id]
            
            # Infection grows exponentially
            growth_rate = 1.0 + self.transmission_rate * self.event.severity
            
            # Healthcare reduces growth
            healthcare_effect = 1.0 - (cell.healthcare_capacity * 0.5)
            growth_rate *= healthcare_effect
            
            # Infection plateaus as population immunity builds
            saturation = 1.0 - (current ** 0.5)  # Diminishing returns
            
            new_level = current * growth_rate * saturation
            new_level = min(0.8, new_level)  # Cap at 80% infected
            
            if new_level > 0.01:
                self.infection_level[cell_id] = new_level
            else:
                to_remove.append(cell_id)
            
            # Mortality accumulates
            mortality = (1.0 - self.recovery_rate) * current * 0.01  # 1% of infected per tick
            self.mortality_per_cell[cell_id] = self.mortality_per_cell.get(cell_id, 0) + mortality
            
            # Update population (mortality reduces density)
            cell.metadata.population_density = max(
                0, cell.metadata.population_density - (cell.metadata.population_density * mortality)
            )
        
        for cell_id in to_remove:
            del self.infection_level[cell_id]

    def _apply_healthcare_impact(self, grid_manager) -> None:
        """Apply pandemic impacts to healthcare infrastructure."""
        for cell_id, infection in self.infection_level.items():
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Healthcare stress from infections
            stress = infection * 0.5  # Up to 50% capacity reduction
            cell.healthcare_capacity = max(0.0, cell.healthcare_capacity - stress)
            
            # Update pandemic intensity
            cell.pandemic_spread = max(cell.pandemic_spread, infection)

    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """Calculate impact on a specific cell."""
        cell_id = f"{cell_x},{cell_y}"
        infection = self.infection_level.get(cell_id, 0)
        
        impacts = {}
        for infra, base_impact in self.INFRASTRUCTURE_IMPACT.items():
            impacts[infra] = base_impact * infection
        
        return impacts

    def affected_infrastructure_types(self) -> List[str]:
        """Return list of affected infrastructure types."""
        return list(self.INFRASTRUCTURE_IMPACT.keys())
