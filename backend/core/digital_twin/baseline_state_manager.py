"""
Baseline State Manager - Save and compare pre/post-disaster states
"""

from typing import Dict, Optional, Any
from datetime import datetime
import json
from pathlib import Path


class BaselineStateManager:
    """
    Manages baseline state capture and comparison.
    Allows saving pre-disaster state and comparing with current state.
    """
    
    def __init__(self):
        self.baseline_snapshot: Optional[Dict] = None
        self.comparison_metrics: Dict = {}
        self.baseline_timestamp: Optional[datetime] = None
    
    def capture_baseline(self, city_model, population_model=None, economic_model=None, asset_registry=None) -> Dict:
        """
        Capture complete baseline state from all models.
        
        Args:
            city_model: CityModel instance
            population_model: PopulationModel instance (optional)
            economic_model: EconomicModel instance (optional)
            asset_registry: CriticalAssetRegistry instance (optional)
        
        Returns:
            Complete baseline snapshot
        """
        self.baseline_timestamp = datetime.utcnow()
        
        snapshot = {
            "timestamp": self.baseline_timestamp.isoformat(),
            "city_metrics": self._capture_city_metrics(city_model),
            "infrastructure": self._capture_infrastructure_state(city_model),
            "population": self._capture_population_state(population_model) if population_model else {},
            "economy": self._capture_economic_state(economic_model) if economic_model else {},
            "critical_assets": self._capture_asset_state(asset_registry) if asset_registry else {},
            "grid_state": self._capture_grid_state(city_model)
        }
        
        self.baseline_snapshot = snapshot
        return snapshot
    
    def _capture_city_metrics(self, city_model) -> Dict:
        """Capture city-level metrics"""
        metrics = city_model.calculate_city_metrics()
        return {
            "population": city_model.total_population,
            "gdp": city_model.gdp,
            "area_km2": city_model.total_area_km2,
            "employment_rate": metrics.employment_rate,
            "infrastructure_health": metrics.infrastructure_health,
            "resilience_score": metrics.resilience_score
        }
    
    def _capture_infrastructure_state(self, city_model) -> Dict:
        """Capture infrastructure state"""
        if not city_model.infrastructure_graph:
            return {}
        
        infra_graph = city_model.infrastructure_graph
        
        # Count nodes by type and health
        nodes_by_type = {}
        total_health = 0.0
        
        for node in infra_graph.nodes.values():
            node_type = node.node_type.value
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = {"count": 0, "total_health": 0.0}
            
            nodes_by_type[node_type]["count"] += 1
            nodes_by_type[node_type]["total_health"] += node.capacity
            total_health += node.capacity
        
        # Calculate average health by type
        for node_type in nodes_by_type:
            count = nodes_by_type[node_type]["count"]
            nodes_by_type[node_type]["avg_health"] = (
                nodes_by_type[node_type]["total_health"] / count if count > 0 else 0.0
            )
        
        return {
            "total_nodes": len(infra_graph.nodes),
            "average_health": total_health / len(infra_graph.nodes) if infra_graph.nodes else 0.0,
            "nodes_by_type": nodes_by_type
        }
    
    def _capture_population_state(self, population_model) -> Dict:
        """Capture population state"""
        return {
            "total_population": population_model.total_population,
            "demographics": population_model.demographics.to_dict(),
            "casualties": population_model.casualties,
            "displaced": population_model.displaced,
            "population_by_zone": population_model.population_by_zone.copy()
        }
    
    def _capture_economic_state(self, economic_model) -> Dict:
        """Capture economic state"""
        return {
            "gdp": economic_model.gdp,
            "baseline_gdp": economic_model.baseline_gdp,
            "total_economic_loss": economic_model.total_economic_loss,
            "business_continuity_index": economic_model.business_continuity_index,
            "employment_rate": economic_model.employment_rate,
            "sectors": {k: v.to_dict() for k, v in economic_model.sectors.items()}
        }
    
    def _capture_asset_state(self, asset_registry) -> Dict:
        """Capture critical asset state"""
        summary = asset_registry.get_operational_summary()
        
        return {
            "total_assets": summary["total_assets"],
            "operational_assets": summary["operational_assets"],
            "by_type": summary["by_type"],
            "assets": [asset.to_dict() for asset in asset_registry.assets.values()]
        }
    
    def _capture_grid_state(self, city_model) -> Dict:
        """Capture grid state"""
        if not city_model.grid_manager:
            return {}
        
        grid = city_model.grid_manager
        
        # Count cells by state
        cells_by_state = {}
        total_cells = len(grid.cells)
        
        for cell in grid.cells.values():
            state = cell.state.value
            cells_by_state[state] = cells_by_state.get(state, 0) + 1
        
        return {
            "total_cells": total_cells,
            "width": grid.width,
            "height": grid.height,
            "cells_by_state": cells_by_state,
            "cells_at_risk": cells_by_state.get("at_risk", 0)
        }
    
    def compare_to_baseline(self, current_state: Dict) -> Dict:
        """
        Compare current state to baseline and calculate deviations.
        
        Args:
            current_state: Current state snapshot (same format as baseline)
        
        Returns:
            Comparison metrics showing deviations
        """
        if not self.baseline_snapshot:
            return {"error": "No baseline snapshot available"}
        
        baseline = self.baseline_snapshot
        
        comparison = {
            "baseline_timestamp": baseline["timestamp"],
            "comparison_timestamp": current_state.get("timestamp", datetime.utcnow().isoformat()),
            "city_metrics_deviation": self._compare_city_metrics(
                baseline.get("city_metrics", {}),
                current_state.get("city_metrics", {})
            ),
            "infrastructure_deviation": self._compare_infrastructure(
                baseline.get("infrastructure", {}),
                current_state.get("infrastructure", {})
            ),
            "population_impact": self._compare_population(
                baseline.get("population", {}),
                current_state.get("population", {})
            ),
            "economic_impact": self._compare_economy(
                baseline.get("economy", {}),
                current_state.get("economy", {})
            ),
            "asset_impact": self._compare_assets(
                baseline.get("critical_assets", {}),
                current_state.get("critical_assets", {})
            )
        }
        
        self.comparison_metrics = comparison
        return comparison
    
    def _compare_city_metrics(self, baseline: Dict, current: Dict) -> Dict:
        """Compare city-level metrics"""
        return {
            "population_change": current.get("population", 0) - baseline.get("population", 0),
            "gdp_change": current.get("gdp", 0) - baseline.get("gdp", 0),
            "infrastructure_health_change": (
                current.get("infrastructure_health", 0) - baseline.get("infrastructure_health", 0)
            ),
            "resilience_score_change": (
                current.get("resilience_score", 0) - baseline.get("resilience_score", 0)
            )
        }
    
    def _compare_infrastructure(self, baseline: Dict, current: Dict) -> Dict:
        """Compare infrastructure state"""
        return {
            "health_degradation": (
                baseline.get("average_health", 1.0) - current.get("average_health", 1.0)
            ),
            "nodes_affected": (
                baseline.get("total_nodes", 0) - current.get("total_nodes", 0)
            )
        }
    
    def _compare_population(self, baseline: Dict, current: Dict) -> Dict:
        """Compare population state"""
        return {
            "casualties": current.get("casualties", 0),
            "displaced": current.get("displaced", 0),
            "population_affected": (
                baseline.get("total_population", 0) - current.get("total_population", 0)
            ),
            "casualty_rate": (
                current.get("casualties", 0) / baseline.get("total_population", 1)
                if baseline.get("total_population", 0) > 0 else 0.0
            )
        }
    
    def _compare_economy(self, baseline: Dict, current: Dict) -> Dict:
        """Compare economic state"""
        return {
            "economic_loss": current.get("total_economic_loss", 0),
            "gdp_loss": baseline.get("gdp", 0) - current.get("gdp", 0),
            "business_continuity_drop": (
                baseline.get("business_continuity_index", 1.0) -
                current.get("business_continuity_index", 1.0)
            )
        }
    
    def _compare_assets(self, baseline: Dict, current: Dict) -> Dict:
        """Compare critical assets state"""
        return {
            "assets_failed": (
                baseline.get("operational_assets", 0) - current.get("operational_assets", 0)
            ),
            "failure_rate": (
                (baseline.get("operational_assets", 0) - current.get("operational_assets", 0)) /
                baseline.get("total_assets", 1)
                if baseline.get("total_assets", 0) > 0 else 0.0
            )
        }
    
    def generate_impact_report(self) -> Dict:
        """Generate comprehensive impact report"""
        if not self.comparison_metrics:
            return {"error": "No comparison metrics available. Run compare_to_baseline first."}
        
        metrics = self.comparison_metrics
        
        # Calculate overall impact severity (0.0 to 1.0)
        severity_factors = [
            abs(metrics.get("city_metrics_deviation", {}).get("infrastructure_health_change", 0)),
            abs(metrics.get("city_metrics_deviation", {}).get("resilience_score_change", 0)),
            metrics.get("population_impact", {}).get("casualty_rate", 0),
            abs(metrics.get("economic_impact", {}).get("business_continuity_drop", 0)),
            metrics.get("asset_impact", {}).get("failure_rate", 0)
        ]
        
        overall_severity = sum(severity_factors) / len(severity_factors) if severity_factors else 0.0
        
        return {
            "overall_severity": overall_severity,
            "severity_level": self._get_severity_level(overall_severity),
            "key_impacts": {
                "casualties": metrics.get("population_impact", {}).get("casualties", 0),
                "displaced": metrics.get("population_impact", {}).get("displaced", 0),
                "economic_loss": metrics.get("economic_impact", {}).get("economic_loss", 0),
                "assets_failed": metrics.get("asset_impact", {}).get("assets_failed", 0),
                "infrastructure_degradation": metrics.get("infrastructure_deviation", {}).get("health_degradation", 0)
            },
            "detailed_metrics": metrics
        }
    
    def _get_severity_level(self, severity: float) -> str:
        """Convert severity score to level"""
        if severity < 0.2:
            return "Minor"
        elif severity < 0.4:
            return "Moderate"
        elif severity < 0.6:
            return "Significant"
        elif severity < 0.8:
            return "Severe"
        else:
            return "Catastrophic"
    
    def save_baseline(self, file_path: str) -> None:
        """Save baseline snapshot to file"""
        if not self.baseline_snapshot:
            raise ValueError("No baseline snapshot to save")
        
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.baseline_snapshot, f, indent=2)
    
    def load_baseline(self, file_path: str) -> Dict:
        """Load baseline snapshot from file"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Baseline file not found: {file_path}")
        
        with open(path, 'r') as f:
            self.baseline_snapshot = json.load(f)
        
        # Parse timestamp
        if "timestamp" in self.baseline_snapshot:
            self.baseline_timestamp = datetime.fromisoformat(
                self.baseline_snapshot["timestamp"]
            )
        
        return self.baseline_snapshot
