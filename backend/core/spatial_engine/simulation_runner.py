"""Simulation runner — orchestrates grid simulation over time."""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
from .grid_manager import GridManager
from .grid_cell import GridCell, CellState
from .diffusion_model import DiffusionModel
from .zoning_engine import ZoningEngine
from .spatial_risk_calculator import SpatialRiskCalculator
from .grid_visual_exporter import GridVisualExporter


@dataclass
class SimulationEvent:
    """A simulation event (disaster, intervention, etc.)."""

    event_id: str
    event_type: str  # "disaster_initiate", "intervention_apply", "recovery_start"
    timestamp: int  # simulation time step
    location: tuple = (0, 0)  # (x, y)
    parameters: Dict = field(default_factory=dict)
    affected_cells: List[str] = field(default_factory=list)


class GridSimulationRunner:
    """Orchestrates grid-based simulation over time."""

    def __init__(
        self,
        grid: GridManager,
        diffusion_model: Optional[DiffusionModel] = None,
        zoning_engine: Optional[ZoningEngine] = None,
    ):
        """Initialize simulation runner."""
        self.grid = grid
        self.diffusion_model = diffusion_model or DiffusionModel(grid)
        self.zoning_engine = zoning_engine or ZoningEngine(grid)
        self.risk_calc = SpatialRiskCalculator(grid)
        self.exporter = GridVisualExporter(grid)

        # Simulation state
        self.current_time = 0
        self.total_steps = 0
        self.is_running = False
        self.simulation_config = {}

        # History
        self.history: List[Dict] = []
        self.events: List[SimulationEvent] = []
        self.event_callbacks: Dict[str, List[Callable]] = {}

    def configure(
        self,
        duration: int = 100,
        diffusion_enabled: bool = True,
        recovery_enabled: bool = True,
        cascading_enabled: bool = True,
    ) -> None:
        """Configure simulation parameters."""
        self.simulation_config = {
            "duration": duration,
            "diffusion_enabled": diffusion_enabled,
            "recovery_enabled": recovery_enabled,
            "cascading_enabled": cascading_enabled,
        }

    def register_event_callback(self, event_type: str, callback: Callable) -> None:
        """Register callback for event type."""
        if event_type not in self.event_callbacks:
            self.event_callbacks[event_type] = []
        self.event_callbacks[event_type].append(callback)

    def trigger_event(self, event: SimulationEvent) -> None:
        """Trigger and log an event."""
        self.events.append(event)
        if event.event_type in self.event_callbacks:
            for callback in self.event_callbacks[event.event_type]:
                callback(event)

    def initiate_disaster(
        self,
        x: int,
        y: int,
        disaster_type: str,
        intensity: float,
        radius: int = 2,
    ) -> SimulationEvent:
        """
        Initiate a disaster at location (x, y).

        Args:
            x, y: Grid coordinates
            disaster_type: flood, seismic, wildfire, pandemic, cyber
            intensity: Initial intensity (0-1)
            radius: Affected radius in cells

        Returns:
            SimulationEvent
        """
        disaster_type = disaster_type.lower()
        intensity = min(1.0, max(0.0, intensity))

        neighbors = self.grid.get_neighborhood_radius(x, y, radius=radius)
        affected_cell_ids = []

        intensity_attr = {
            "flood": "flood_intensity",
            "seismic": "seismic_intensity",
            "wildfire": "wildfire_intensity",
            "pandemic": "pandemic_spread",
            "cyber": "cyber_risk",
        }.get(disaster_type)

        if intensity_attr:
            # Apply to epicenter
            cell = self.grid.get_cell(x, y)
            if cell:
                setattr(cell, intensity_attr, intensity)
                cell.update_state_from_hazards()
                affected_cell_ids.append(cell.cell_id)

            # Apply to neighbors with decay
            for neighbor in neighbors:
                distance = (
                    ((neighbor.x - x) ** 2 + (neighbor.y - y) ** 2) ** 0.5 + 1
                )
                decayed_intensity = intensity * (0.5 ** (distance - 1))
                setattr(neighbor, intensity_attr, max(
                    getattr(neighbor, intensity_attr), decayed_intensity
                ))
                neighbor.update_state_from_hazards()
                affected_cell_ids.append(neighbor.cell_id)

        event = SimulationEvent(
            event_id=f"disaster_{len(self.events)}",
            event_type="disaster_initiate",
            timestamp=self.current_time,
            location=(x, y),
            parameters={
                "disaster_type": disaster_type,
                "intensity": intensity,
                "radius": radius,
            },
            affected_cells=affected_cell_ids,
        )
        self.trigger_event(event)
        return event

    def apply_intervention(
        self, zone_type: str, intervention_level: float, resource_level: float = 1.0
    ) -> SimulationEvent:
        """Apply policy/resource intervention to zone."""
        self.zoning_engine.apply_zone_intervention(zone_type, intervention_level)

        # Update cells
        if zone_type in self.zoning_engine.zones:
            for cell_id in self.zoning_engine.zones[zone_type]:
                x, y = map(int, cell_id.split(","))
                cell = self.grid.get_cell(x, y)
                if cell:
                    cell.resources_allocated[zone_type] = resource_level

        event = SimulationEvent(
            event_id=f"intervention_{len(self.events)}",
            event_type="intervention_apply",
            timestamp=self.current_time,
            parameters={
                "zone_type": zone_type,
                "intervention_level": intervention_level,
                "resource_level": resource_level,
            },
        )
        self.trigger_event(event)
        return event

    def step(self) -> None:
        """Execute one simulation time step."""
        if not self.simulation_config:
            self.configure()

        # 1. Propagate hazards if enabled
        if self.simulation_config.get("diffusion_enabled", True):
            self.diffusion_model.propagate_step(hazard_type="all")

        # 2. Cascade infrastructure damage
        if self.simulation_config.get("cascading_enabled", True):
            self.diffusion_model.cascade_infrastructure_damage()

        # 3. Apply recovery if enabled
        if self.simulation_config.get("recovery_enabled", True):
            for cell in self.grid.get_all_cells():
                cell.apply_recovery()

        # 4. Update cell states
        for cell in self.grid.get_all_cells():
            cell.update_state_from_hazards()
            if cell.state != CellState.HEALTHY:
                cell.time_affected += 1

        # 5. Record statistics
        stats = self.grid.calculate_statistics()
        stats["timestamp"] = self.current_time
        self.history.append(stats)

        self.current_time += 1

    def run(self, duration: Optional[int] = None) -> Dict:
        """
        Run simulation for specified duration.

        Args:
            duration: Number of time steps to run (default from config)

        Returns:
            Simulation summary
        """
        if not self.simulation_config:
            self.configure()

        if duration is None:
            duration = self.simulation_config.get("duration", 100)

        self.is_running = True
        self.current_time = 0
        self.history = []

        try:
            for step in range(duration):
                self.step()
        finally:
            self.is_running = False
            self.total_steps = self.current_time

        return self.get_summary()

    def pause(self) -> None:
        """Pause simulation."""
        self.is_running = False

    def resume(self, additional_steps: int = 100) -> Dict:
        """Resume paused simulation."""
        self.is_running = True
        try:
            for _ in range(additional_steps):
                if not self.is_running:
                    break
                self.step()
        finally:
            self.is_running = False

        return self.get_summary()

    def reset(self) -> None:
        """Reset simulation to initial state."""
        self.grid.reset()
        self.current_time = 0
        self.history = []
        self.events = []
        self.total_steps = 0
        self.is_running = False

    def get_summary(self) -> Dict:
        """Get simulation summary."""
        return {
            "total_steps": self.total_steps,
            "current_time": self.current_time,
            "is_running": self.is_running,
            "history_length": len(self.history),
            "events_count": len(self.events),
            "grid_statistics": self.grid.calculate_statistics(),
            "final_frame": self.history[-1] if self.history else None,
        }

    def export_history(self) -> Dict:
        """Export full simulation history."""
        return {
            "config": self.simulation_config,
            "summary": self.get_summary(),
            "history": self.history,
            "events": [
                {
                    "event_id": e.event_id,
                    "event_type": e.event_type,
                    "timestamp": e.timestamp,
                    "location": e.location,
                    "parameters": e.parameters,
                }
                for e in self.events
            ],
        }

    def save_to_file(self, filepath: str) -> None:
        """Save simulation history to JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.export_history(), f, indent=2)

    def load_from_file(self, filepath: str) -> None:
        """Load simulation history from JSON file (for replay)."""
        with open(filepath, "r") as f:
            data = json.load(f)
            self.simulation_config = data.get("config", {})
            # Note: full state restoration would require more work
