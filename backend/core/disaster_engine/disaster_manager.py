"""Disaster Manager — orchestrates multiple simultaneous disasters and cascading failures."""

from typing import Dict, List, Optional
from enum import Enum

from .base_disaster import BaseDisaster, DisasterEvent, DisasterType
from .flood_model import FloodModel
from .earthquake_model import EarthquakeModel
from .wildfire_model import WildfireModel
from .pandemic_model import PandemicModel
from .cyber_attack_model import CyberAttackModel


class DisasterManager:
    """
    Manages multiple simultaneous disasters.
    
    - Maintains active disasters track
    - Orchestrates propagation for each
    - Handles cascading triggers (e.g., earthquake → fires)
    - Aggregates impacts across disaster types
    - Provides unified interface to GridSimulationRunner
    """

    def __init__(self):
        """Initialize empty disaster manager."""
        self.active_disasters: Dict[str, BaseDisaster] = {}
        self.disaster_history: Dict[str, List[BaseDisaster]] = {}  # By type
        self.cascade_triggers: Dict[str, List[str]] = {
            # Earthquake can trigger fires
            DisasterType.EARTHQUAKE: [DisasterType.WILDFIRE],
            # Flood can trigger cyber (water treatment SCADA)
            DisasterType.FLOOD: [DisasterType.CYBER_ATTACK],
            # Pandemic stresses multiple systems
            DisasterType.PANDEMIC: [],
        }

    def add_disaster(self, disaster: BaseDisaster) -> str:
        """
        Add an active disaster.
        
        Args:
            disaster: BaseDisaster instance
            
        Returns:
            Unique disaster ID
        """
        disaster_id = f"{disaster.event.disaster_type.value}_{len(self.active_disasters)}"
        self.active_disasters[disaster_id] = disaster
        
        # Track in history
        dtype = disaster.event.disaster_type.value
        if dtype not in self.disaster_history:
            self.disaster_history[dtype] = []
        self.disaster_history[dtype].append(disaster)
        
        return disaster_id

    def remove_disaster(self, disaster_id: str) -> None:
        """Remove completed disaster."""
        if disaster_id in self.active_disasters:
            del self.active_disasters[disaster_id]

    def propagate_all(self, grid_manager, simulation_context) -> None:
        """Execute one tick of all active disasters."""
        for disaster_id in list(self.active_disasters.keys()):
            disaster = self.active_disasters[disaster_id]
            disaster.propagate(grid_manager, simulation_context)
            
            # Check if disaster is complete (intensity decayed below threshold)
            if disaster.total_impact < 0.01:
                self.remove_disaster(disaster_id)

    def trigger_cascades(self, grid_manager, source_disaster: BaseDisaster) -> None:
        """
        Check if a disaster should trigger cascading disasters.
        
        Args:
            grid_manager: GridManager instance
            source_disaster: The disaster that may trigger cascades
        """
        cascade_targets = self.cascade_triggers.get(
            source_disaster.event.disaster_type, []
        )
        
        for cascade_type in cascade_targets:
            if source_disaster.total_impact > 0.2:  # Only cascade if strong enough
                # Create cascade event
                cascade_event = DisasterEvent(
                    disaster_type=cascade_type,
                    severity=source_disaster.event.severity * 0.6,  # Reduced severity
                    epicenter=source_disaster.event.epicenter,
                    radius_km=source_disaster.event.radius_km,
                    start_tick=source_disaster.current_tick,
                )
                
                cascade_disaster = self._create_disaster(cascade_event)
                if cascade_disaster:
                    self.add_disaster(cascade_disaster)

    def _create_disaster(self, event: DisasterEvent) -> Optional[BaseDisaster]:
        """Factory method to create appropriate disaster model."""
        if event.disaster_type == DisasterType.FLOOD:
            return FloodModel(event)
        elif event.disaster_type == DisasterType.EARTHQUAKE:
            return EarthquakeModel(event)
        elif event.disaster_type == DisasterType.WILDFIRE:
            return WildfireModel(event)
        elif event.disaster_type == DisasterType.PANDEMIC:
            return PandemicModel(event)
        elif event.disaster_type == DisasterType.CYBER_ATTACK:
            return CyberAttackModel(event)
        return None

    def get_aggregated_impact(
        self, cell_x: int, cell_y: int
    ) -> Dict[str, float]:
        """
        Get combined impact from all disasters at a location.
        
        Returns dict: {infrastructure_type: total_damage_factor}
        """
        aggregated = {}
        
        for disaster in self.active_disasters.values():
            impacts = disaster.calculate_impact(cell_x, cell_y)
            for infra, damage in impacts.items():
                aggregated[infra] = max(
                    aggregated.get(infra, 0.0), damage
                )  # Use max for cascading effects
        
        return aggregated

    def get_active_disaster_count(self) -> int:
        """Return count of active disasters."""
        return len(self.active_disasters)

    def get_active_disasters_by_type(self) -> Dict[str, int]:
        """Return count of active disasters per type."""
        counts = {}
        for disaster in self.active_disasters.values():
            dtype = disaster.event.disaster_type.value
            counts[dtype] = counts.get(dtype, 0) + 1
        return counts

    def get_summary(self) -> Dict:
        """Get summary statistics of all active disasters."""
        summary = {
            "active_disaster_count": self.get_active_disaster_count(),
            "by_type": self.get_active_disasters_by_type(),
            "total_cumulative_impact": sum(
                d.total_impact for d in self.active_disasters.values()
            ),
            "affected_cells": set(),
        }
        
        # Aggregate affected cells
        for disaster in self.active_disasters.values():
            summary["affected_cells"].update(disaster.affected_cells.keys())
        summary["affected_cells"] = len(summary["affected_cells"])
        
        return summary
