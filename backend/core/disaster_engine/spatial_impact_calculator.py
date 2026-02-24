"""Spatial Impact Calculator — maps disaster impacts to grid cells and infrastructure."""

from typing import Dict, List, Tuple

from .disaster_manager import DisasterManager


class SpatialImpactCalculator:
    """
    Calculates and applies disaster impacts to grid cells.
    
    - Queries DisasterManager for aggregated impacts
    - Applies infrastructure damage to GridCell objects
    - Tracks population affected
    - Identifies critical infrastructure failures
    """

    def __init__(self, disaster_manager: DisasterManager):
        """
        Initialize impact calculator.
        
        Args:
            disaster_manager: DisasterManager instance
        """
        self.disaster_manager = disaster_manager

    def apply_impacts(self, grid_manager) -> Dict:
        """
        Apply all active disaster impacts to grid cells.
        
        Returns:
            Impact report with statistics
        """
        report = {
            "total_cells_affected": 0,
            "population_affected": 0,
            "infrastructure_failures": {},
            "critical_zones": [],
        }
        
        # Iterate grid and apply impacts
        for cell in grid_manager.get_all_cells():
            impacts = self.disaster_manager.get_aggregated_impact(cell.x, cell.y)
            
            if not impacts or all(v == 0 for v in impacts.values()):
                continue  # No impact
            
            # Track affected
            report["total_cells_affected"] += 1
            report["population_affected"] += cell.metadata.population_density
            
            # Apply each infrastructure damage
            self._apply_infrastructure_damage(cell, impacts, report)
        
        return report

    def _apply_infrastructure_damage(
        self, cell, impacts: Dict[str, float], report: Dict
    ) -> None:
        """Apply damage to cell infrastructure based on disaster impacts."""
        for infra_type, damage_factor in impacts.items():
            if damage_factor <= 0:
                continue
            
            if infra_type == "power":
                cell.power_grid_health = max(0.0, cell.power_grid_health - damage_factor * 0.3)
                report["infrastructure_failures"]["power"] = (
                    report["infrastructure_failures"].get("power", 0) + 1
                )
            
            elif infra_type == "water":
                cell.water_network_health = max(
                    0.0, cell.water_network_health - damage_factor * 0.3
                )
                report["infrastructure_failures"]["water"] = (
                    report["infrastructure_failures"].get("water", 0) + 1
                )
            
            elif infra_type == "transport":
                cell.transport_network_health = max(
                    0.0, cell.transport_network_health - damage_factor * 0.3
                )
                report["infrastructure_failures"]["transport"] = (
                    report["infrastructure_failures"].get("transport", 0) + 1
                )
            
            elif infra_type == "healthcare":
                cell.healthcare_capacity = max(
                    0.0, cell.healthcare_capacity - damage_factor * 0.3
                )
                report["infrastructure_failures"]["healthcare"] = (
                    report["infrastructure_failures"].get("healthcare", 0) + 1
                )
            
            elif infra_type == "communication":
                cell.communication_health = max(
                    0.0, cell.communication_health - damage_factor * 0.3
                )
                report["infrastructure_failures"]["communication"] = (
                    report["infrastructure_failures"].get("communication", 0) + 1
                )
        
        # Identify critical zones (multiple infrastructure failures)
        failures = sum(
            1
            for h in [
                cell.power_grid_health,
                cell.water_network_health,
                cell.healthcare_capacity,
            ]
            if h < 0.3
        )
        
        if failures >= 2:
            report["critical_zones"].append((cell.x, cell.y))

    def get_infrastructure_status(self, grid_manager) -> Dict[str, float]:
        """
        Get average infrastructure health across grid.
        
        Returns:
            {infrastructure_type: average_health (0-1)}
        """
        cells = list(grid_manager.get_all_cells())
        if not cells:
            return {}
        
        status = {
            "power": sum(c.power_grid_health for c in cells) / len(cells),
            "water": sum(c.water_network_health for c in cells) / len(cells),
            "transport": sum(c.transport_network_health for c in cells) / len(cells),
            "healthcare": sum(c.healthcare_capacity for c in cells) / len(cells),
            "communication": sum(c.communication_health for c in cells) / len(cells),
        }
        
        return status

    def get_population_vulnerability(self, grid_manager) -> Dict:
        """
        Assess population vulnerability based on:
        - Population density
        - Healthcare infrastructure status
        - Accessible resources
        
        Returns:
            Vulnerability metrics
        """
        cells = list(grid_manager.get_all_cells())
        total_pop = sum(c.metadata.population_density for c in cells)
        
        if total_pop == 0:
            return {"vulnerability_index": 0.0, "at_risk_population": 0}
        
        # Calculate vulnerability index
        vulnerability_score = 0.0
        at_risk_pop = 0
        
        for cell in cells:
            # High population + low healthcare = high vulnerability
            pop_factor = cell.metadata.population_density / max(1, total_pop / len(cells))  # Relative density
            healthcare_factor = 1.0 - cell.healthcare_capacity
            
            cell_vulnerability = pop_factor * healthcare_factor
            vulnerability_score += cell_vulnerability * cell.metadata.population_density
            
            if cell_vulnerability > 0.5:
                at_risk_pop += cell.metadata.population_density
        
        return {
            "vulnerability_index": min(1.0, vulnerability_score / total_pop),
            "at_risk_population": at_risk_pop,
            "total_population": total_pop,
        }

    def identify_intervention_priorities(
        self, grid_manager, intervention_radius: int = 2
    ) -> List[Tuple[int, int, str]]:
        """
        Identify where interventions (supply drops, repairs) should focus.
        
        Args:
            grid_manager: GridManager instance
            intervention_radius: Search radius for clustering
            
        Returns:
            List of (x, y, priority_type) tuples
        """
        priorities = []
        
        for cell in grid_manager.get_all_cells():
            # Healthcare shortage = high priority
            if cell.healthcare_capacity < 0.3 and cell.metadata.population_density > 1000:
                priorities.append((cell.x, cell.y, "healthcare_support"))
            
            # Power failure affecting dense areas
            if cell.power_grid_health < 0.2 and cell.metadata.population_density > 2000:
                priorities.append((cell.x, cell.y, "power_restoration"))
            
            # Water contamination/failure
            if cell.water_network_health < 0.3 and cell.metadata.population_density > 1500:
                priorities.append((cell.x, cell.y, "water_supply"))
        
        return priorities
