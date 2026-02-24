"""
City Model - Top-level city state and behavior
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class CityMetrics:
    """City-level metrics"""
    total_population: int
    gdp: float
    employment_rate: float
    infrastructure_health: float
    resilience_score: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        return {
            "total_population": self.total_population,
            "gdp": self.gdp,
            "employment_rate": self.employment_rate,
            "infrastructure_health": self.infrastructure_health,
            "resilience_score": self.resilience_score,
            "timestamp": self.timestamp.isoformat()
        }


class CityModel:
    """
    Top-level city model that manages city state and behavior.
    Integrates with grid, infrastructure, population, and economic models.
    """
    
    def __init__(
        self,
        city_id: str,
        name: str,
        total_population: int,
        total_area_km2: float,
        gdp: float,
        grid_manager=None,
        infrastructure_graph=None
    ):
        self.city_id = city_id
        self.name = name
        self.total_population = total_population
        self.total_area_km2 = total_area_km2
        self.gdp = gdp
        
        # References to other systems
        self.grid_manager = grid_manager
        self.infrastructure_graph = infrastructure_graph
        
        # State tracking
        self.baseline_state: Optional[Dict] = None
        self.current_state: Dict = {}
        self.metrics_history: List[CityMetrics] = []
        
        # Initialize baseline
        self.initialize_baseline()
    
    def initialize_baseline(self) -> None:
        """Capture initial city state as baseline"""
        self.baseline_state = {
            "city_id": self.city_id,
            "name": self.name,
            "total_population": self.total_population,
            "total_area_km2": self.total_area_km2,
            "gdp": self.gdp,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.current_state = self.baseline_state.copy()
    
    def update_state(self, time_step: int) -> None:
        """Update city state for current time step"""
        metrics = self.calculate_city_metrics()
        self.metrics_history.append(metrics)
        
        self.current_state.update({
            "time_step": time_step,
            "metrics": metrics.to_dict(),
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def calculate_city_metrics(self) -> CityMetrics:
        """Calculate current city-level metrics"""
        # Calculate infrastructure health
        infra_health = 1.0
        if self.infrastructure_graph:
            try:
                total_nodes = len(self.infrastructure_graph.nodes)
                if total_nodes > 0:
                    operational_nodes = sum(
                        1 for node in self.infrastructure_graph.nodes.values()
                        if node.capacity > 0.5
                    )
                    infra_health = operational_nodes / total_nodes
            except Exception:
                infra_health = 1.0
        
        # Calculate resilience score (simplified)
        resilience = self._calculate_resilience_score(infra_health)
        
        return CityMetrics(
            total_population=self.total_population,
            gdp=self.gdp,
            employment_rate=0.95,  # Default, will be updated by economic model
            infrastructure_health=infra_health,
            resilience_score=resilience
        )
    
    def _calculate_resilience_score(self, infra_health: float) -> float:
        """
        Calculate city resilience score based on multiple factors.
        Score ranges from 0.0 (no resilience) to 1.0 (maximum resilience)
        """
        # Factors: infrastructure health, population density, economic strength
        population_density = self.total_population / self.total_area_km2
        
        # Normalize population density (assume 1000 people/km2 is optimal)
        density_factor = min(population_density / 1000.0, 1.0)
        
        # Economic factor (GDP per capita)
        gdp_per_capita = self.gdp / self.total_population if self.total_population > 0 else 0
        economic_factor = min(gdp_per_capita / 50000.0, 1.0)  # Assume $50k is optimal
        
        # Weighted average
        resilience = (
            infra_health * 0.5 +
            density_factor * 0.2 +
            economic_factor * 0.3
        )
        
        return max(0.0, min(1.0, resilience))
    
    def get_resilience_score(self) -> float:
        """Get current resilience score"""
        metrics = self.calculate_city_metrics()
        return metrics.resilience_score
    
    def export_state(self) -> Dict:
        """Export current city state"""
        return {
            "city_id": self.city_id,
            "name": self.name,
            "current_state": self.current_state,
            "baseline_state": self.baseline_state,
            "metrics_history": [m.to_dict() for m in self.metrics_history[-10:]],  # Last 10
            "grid_size": (
                f"{self.grid_manager.width}x{self.grid_manager.height}"
                if self.grid_manager else "N/A"
            ),
            "infrastructure_nodes": (
                len(self.infrastructure_graph.nodes)
                if self.infrastructure_graph else 0
            )
        }
    
    def get_status_summary(self) -> Dict:
        """Get concise status summary"""
        metrics = self.calculate_city_metrics()
        
        return {
            "city_id": self.city_id,
            "name": self.name,
            "population": self.total_population,
            "area_km2": self.total_area_km2,
            "gdp": self.gdp,
            "infrastructure_health": f"{metrics.infrastructure_health * 100:.1f}%",
            "resilience_score": f"{metrics.resilience_score:.3f}",
            "employment_rate": f"{metrics.employment_rate * 100:.1f}%"
        }
    
    def reset_to_baseline(self) -> None:
        """Reset city to baseline state"""
        if self.baseline_state:
            self.current_state = self.baseline_state.copy()
            self.metrics_history.clear()
