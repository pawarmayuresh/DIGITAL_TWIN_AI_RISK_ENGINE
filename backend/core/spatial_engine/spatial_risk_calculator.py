"""Spatial risk calculator and heatmap generator."""

from typing import Dict, List, Tuple, Optional
import numpy as np
from .grid_manager import GridManager
from .grid_cell import GridCell


class SpatialRiskCalculator:
    """Calculates spatial risk metrics and heatmaps."""

    def __init__(self, grid: GridManager):
        """Initialize risk calculator."""
        self.grid = grid

    def calculate_cell_risk_score(self, cell: GridCell) -> float:
        """
        Calculate overall risk score for a cell (0-1).

        Risk = f(hazard, infrastructure, population, intervention)
        """
        hazard_level = cell.get_total_hazard_level()  # 0-1
        infra_health = cell.get_infrastructure_health()  # 0-1 (higher = better)
        pop_factor = min(1.0, cell.metadata.population_density / 200.0)  # normalized
        intervention_factor = 1.0 - cell.intervention_level * 0.5  # intervention reduces risk

        risk = (hazard_level * 0.4 + (1.0 - infra_health) * 0.3 + pop_factor * 0.2) * (
            intervention_factor
        )
        return min(1.0, risk)

    def calculate_risk_heatmap(self) -> np.ndarray:
        """Generate risk heatmap (2D array)."""
        heatmap = np.zeros((self.grid.height, self.grid.width))

        for cell in self.grid.get_all_cells():
            risk_score = self.calculate_cell_risk_score(cell)
            heatmap[cell.y, cell.x] = risk_score

        return heatmap

    def calculate_hazard_heatmap(self, hazard_type: str) -> np.ndarray:
        """Generate heatmap for specific hazard type."""
        heatmap = np.zeros((self.grid.height, self.grid.width))

        hazard_attr = {
            "flood": "flood_intensity",
            "seismic": "seismic_intensity",
            "wildfire": "wildfire_intensity",
            "pandemic": "pandemic_spread",
            "cyber": "cyber_risk",
        }.get(hazard_type)

        if not hazard_attr:
            return heatmap

        for cell in self.grid.get_all_cells():
            intensity = getattr(cell, hazard_attr, 0.0)
            heatmap[cell.y, cell.x] = intensity

        return heatmap

    def calculate_infrastructure_health_heatmap(self, infra_type: str) -> np.ndarray:
        """Generate heatmap for specific infrastructure type."""
        heatmap = np.zeros((self.grid.height, self.grid.width))

        infra_attr = {
            "power": "power_grid_health",
            "water": "water_network_health",
            "transport": "transport_network_health",
            "healthcare": "healthcare_capacity",
            "communication": "communication_health",
        }.get(infra_type)

        if not infra_attr:
            return heatmap

        for cell in self.grid.get_all_cells():
            health = getattr(cell, infra_attr, 1.0)
            heatmap[cell.y, cell.x] = health

        return heatmap

    def calculate_vulnerability_heatmap(self) -> np.ndarray:
        """Generate vulnerability heatmap (population exposure * hazard)."""
        heatmap = np.zeros((self.grid.height, self.grid.width))

        for cell in self.grid.get_all_cells():
            pop_factor = min(1.0, cell.metadata.population_density / 200.0)
            hazard = cell.get_total_hazard_level()
            vulnerability = pop_factor * hazard
            heatmap[cell.y, cell.x] = vulnerability

        return heatmap

    def calculate_cascading_impact_heatmap(self) -> np.ndarray:
        """Generate heatmap showing cascading failure impact."""
        heatmap = np.zeros((self.grid.height, self.grid.width))

        for cell in self.grid.get_all_cells():
            # Cascading impact = infrastructure failure affecting neighbors
            infra_impact = (
                (1.0 - cell.power_grid_health) * 0.3
                + (1.0 - cell.water_network_health) * 0.2
                + (1.0 - cell.transport_network_health) * 0.3
                + (1.0 - cell.communication_health) * 0.2
            )

            # Count affected neighbors
            neighbors = self.grid.get_neighbors(cell.x, cell.y)
            affected_neighbors = sum(
                1 for n in neighbors if n.state.value in ["affected", "damaged", "collapsed"]
            )

            cascading_score = infra_impact * (1.0 + affected_neighbors * 0.2)
            heatmap[cell.y, cell.x] = min(1.0, cascading_score)

        return heatmap

    def get_hotspots(self, heatmap: np.ndarray, threshold: float = 0.7) -> List[Tuple[int, int]]:
        """Identify high-risk hotspots in heatmap."""
        hotspots = []
        for y in range(heatmap.shape[0]):
            for x in range(heatmap.shape[1]):
                if heatmap[y, x] >= threshold:
                    hotspots.append((x, y))
        return hotspots

    def calculate_risk_metrics(self) -> Dict:
        """Calculate comprehensive risk metrics."""
        cells = self.grid.get_all_cells()
        risk_scores = [self.calculate_cell_risk_score(cell) for cell in cells]

        return {
            "average_risk": float(np.mean(risk_scores)),
            "max_risk": float(np.max(risk_scores)),
            "min_risk": float(np.min(risk_scores)),
            "high_risk_cells": sum(1 for rs in risk_scores if rs > 0.7),
            "medium_risk_cells": sum(1 for rs in risk_scores if 0.4 < rs <= 0.7),
            "low_risk_cells": sum(1 for rs in risk_scores if rs <= 0.4),
        }


class GeoMapper:
    """Manages geographic data and coordinate transformations."""

    def __init__(self, grid: GridManager, origin_lat: float = 0.0, origin_lon: float = 0.0):
        """
        Initialize geo mapper.

        Args:
            grid: GridManager instance
            origin_lat, origin_lon: Geographic coordinates of grid origin
        """
        self.grid = grid
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon

    def cell_to_latlon(self, x: int, y: int) -> Tuple[float, float]:
        """Convert grid coordinates to lat/lon."""
        # Simple linear conversion: 1 cell = 0.001 degrees
        lat = self.origin_lat + y * 0.001
        lon = self.origin_lon + x * 0.001
        return lat, lon

    def latlon_to_cell(self, lat: float, lon: float) -> Tuple[int, int]:
        """Convert lat/lon to grid coordinates."""
        y = int((lat - self.origin_lat) / 0.001)
        x = int((lon - self.origin_lon) / 0.001)
        return x, y

    def get_cell_bounding_box(self, x: int, y: int) -> Dict[str, float]:
        """Get bounding box for a cell (lat/lon)."""
        lat_min, lon_min = self.cell_to_latlon(x, y)
        lat_max, lon_max = self.cell_to_latlon(x + 1, y + 1)

        return {
            "lat_min": min(lat_min, lat_max),
            "lat_max": max(lat_min, lat_max),
            "lon_min": min(lon_min, lon_max),
            "lon_max": max(lon_min, lon_max),
        }

    def export_geojson_heatmap(
        self, heatmap_name: str, heatmap: np.ndarray
    ) -> Dict:
        """Export heatmap as GeoJSON features."""
        features = []

        for y in range(heatmap.shape[0]):
            for x in range(heatmap.shape[1]):
                value = float(heatmap[y, x])
                bbox = self.get_cell_bounding_box(x, y)

                feature = {
                    "type": "Feature",
                    "properties": {
                        "x": x,
                        "y": y,
                        "value": value,
                        "heatmap": heatmap_name,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [bbox["lon_min"], bbox["lat_min"]],
                                [bbox["lon_max"], bbox["lat_min"]],
                                [bbox["lon_max"], bbox["lat_max"]],
                                [bbox["lon_min"], bbox["lat_max"]],
                                [bbox["lon_min"], bbox["lat_min"]],
                            ]
                        ],
                    },
                }
                features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features,
        }
