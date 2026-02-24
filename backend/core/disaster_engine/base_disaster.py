"""Base disaster abstraction — defines interface for all disaster types."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import random


class DisasterType(Enum):
    """Supported disaster types."""
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"
    WILDFIRE = "wildfire"
    PANDEMIC = "pandemic"
    CYBER_ATTACK = "cyber_attack"


class Severity(Enum):
    """Disaster severity levels."""
    MINOR = 0.3
    MODERATE = 0.6
    SEVERE = 0.8
    CATASTROPHIC = 1.0


@dataclass
class DisasterEvent:
    """A disaster event specification."""
    
    event_id: str
    disaster_type: DisasterType
    epicenter: tuple = (0, 0)  # (x, y) grid coordinates
    severity: float = 0.5  # 0-1 normalized
    radius_km: float = 5.0
    duration_ticks: int = 50
    onset_time: int = 0  # when to start (simulation tick)
    seed: Optional[int] = None
    custom_params: Dict = field(default_factory=dict)


class BaseDisaster(ABC):
    """
    Abstract base class for all disaster types.
    
    Defines interface for:
    - Propagation/evolution
    - Infrastructure impact
    - Recovery dynamics
    - Risk assessment
    """

    def __init__(self, event: DisasterEvent):
        """
        Initialize disaster from event specification.
        
        Args:
            event: DisasterEvent with type, location, severity, etc.
        """
        self.event = event
        self.current_tick = 0
        self.is_active = False
        self.affected_cells: Dict[str, float] = {}  # cell_id -> impact intensity
        self.total_impact = 0.0
        
        # Reproducibility
        if event.seed is not None:
            random.seed(event.seed)

    @abstractmethod
    def propagate(self, grid_manager, simulation_context) -> None:
        """
        Execute one simulation tick of disaster propagation.
        
        Args:
            grid_manager: GridManager instance
            simulation_context: Simulation state for context
        """
        pass

    @abstractmethod
    def calculate_impact(self, cell_x: int, cell_y: int) -> Dict[str, float]:
        """
        Calculate impact on a specific cell.
        
        Args:
            cell_x, cell_y: Grid coordinates
            
        Returns:
            Dict of infrastructure impacts: {infrastructure_type: damage_fraction}
        """
        pass

    @abstractmethod
    def affected_infrastructure_types(self) -> List[str]:
        """Return list of infrastructure types affected by this disaster."""
        pass

    def step(self, grid_manager, simulation_context) -> None:
        """Execute one step of disaster evolution."""
        if self.current_tick < self.event.duration_ticks:
            self.is_active = True
            self.propagate(grid_manager, simulation_context)
            self.current_tick += 1
        else:
            self.is_active = False

    def get_intensity_at_location(self, distance_km: float) -> float:
        """
        Calculate disaster intensity at distance from epicenter.
        
        Intensity decays with distance and reaches 0 after radius.
        
        Args:
            distance_km: Distance from epicenter in km
            
        Returns:
            Intensity factor 0-1
        """
        if distance_km > self.event.radius_km:
            return 0.0
        
        fraction_of_radius = distance_km / self.event.radius_km
        # Quadratic decay: stronger near epicenter
        intensity = self.event.severity * (1.0 - fraction_of_radius ** 2)
        return max(0.0, intensity)

    def get_time_factor(self) -> float:
        """
        Calculate temporal evolution factor (0 → 1 → 0 or similar).
        
        Most disasters intensify, peak, then subside.
        """
        if self.event.duration_ticks == 0:
            return 0.0
        
        progress = self.current_tick / self.event.duration_ticks
        
        if progress < 0.3:
            # Onset phase: ramp up
            return (progress / 0.3) * 0.7
        elif progress < 0.7:
            # Peak phase: high intensity
            return 0.7 + (progress - 0.3) / 0.4 * 0.3
        else:
            # Decay phase: subside
            return (1.0 - progress) / 0.3
    
    def reset(self) -> None:
        """Reset disaster to initial state."""
        self.current_tick = 0
        self.is_active = False
        self.affected_cells = {}
        self.total_impact = 0.0

    def summary(self) -> Dict:
        """Get summary statistics of disaster."""
        return {
            "event_id": self.event.event_id,
            "type": self.event.disaster_type.value,
            "current_tick": self.current_tick,
            "duration_ticks": self.event.duration_ticks,
            "is_active": self.is_active,
            "affected_cell_count": len(self.affected_cells),
            "total_impact": self.total_impact,
            "severity": self.event.severity,
        }
