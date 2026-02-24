"""Zoning engine — manages urban zones and their properties."""

from typing import Dict, List, Set
from enum import Enum
from .grid_manager import GridManager
from .grid_cell import GridCell, CellMetadata


class ZoneType(Enum):
    """Urban zone classification."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED = "mixed"
    INFRASTRUCTURE_HUB = "infrastructure_hub"
    HOSPITAL = "hospital"
    EMERGENCY_SHELTER = "emergency_shelter"
    GREEN_SPACE = "green_space"
    AGRICULTURAL = "agricultural"


@staticmethod
def get_zone_properties(zone_type: str) -> Dict:
    """Get baseline properties for zone type."""
    properties = {
        "residential": {
            "population_density": 150.0,
            "infrastructure_types": ["power", "water"],
            "recovery_rate": 0.15,
            "infrastructure_critical_assets": {"primary_substation": 0.3},
        },
        "commercial": {
            "population_density": 100.0,
            "infrastructure_types": ["power", "communication"],
            "recovery_rate": 0.12,
            "infrastructure_critical_assets": {"data_center": 0.8},
        },
        "industrial": {
            "population_density": 50.0,
            "infrastructure_types": ["power", "transport", "water"],
            "recovery_rate": 0.08,
            "infrastructure_critical_assets": {"supplier_node": 0.6},
        },
        "infrastructure_hub": {
            "population_density": 20.0,
            "infrastructure_types": ["power", "water", "transport", "communication"],
            "recovery_rate": 0.05,
            "infrastructure_critical_assets": {
                "central_hub": 1.0,
                "backup_power": 0.7,
            },
        },
        "hospital": {
            "population_density": 200.0,
            "infrastructure_types": ["power", "water", "healthcare"],
            "recovery_rate": 0.2,
            "infrastructure_critical_assets": {"icu": 1.0, "emergency": 0.9},
        },
        "emergency_shelter": {
            "population_density": 300.0,
            "infrastructure_types": ["power", "water", "communication"],
            "recovery_rate": 0.25,
            "infrastructure_critical_assets": {"medical": 0.8},
        },
        "green_space": {
            "population_density": 5.0,
            "infrastructure_types": [],
            "recovery_rate": 0.9,
            "infrastructure_critical_assets": {},
        },
        "mixed": {
            "population_density": 120.0,
            "infrastructure_types": ["power", "water", "transport"],
            "recovery_rate": 0.12,
            "infrastructure_critical_assets": {},
        },
    }
    return properties.get(zone_type, properties["mixed"])


class ZoningEngine:
    """Manages zone assignments and zone-level policies."""

    def __init__(self, grid: GridManager):
        """Initialize zoning engine."""
        self.grid = grid
        self.zones: Dict[str, Set[str]] = {}  # zone_type -> set of cell_ids
        self.zone_aggregates: Dict[str, Dict] = {}  # zone_id -> aggregate stats

    def assign_zone(self, cell: GridCell, zone_type: str) -> None:
        """Assign cell to zone type."""
        cell.metadata.zone_type = zone_type

        # Update zone registry
        if zone_type not in self.zones:
            self.zones[zone_type] = set()
        self.zones[zone_type].add(cell.cell_id)

        # Apply zone properties
        props = get_zone_properties(zone_type)
        cell.metadata.population_density = props["population_density"]
        cell.metadata.infrastructure_types = props["infrastructure_types"]
        cell.recovery_rate = props["recovery_rate"]
        cell.metadata.critical_assets = props["infrastructure_critical_assets"]

    def assign_grid_zones_checkerboard(self) -> None:
        """Assign zones in a simple checkerboard pattern for testing."""
        pattern = [
            ZoneType.RESIDENTIAL.value,
            ZoneType.COMMERCIAL.value,
            ZoneType.MIXED.value,
            ZoneType.INDUSTRIAL.value,
        ]
        idx = 0
        for cell in self.grid.get_all_cells():
            zone_type = pattern[idx % len(pattern)]
            self.assign_zone(cell, zone_type)
            idx += 1

    def assign_grid_zones_geographic(self, seed: int = 42) -> None:
        """Assign zones based on simple geographic regions."""
        import random

        random.seed(seed)
        w, h = self.grid.width, self.grid.height

        # Define region boundaries
        regions = [
            {"type": ZoneType.COMMERCIAL.value, "x_range": (0, w // 3), "y_range": (0, h // 2)},
            {"type": ZoneType.RESIDENTIAL.value, "x_range": (w // 3, 2 * w // 3), "y_range": (0, h)},
            {"type": ZoneType.INDUSTRIAL.value, "x_range": (2 * w // 3, w), "y_range": (0, h // 3)},
            {"type": ZoneType.GREEN_SPACE.value, "x_range": (2 * w // 3, w), "y_range": (h // 3, h)},
        ]

        for cell in self.grid.get_all_cells():
            assigned = False
            for region in regions:
                x_min, x_max = region["x_range"]
                y_min, y_max = region["y_range"]
                if x_min <= cell.x < x_max and y_min <= cell.y < y_max:
                    self.assign_zone(cell, region["type"])
                    assigned = True
                    break

            if not assigned:
                self.assign_zone(cell, ZoneType.MIXED.value)

    def get_zone_health(self, zone_type: str) -> float:
        """Calculate average infrastructure health in zone."""
        if zone_type not in self.zones:
            return 1.0

        cells = [
            self.grid.get_cell(int(cid.split(",")[0]), int(cid.split(",")[1]))
            for cid in self.zones[zone_type]
        ]
        cells = [c for c in cells if c]

        if not cells:
            return 1.0

        avg_health = sum(cell.get_infrastructure_health() for cell in cells) / len(cells)
        return avg_health

    def get_zone_population_at_risk(self, zone_type: str) -> float:
        """Calculate total population at risk in zone."""
        if zone_type not in self.zones:
            return 0.0

        cells = [
            self.grid.get_cell(int(cid.split(",")[0]), int(cid.split(",")[1]))
            for cid in self.zones[zone_type]
        ]
        cells = [c for c in cells if c]

        if not cells:
            return 0.0

        at_risk_pop = sum(
            cell.metadata.population_density
            for cell in cells
            if cell.state.value in ["affected", "damaged", "collapsed"]
        )
        return at_risk_pop

    def apply_zone_intervention(self, zone_type: str, intervention_level: float) -> None:
        """Apply policy intervention to zone (0-1 scale)."""
        if zone_type not in self.zones:
            return

        for cell_id in self.zones[zone_type]:
            x, y = map(int, cell_id.split(","))
            cell = self.grid.get_cell(x, y)
            if cell:
                cell.intervention_level = min(1.0, intervention_level)

    def calculate_zone_statistics(self) -> Dict:
        """Calculate statistics per zone."""
        stats = {}
        for zone_type in self.zones:
            stats[zone_type] = {
                "cell_count": len(self.zones[zone_type]),
                "infrastructure_health": self.get_zone_health(zone_type),
                "population_at_risk": self.get_zone_population_at_risk(zone_type),
            }
        return stats
