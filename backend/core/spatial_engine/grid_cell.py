"""Grid cell model — represents a discrete spatial unit in the urban digital twin."""

from enum import Enum
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
import json


class CellState(Enum):
    """Cell operational state."""
    HEALTHY = "healthy"
    AFFECTED = "affected"
    DAMAGED = "damaged"
    COLLAPSED = "collapsed"
    RECOVERING = "recovering"


class PopulationStatus(Enum):
    """Population status in cell."""
    SAFE = "safe"
    AT_RISK = "at_risk"
    THREATENED = "threatened"
    EVACUATED = "evacuated"


@dataclass
class CellMetadata:
    """Metadata for a grid cell."""
    x: int
    y: int
    zone_type: str = "mixed"  # residential, commercial, industrial, mixed
    population_density: float = 0.0  # persons per unit area
    infrastructure_types: List[str] = field(default_factory=list)  # power, water, transport, healthcare
    critical_assets: Dict[str, float] = field(default_factory=dict)  # asset_id -> importance (0-1)
    elevation: float = 0.0
    land_use: str = "urban"
    flood_risk_baseline: float = 0.0  # baseline flood risk (0-1)
    seismic_risk_baseline: float = 0.0
    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize metadata."""
        return {
            "x": self.x,
            "y": self.y,
            "zone_type": self.zone_type,
            "population_density": self.population_density,
            "infrastructure_types": self.infrastructure_types,
            "critical_assets": self.critical_assets,
            "elevation": self.elevation,
            "land_use": self.land_use,
            "flood_risk_baseline": self.flood_risk_baseline,
            "seismic_risk_baseline": self.seismic_risk_baseline,
            "custom_attributes": self.custom_attributes,
        }


@dataclass
class GridCell:
    """A discrete spatial unit (cell) in the urban grid."""

    # Identity
    cell_id: str
    x: int  # grid column
    y: int  # grid row
    metadata: CellMetadata

    # State
    state: CellState = CellState.HEALTHY
    population_status: PopulationStatus = PopulationStatus.SAFE

    # Hazard levels (0-1 normalized)
    flood_intensity: float = 0.0
    seismic_intensity: float = 0.0
    wildfire_intensity: float = 0.0
    pandemic_spread: float = 0.0
    cyber_risk: float = 0.0

    # Infrastructure status (0-1, where 1 = full operational)
    power_grid_health: float = 1.0
    water_network_health: float = 1.0
    transport_network_health: float = 1.0
    healthcare_capacity: float = 1.0
    communication_health: float = 1.0

    # Economic & social metrics
    economic_loss: float = 0.0  # cumulative loss
    damage_level: float = 0.0  # 0-1, fraction of cell damaged
    services_disrupted: List[str] = field(default_factory=list)

    # Recovery & intervention
    recovery_rate: float = 0.1  # % recovery per time step (0-1)
    resources_allocated: Dict[str, float] = field(default_factory=dict)  # resource_type -> amount
    intervention_level: float = 0.0  # 0-1, level of policy intervention applied

    # Temporal tracking
    time_affected: int = 0  # steps since first affected
    time_since_last_update: int = 0

    def get_total_hazard_level(self) -> float:
        """Calculate combined hazard intensity across all disaster types."""
        # Use max rather than weighted sum to detect any significant hazard
        return max(
            self.flood_intensity,
            self.seismic_intensity,
            self.wildfire_intensity,
            self.pandemic_spread,
            self.cyber_risk,
        )

    def get_infrastructure_health(self) -> float:
        """Average infrastructure operational status."""
        healths = [
            self.power_grid_health,
            self.water_network_health,
            self.transport_network_health,
            self.healthcare_capacity,
            self.communication_health,
        ]
        return sum(healths) / len(healths) if healths else 1.0

    def update_state_from_hazards(self) -> None:
        """Determine cell state based on cumulative hazards and infrastructure."""
        hazard_level = self.get_total_hazard_level()
        infra_health = self.get_infrastructure_health()

        if hazard_level > 0.8 or infra_health < 0.1:
            self.state = CellState.COLLAPSED
        elif hazard_level > 0.6 or infra_health < 0.3:
            self.state = CellState.DAMAGED
        elif hazard_level > 0.3:
            self.state = CellState.AFFECTED
        elif self.state == CellState.RECOVERING and infra_health > 0.9:
            self.state = CellState.HEALTHY
        elif self.state in [CellState.DAMAGED, CellState.COLLAPSED]:
            self.state = CellState.RECOVERING

    def apply_recovery(self) -> None:
        """Apply recovery mechanisms (natural + intervention-driven)."""
        # Natural recovery
        self.flood_intensity = max(0.0, self.flood_intensity - self.recovery_rate * 0.05)
        self.pandemic_spread = max(0.0, self.pandemic_spread - self.recovery_rate * 0.02)
        self.cyber_risk = max(0.0, self.cyber_risk - self.recovery_rate * 0.03)

        # Infrastructure recovery
        if self.power_grid_health < 1.0:
            self.power_grid_health = min(1.0, self.power_grid_health + self.recovery_rate * 0.05)
        if self.water_network_health < 1.0:
            self.water_network_health = min(
                1.0, self.water_network_health + self.recovery_rate * 0.03
            )
        if self.transport_network_health < 1.0:
            self.transport_network_health = min(
                1.0, self.transport_network_health + self.recovery_rate * 0.04
            )

        # Intervention boost
        if self.intervention_level > 0:
            intervention_boost = 0.1 * self.intervention_level
            self.power_grid_health = min(1.0, self.power_grid_health + intervention_boost * 0.02)
            self.healthcare_capacity = min(1.0, self.healthcare_capacity + intervention_boost * 0.03)

    def to_dict(self) -> Dict:
        """Serialize cell state to dict."""
        return {
            "cell_id": self.cell_id,
            "x": self.x,
            "y": self.y,
            "state": self.state.value,
            "population_status": self.population_status.value,
            "hazard_levels": {
                "flood": self.flood_intensity,
                "seismic": self.seismic_intensity,
                "wildfire": self.wildfire_intensity,
                "pandemic": self.pandemic_spread,
                "cyber": self.cyber_risk,
            },
            "infrastructure_health": {
                "power": self.power_grid_health,
                "water": self.water_network_health,
                "transport": self.transport_network_health,
                "healthcare": self.healthcare_capacity,
                "communication": self.communication_health,
            },
            "economic_loss": self.economic_loss,
            "damage_level": self.damage_level,
            "services_disrupted": self.services_disrupted,
            "metadata": self.metadata.to_dict(),
        }
