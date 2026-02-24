"""Cyber Attack Model — simulates network-based attacks and cascading infrastructure failure."""

from typing import Dict, List
import math
import random

from .base_disaster import BaseDisaster, DisasterEvent


class CyberAttackModel(BaseDisaster):
    """
    Cyber attack disaster model.
    
    - Attacks propagate through communication/power network connectivity
    - Not spatially bound — spreads via infrastructure links
    - Primary targets: communication, power, water SCADA
    - Can cascade: power failure → water pump failure → healthcare impact
    - Affects multiple infrastructure types sequentially
    """

    INFRASTRUCTURE_IMPACT = {
        "communication": 0.9,   # Primary target
        "power": 0.7,           # Secondary target (SCADA systems)
        "water": 0.8,           # Water treatment SCADA vulnerable
        "healthcare": 0.6,      # Depends on IT systems
        "transport": 0.4,       # Traffic signals, GPS affected
    }

    def __init__(
        self,
        event: DisasterEvent,
        target_infrastructure: str = "communication",  # Primary attack vector
        cascade_delay: int = 3,  # ticks before cascade to other systems
    ):
        """
        Initialize cyber attack model.
        
        Args:
            event: DisasterEvent specification
            target_infrastructure: Primary attack target
            cascade_delay: Ticks before failure cascades
        """
        super().__init__(event)
        self.target_infrastructure = target_infrastructure
        self.cascade_delay = cascade_delay
        
        # Compromised cells (cell_id -> compromission_level)
        self.compromised_cells: Dict[str, float] = {}
        
        # Time since compromise (for cascades)
        self.compromise_age: Dict[str, int] = {}
        
        # Cascaded failures (secondary infrastructure affected)
        self.cascaded_failures: Dict[str, List[str]] = {}

    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one tick of cyber attack:
        1. Initial compromise at epicenter
        2. Spread to connected nodes (infrastructure links)
        3. Cascade to dependent systems after delay
        4. Update infrastructure health
        """
        x_epicenter, y_epicenter = self.event.epicenter
        
        # Initialize attack at epicenter
        if self.current_tick == 0:
            cell = grid_manager.get_cell(x_epicenter, y_epicenter)
            if cell:
                self.compromised_cells[cell.cell_id] = 0.1
                self.compromise_age[cell.cell_id] = 0
        
        # Age all compromised cells
        for cell_id in list(self.compromise_age.keys()):
            self.compromise_age[cell_id] += 1
        
        # Spread through network
        self._propagate_through_network(grid_manager)
        
        # Apply cascading failures
        self._apply_cascades(grid_manager)
        
        # Update cell infrastructure health
        self._update_infrastructure_health(grid_manager)
        
        self.affected_cells = self.compromised_cells.copy()
        self.total_impact = sum(self.compromised_cells.values())

    def _propagate_through_network(self, grid_manager) -> None:
        """Spread compromise through network connectivity."""
        new_compromises = {}
        
        for cell_id, compromission in list(self.compromised_cells.items()):
            if compromission < 0.01:
                continue
            
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Cyber spreads through high-connectivity neighbors
            neighbors = grid_manager.get_neighbors(x, y, neighborhood="moore")
            
            for neighbor in neighbors:
                if neighbor.cell_id in self.compromised_cells:
                    continue  # Already compromised
                
                # Spread probability based on:
                # 1. Communication infrastructure quality
                # 2. Attack strength/severity
                # 3. Target proximity
                
                connectivity = neighbor.communication_health
                spread_prob = min(
                    1.0,
                    0.3 * compromission * connectivity * self.event.severity
                )
                
                if random.random() < spread_prob:
                    new_compromises[neighbor.cell_id] = compromission * 0.5
                    self.compromise_age[neighbor.cell_id] = 0

        self.compromised_cells.update(new_compromises)

    def _apply_cascades(self, grid_manager) -> None:
        """Apply cascading failures to dependent infrastructure."""
        for cell_id in self.compromised_cells.keys():
            age = self.compromise_age.get(cell_id, 0)
            
            if age >= self.cascade_delay:
                x, y = map(int, cell_id.split(","))
                cell = grid_manager.get_cell(x, y)
                if not cell:
                    continue
                
                # Define cascade paths
                cascades = [
                    ("communication", "power"),       # Telecom depends on power
                    ("communication", "water"),        # SCADA depends on comms
                    ("power", "water"),                # Water pumps need power
                    ("power", "healthcare"),           # Hospitals need power
                ]
                
                if cell_id not in self.cascaded_failures:
                    self.cascaded_failures[cell_id] = []
                
                for source, target in cascades:
                    if source == self.target_infrastructure:
                        compromise = self.compromised_cells[cell_id]
                        # Cascade severity depends on source compromise level
                        cascade_severity = compromise * 0.8  # Slightly less severe
                        
                        if target not in self.cascaded_failures[cell_id]:
                            self.cascaded_failures[cell_id].append(target)
                            
                            # You could add downstream compromise here
                            # For now, we track what cascaded

    def _update_infrastructure_health(self, grid_manager) -> None:
        """Update gridcell infrastructure health based on attacks."""
        for cell_id, compromission in self.compromised_cells.items():
            x, y = map(int, cell_id.split(","))
            cell = grid_manager.get_cell(x, y)
            if not cell:
                continue
            
            # Direct impact
            cell.communication_health = max(
                0.0, cell.communication_health - compromission * 0.15
            )
            
            # Cascade impacts
            cascades = self.cascaded_failures.get(cell_id, [])
            if "power" in cascades:
                cell.power_grid_health = max(0.0, cell.power_grid_health - compromission * 0.1)
            if "water" in cascades:
                cell.water_network_health = max(0.0, cell.water_network_health - compromission * 0.1)
            if "healthcare" in cascades:
                cell.healthcare_system_health = max(
                    0.0, cell.healthcare_system_health - compromission * 0.1
                )
            
            # Update cyber intensity
            cell.cyber_risk = max(cell.cyber_risk, compromission)

    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """Calculate impact on a specific cell."""
        cell_id = f"{cell_x},{cell_y}"
        compromission = self.compromised_cells.get(cell_id, 0)
        cascades = self.cascaded_failures.get(cell_id, [])
        
        impacts = {}
        for infra, base_impact in self.INFRASTRUCTURE_IMPACT.items():
            if infra == self.target_infrastructure or infra in cascades:
                impacts[infra] = base_impact * compromission
            else:
                impacts[infra] = 0.0
        
        return impacts

    def affected_infrastructure_types(self) -> List[str]:
        """Return list of affected infrastructure types."""
        primary = [self.target_infrastructure]
        secondary = []
        
        # Most cascade scenarios include power/water
        if self.target_infrastructure == "communication":
            secondary = ["power", "water", "healthcare"]
        elif self.target_infrastructure == "power":
            secondary = ["water", "healthcare", "transport"]
        
        return primary + secondary
