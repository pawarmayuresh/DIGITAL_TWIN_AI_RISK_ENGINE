"""Grid visualization exporter — generates visual outputs."""

from typing import Dict, List
import json
import numpy as np
from .grid_manager import GridManager
from .spatial_risk_calculator import SpatialRiskCalculator


class GridVisualExporter:
    """Exports grid state as visual data (JSON, arrays, images)."""

    def __init__(self, grid: GridManager):
        """Initialize exporter."""
        self.grid = grid
        self.risk_calc = SpatialRiskCalculator(grid)

    def export_grid_as_json(self) -> Dict:
        """Export entire grid state as JSON."""
        return self.grid.to_dict()

    def export_heatmap_as_json(self, heatmap: np.ndarray) -> Dict:
        """Export heatmap as JSON array."""
        return {
            "width": heatmap.shape[1],
            "height": heatmap.shape[0],
            "data": heatmap.tolist(),
        }

    def export_cell_snapshot(self, x: int, y: int) -> Dict:
        """Export detailed state of a single cell."""
        cell = self.grid.get_cell(x, y)
        if not cell:
            return {}

        return cell.to_dict()

    def export_region_snapshot(self, x_min: int, y_min: int, x_max: int, y_max: int) -> Dict:
        """Export state of a rectangular region."""
        region_cells = []
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                cell = self.grid.get_cell(x, y)
                if cell:
                    region_cells.append(cell.to_dict())

        return {
            "region": {
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max,
            },
            "cells": region_cells,
        }

    def export_hazard_summary(self) -> Dict:
        """Export summary of all hazard types across grid."""
        heatmaps = {
            "risk": self.risk_calc.calculate_risk_heatmap(),
            "flood": self.risk_calc.calculate_hazard_heatmap("flood"),
            "seismic": self.risk_calc.calculate_hazard_heatmap("seismic"),
            "wildfire": self.risk_calc.calculate_hazard_heatmap("wildfire"),
            "pandemic": self.risk_calc.calculate_hazard_heatmap("pandemic"),
            "cyber": self.risk_calc.calculate_hazard_heatmap("cyber"),
        }

        return {
            heatmap_name: {
                "max": float(np.max(hm)),
                "min": float(np.min(hm)),
                "mean": float(np.mean(hm)),
            }
            for heatmap_name, hm in heatmaps.items()
        }

    def export_infrastructure_summary(self) -> Dict:
        """Export summary of infrastructure health across grid."""
        heatmaps = {
            "power": self.risk_calc.calculate_infrastructure_health_heatmap("power"),
            "water": self.risk_calc.calculate_infrastructure_health_heatmap("water"),
            "transport": self.risk_calc.calculate_infrastructure_health_heatmap("transport"),
            "healthcare": self.risk_calc.calculate_infrastructure_health_heatmap("healthcare"),
            "communication": self.risk_calc.calculate_infrastructure_health_heatmap("communication"),
        }

        return {
            infra_name: {
                "max": float(np.max(hm)),
                "min": float(np.min(hm)),
                "mean": float(np.mean(hm)),
            }
            for infra_name, hm in heatmaps.items()
        }

    def export_animation_frame(self, frame_number: int, timestamp: int) -> Dict:
        """Export current grid state as an animation frame."""
        return {
            "frame": frame_number,
            "timestamp": timestamp,
            "statistics": self.grid.calculate_statistics(),
            "hazard_summary": self.export_hazard_summary(),
            "infrastructure_summary": self.export_infrastructure_summary(),
            "risk_metrics": self.risk_calc.calculate_risk_metrics(),
        }

    def export_timeline_data(self, history: List[Dict]) -> Dict:
        """Export historical timeline data."""
        return {
            "timeline": history,
            "frames": len(history),
            "summary": {
                "start_state": history[0] if history else None,
                "end_state": history[-1] if history else None,
            },
        }

    def export_as_csv_compatible_dict(self) -> Dict[str, List]:
        """Export grid data in CSV-compatible format."""
        cells = self.grid.get_all_cells()
        data = {
            "cell_id": [],
            "x": [],
            "y": [],
            "state": [],
            "hazard_total": [],
            "flood": [],
            "seismic": [],
            "wildfire": [],
            "pandemic": [],
            "cyber": [],
            "power_health": [],
            "water_health": [],
            "transport_health": [],
            "healthcare_capacity": [],
            "communication_health": [],
            "population_density": [],
            "damage_level": [],
            "economic_loss": [],
        }

        for cell in cells:
            data["cell_id"].append(cell.cell_id)
            data["x"].append(cell.x)
            data["y"].append(cell.y)
            data["state"].append(cell.state.value)
            data["hazard_total"].append(cell.get_total_hazard_level())
            data["flood"].append(cell.flood_intensity)
            data["seismic"].append(cell.seismic_intensity)
            data["wildfire"].append(cell.wildfire_intensity)
            data["pandemic"].append(cell.pandemic_spread)
            data["cyber"].append(cell.cyber_risk)
            data["power_health"].append(cell.power_grid_health)
            data["water_health"].append(cell.water_network_health)
            data["transport_health"].append(cell.transport_network_health)
            data["healthcare_capacity"].append(cell.healthcare_capacity)
            data["communication_health"].append(cell.communication_health)
            data["population_density"].append(cell.metadata.population_density)
            data["damage_level"].append(cell.damage_level)
            data["economic_loss"].append(cell.economic_loss)

        return data
