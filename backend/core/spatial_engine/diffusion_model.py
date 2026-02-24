"""Diffusion and propagation model — simulates hazard spread across grid."""

from typing import Dict, List, Tuple, Callable
from .grid_manager import GridManager
from .grid_cell import GridCell
import numpy as np


class DiffusionModel:
    """Models the spatial propagation and diffusion of hazards."""

    def __init__(self, grid: GridManager):
        """
        Initialize diffusion model.

        Args:
            grid: GridManager instance
        """
        self.grid = grid

        # Diffusion parameters (tunable)
        self.diffusion_rates = {
            "flood": 0.3,  # spread rate per step
            "seismic": 0.1,
            "wildfire": 0.4,
            "pandemic": 0.25,
            "cyber": 0.2,
        }

        self.neighborhood_decay = {
            "flood": 0.7,  # decay with distance
            "seismic": 0.5,
            "wildfire": 0.8,
            "pandemic": 0.6,
            "cyber": 0.4,
        }

        self.intensity_thresholds = {
            "flood": 0.1,  # minimum to propagate
            "seismic": 0.2,
            "wildfire": 0.15,
            "pandemic": 0.05,
            "cyber": 0.1,
        }

    def propagate_flood(self, cells: List[GridCell]) -> None:
        """Propagate flood hazard to neighbors (considering elevation)."""
        for cell in cells:
            if cell.flood_intensity < self.intensity_thresholds["flood"]:
                continue

            neighbors = self.grid.get_neighbors(cell.x, cell.y, neighborhood="moore")
            spread_rate = self.diffusion_rates["flood"]

            for neighbor in neighbors:
                # Elevation factor: floods spread downhill
                elevation_diff = cell.metadata.elevation - neighbor.metadata.elevation
                elevation_factor = max(0.0, min(1.0, 0.5 + elevation_diff / 100.0))

                new_intensity = (
                    cell.flood_intensity * spread_rate * self.neighborhood_decay["flood"]
                    * elevation_factor
                )
                neighbor.flood_intensity = max(neighbor.flood_intensity, new_intensity)

    def propagate_wildfire(self, cells: List[GridCell]) -> None:
        """Propagate wildfire (fast spread, consumption, wind effects)."""
        for cell in cells:
            if cell.wildfire_intensity < self.intensity_thresholds["wildfire"]:
                continue

            neighbors = self.grid.get_neighbors(cell.x, cell.y, neighborhood="moore")
            spread_rate = self.diffusion_rates["wildfire"]

            for neighbor in neighbors:
                # Land use factor: more spread in natural areas
                land_use_susceptibility = {"urban": 0.3, "suburban": 0.6, "natural": 1.0}.get(
                    neighbor.metadata.land_use, 0.5
                )

                new_intensity = (
                    cell.wildfire_intensity * spread_rate * self.neighborhood_decay["wildfire"]
                    * land_use_susceptibility
                )
                neighbor.wildfire_intensity = max(neighbor.wildfire_intensity, new_intensity)

    def propagate_seismic(self, cells: List[GridCell]) -> None:
        """Propagate seismic shaking (P-waves, S-waves, diminishing with distance)."""
        # Seismic spreads outward from epicenter(s)
        for cell in cells:
            if cell.seismic_intensity < self.intensity_thresholds["seismic"]:
                continue

            # Larger neighborhood for seismic
            neighbors = self.grid.get_neighborhood_radius(cell.x, cell.y, radius=3)
            spread_rate = self.diffusion_rates["seismic"]

            for neighbor in neighbors:
                distance = (
                    np.sqrt((neighbor.x - cell.x) ** 2 + (neighbor.y - cell.y) ** 2) + 1
                )
                decay_factor = self.neighborhood_decay["seismic"] ** (distance - 1)

                new_intensity = cell.seismic_intensity * spread_rate * decay_factor
                neighbor.seismic_intensity = max(neighbor.seismic_intensity, new_intensity)

    def propagate_pandemic(self, cells: List[GridCell]) -> None:
        """Propagate pandemic spread (population-dependent)."""
        for cell in cells:
            if cell.pandemic_spread < self.intensity_thresholds["pandemic"]:
                continue

            neighbors = self.grid.get_neighbors(cell.x, cell.y, neighborhood="moore")
            spread_rate = self.diffusion_rates["pandemic"]

            for neighbor in neighbors:
                # Population density affects transmission
                pop_factor = min(1.0, neighbor.metadata.population_density / 100.0)
                transport_factor = neighbor.transport_network_health  # transport links spread

                new_intensity = (
                    cell.pandemic_spread
                    * spread_rate
                    * self.neighborhood_decay["pandemic"]
                    * (0.5 * pop_factor + 0.5 * transport_factor)
                )
                neighbor.pandemic_spread = max(neighbor.pandemic_spread, new_intensity)

    def propagate_cyber(self, cells: List[GridCell]) -> None:
        """Propagate cyber risk (network-dependent, non-spatial)."""
        for cell in cells:
            if cell.cyber_risk < self.intensity_thresholds["cyber"]:
                continue

            # Cyber spreads to all nearby critical infrastructure
            neighbors = self.grid.get_neighbors(cell.x, cell.y, neighborhood="moore")
            spread_rate = self.diffusion_rates["cyber"]

            for neighbor in neighbors:
                # Cyber spreads through communication networks
                comm_factor = (
                    1.0 - neighbor.communication_health
                ) * 0.5 + neighbor.communication_health * 0.1

                new_intensity = (
                    cell.cyber_risk * spread_rate * self.neighborhood_decay["cyber"] * comm_factor
                )
                neighbor.cyber_risk = max(neighbor.cyber_risk, new_intensity)

    def apply_intensity_decay(
        self, hazard_type: str, decay_rate: float = 0.05
    ) -> None:
        """Apply natural decay of hazard intensity over time."""
        decay_property = {
            "flood": "flood_intensity",
            "seismic": "seismic_intensity",
            "wildfire": "wildfire_intensity",
            "pandemic": "pandemic_spread",
            "cyber": "cyber_risk",
        }.get(hazard_type)

        if not decay_property:
            return

        for cell in self.grid.get_all_cells():
            current = getattr(cell, decay_property)
            setattr(cell, decay_property, max(0.0, current - decay_rate))

    def cascade_infrastructure_damage(self) -> None:
        """Cascade infrastructure failures due to hazard exposure."""
        for cell in self.grid.get_all_cells():
            hazard_level = cell.get_total_hazard_level()

            # Power grid vulnerability
            if cell.flood_intensity > 0.5:
                cell.power_grid_health = max(0.0, cell.power_grid_health - 0.15)
            if cell.cyber_risk > 0.6:
                cell.power_grid_health = max(0.0, cell.power_grid_health - 0.2)

            # Water systems vulnerability
            if cell.flood_intensity > 0.3:
                cell.water_network_health = max(0.0, cell.water_network_health - 0.1)
            if cell.seismic_intensity > 0.4:
                cell.water_network_health = max(0.0, cell.water_network_health - 0.15)

            # Transport vulnerability
            if cell.wildfire_intensity > 0.5:
                cell.transport_network_health = max(0.0, cell.transport_network_health - 0.2)
            if cell.seismic_intensity > 0.6:
                cell.transport_network_health = max(0.0, cell.transport_network_health - 0.25)
            if cell.flood_intensity > 0.4:
                cell.transport_network_health = max(0.0, cell.transport_network_health - 0.12)

            # Healthcare vulnerability
            if hazard_level > 0.5:
                cell.healthcare_capacity = max(
                    0.0, cell.healthcare_capacity - hazard_level * 0.1
                )

            # Communication vulnerability (cyber + physical)
            if cell.cyber_risk > 0.4:
                cell.communication_health = max(0.0, cell.communication_health - 0.2)
            if cell.seismic_intensity > 0.5:
                cell.communication_health = max(0.0, cell.communication_health - 0.12)

    def propagate_step(self, hazard_type: str = "all") -> None:
        """Execute one propagation step for specified hazard type."""
        affected = self.grid.get_affected_cells()

        if hazard_type in ["all", "flood"]:
            self.propagate_flood(affected)
            self.apply_intensity_decay("flood", decay_rate=0.03)

        if hazard_type in ["all", "seismic"]:
            self.propagate_seismic(affected)
            self.apply_intensity_decay("seismic", decay_rate=0.05)

        if hazard_type in ["all", "wildfire"]:
            self.propagate_wildfire(affected)
            self.apply_intensity_decay("wildfire", decay_rate=0.04)

        if hazard_type in ["all", "pandemic"]:
            self.propagate_pandemic(affected)
            self.apply_intensity_decay("pandemic", decay_rate=0.02)

        if hazard_type in ["all", "cyber"]:
            self.propagate_cyber(affected)
            self.apply_intensity_decay("cyber", decay_rate=0.03)

        # Cascade infrastructure damage
        self.cascade_infrastructure_damage()

        # Update cell states
        for cell in self.grid.get_all_cells():
            cell.update_state_from_hazards()
