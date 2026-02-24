"""Grid manager — orchestrates grid structure, indexing, and spatial operations."""

from typing import Dict, List, Set, Tuple, Optional
from .grid_cell import GridCell, CellMetadata, CellState
import numpy as np


class GridManager:
    """Manages a discrete spatial grid of cells."""

    def __init__(self, width: int, height: int, cell_size: float = 100.0):
        """
        Initialize grid.

        Args:
            width: Number of columns
            height: Number of rows
            cell_size: Physical size of each cell (meters)
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Grid storage: dict[str, GridCell] where key = "x,y"
        self.cells: Dict[str, GridCell] = {}

        # Spatial indexing
        self.cell_index: Dict[str, GridCell] = {}  # same as cells
        self.adjacency_cache: Dict[str, List[str]] = {}  # cell_id -> list of neighbor cell_ids

        # Metadata
        self.total_population = 0.0
        self.total_critical_assets = {}

    def create_cell(
        self, x: int, y: int, metadata: Optional[CellMetadata] = None
    ) -> GridCell:
        """Create and register a cell."""
        cell_id = f"{x},{y}"
        if cell_id in self.cells:
            return self.cells[cell_id]

        if metadata is None:
            metadata = CellMetadata(x=x, y=y)
        else:
            metadata.x = x
            metadata.y = y

        cell = GridCell(
            cell_id=cell_id,
            x=x,
            y=y,
            metadata=metadata,
        )
        self.cells[cell_id] = cell
        self.cell_index[cell_id] = cell

        # Update aggregates
        self.total_population += metadata.population_density

        return cell

    def get_cell(self, x: int, y: int) -> Optional[GridCell]:
        """Retrieve cell at (x, y)."""
        cell_id = f"{x},{y}"
        return self.cells.get(cell_id)

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if (x, y) is within grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(
        self, x: int, y: int, neighborhood: str = "moore"
    ) -> List[GridCell]:
        """
        Get neighboring cells (Moore or Von Neumann neighborhood).

        Args:
            x, y: Cell coordinates
            neighborhood: "moore" (8-connected) or "neumann" (4-connected)

        Returns:
            List of neighbor GridCell objects
        """
        cell_id = f"{x},{y}"

        # Use cache if available
        if cell_id in self.adjacency_cache:
            return [self.cells[cid] for cid in self.adjacency_cache[cell_id] if cid in self.cells]

        neighbors = []
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        if neighborhood == "neumann":
            directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        neighbor_ids = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny):
                neighbor_id = f"{nx},{ny}"
                neighbor_ids.append(neighbor_id)
                if neighbor_id in self.cells:
                    neighbors.append(self.cells[neighbor_id])

        self.adjacency_cache[cell_id] = neighbor_ids
        return neighbors

    def get_neighborhood_radius(self, x: int, y: int, radius: int) -> List[GridCell]:
        """Get all cells within Manhattan distance."""
        cells = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_within_bounds(nx, ny):
                    cell = self.get_cell(nx, ny)
                    if cell:
                        cells.append(cell)
        return cells

    def get_all_cells(self) -> List[GridCell]:
        """Return all cells in the grid."""
        return list(self.cells.values())

    def get_cells_by_state(self, state: CellState) -> List[GridCell]:
        """Get all cells in a specific state."""
        return [cell for cell in self.cells.values() if cell.state == state]

    def get_affected_cells(self) -> List[GridCell]:
        """Get all cells that are damaged or worse."""
        return [
            cell
            for cell in self.cells.values()
            if cell.state in [CellState.AFFECTED, CellState.DAMAGED, CellState.COLLAPSED]
        ]

    def calculate_statistics(self) -> Dict:
        """Calculate grid-wide statistics."""
        cells = self.get_all_cells()
        if not cells:
            return {}

        hazard_levels = [cell.get_total_hazard_level() for cell in cells]
        infra_healths = [cell.get_infrastructure_health() for cell in cells]
        damages = [cell.damage_level for cell in cells]

        return {
            "total_cells": len(cells),
            "average_hazard": np.mean(hazard_levels),
            "max_hazard": np.max(hazard_levels),
            "average_infrastructure_health": np.mean(infra_healths),
            "total_damage": np.sum(damages),
            "affected_cell_count": len(self.get_affected_cells()),
            "affected_population": sum(
                cell.metadata.population_density
                for cell in self.get_affected_cells()
            ),
            "state_distribution": {
                state.value: len(self.get_cells_by_state(state)) for state in CellState
            },
        }

    def reset(self) -> None:
        """Reset all cells to healthy state."""
        for cell in self.cells.values():
            cell.state = CellState.HEALTHY
            cell.flood_intensity = 0.0
            cell.seismic_intensity = 0.0
            cell.wildfire_intensity = 0.0
            cell.pandemic_spread = 0.0
            cell.cyber_risk = 0.0
            cell.power_grid_health = 1.0
            cell.water_network_health = 1.0
            cell.transport_network_health = 1.0
            cell.healthcare_capacity = 1.0
            cell.communication_health = 1.0
            cell.economic_loss = 0.0
            cell.damage_level = 0.0
            cell.services_disrupted = []

    def to_dict(self) -> Dict:
        """Serialize grid state."""
        return {
            "width": self.width,
            "height": self.height,
            "cell_size": self.cell_size,
            "total_cells": len(self.cells),
            "cells": {cid: cell.to_dict() for cid, cell in self.cells.items()},
            "statistics": self.calculate_statistics(),
        }
