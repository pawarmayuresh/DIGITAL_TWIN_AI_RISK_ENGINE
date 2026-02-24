"""
Twin Manager - Orchestrates all digital twin components
"""

from typing import Dict, Optional, Any
from datetime import datetime

from .city_model import CityModel
from .population_model import PopulationModel, Demographics
from .economic_model import EconomicModel
from .critical_asset_registry import CriticalAssetRegistry
from .baseline_state_manager import BaselineStateManager


class TwinManager:
    """
    Orchestrates all digital twin components.
    Manages simulation loop and integrates with disaster and cascading systems.
    """
    
    def __init__(self):
        # Core models
        self.city_model: Optional[CityModel] = None
        self.population_model: Optional[PopulationModel] = None
        self.economic_model: Optional[EconomicModel] = None
        self.asset_registry: Optional[CriticalAssetRegistry] = None
        self.baseline_manager: BaselineStateManager = BaselineStateManager()
        
        # External system references
        self.grid_manager = None
        self.disaster_manager = None
        self.cascade_engine = None
        self.infrastructure_graph = None
        
        # Simulation state
        self.current_time_step: int = 0
        self.is_initialized: bool = False
    
    def initialize_twin(
        self,
        city_id: str,
        city_name: str,
        total_population: int,
        total_area_km2: float,
        gdp: float,
        grid_manager=None,
        infrastructure_graph=None,
        disaster_manager=None,
        cascade_engine=None
    ) -> Dict:
        """
        Initialize complete digital twin with all components.
        
        Args:
            city_id: Unique city identifier
            city_name: City name
            total_population: Total population
            total_area_km2: Total area in square kilometers
            gdp: Annual GDP in dollars
            grid_manager: GridManager instance (optional)
            infrastructure_graph: InfrastructureGraph instance (optional)
            disaster_manager: DisasterManager instance (optional)
            cascade_engine: CascadingFailureEngine instance (optional)
        
        Returns:
            Initialization status
        """
        # Store external references
        self.grid_manager = grid_manager
        self.infrastructure_graph = infrastructure_graph
        self.disaster_manager = disaster_manager
        self.cascade_engine = cascade_engine
        
        # Initialize city model
        self.city_model = CityModel(
            city_id=city_id,
            name=city_name,
            total_population=total_population,
            total_area_km2=total_area_km2,
            gdp=gdp,
            grid_manager=grid_manager,
            infrastructure_graph=infrastructure_graph
        )
        
        # Initialize population model
        self.population_model = PopulationModel(
            total_population=total_population
        )
        
        # Initialize population on grid
        if grid_manager:
            self.population_model.initialize_population(grid_manager)
        
        # Initialize economic model
        total_employment = int(total_population * 0.6)  # 60% employment rate
        self.economic_model = EconomicModel(
            gdp=gdp,
            total_employment=total_employment
        )
        
        # Initialize critical asset registry
        self.asset_registry = CriticalAssetRegistry()
        
        # Create default assets if grid is available
        if grid_manager:
            self.asset_registry.initialize_default_assets(
                grid_manager.width,
                grid_manager.height
            )
        
        # Capture baseline state
        self.baseline_manager.capture_baseline(
            self.city_model,
            self.population_model,
            self.economic_model,
            self.asset_registry
        )
        
        self.is_initialized = True
        self.current_time_step = 0
        
        return {
            "status": "initialized",
            "city_id": city_id,
            "city_name": city_name,
            "population": total_population,
            "gdp": gdp,
            "critical_assets": len(self.asset_registry.assets),
            "grid_size": f"{grid_manager.width}x{grid_manager.height}" if grid_manager else "N/A"
        }
    
    def run_simulation_step(self, time_step: Optional[int] = None) -> Dict:
        """
        Run one simulation time step.
        Integrates disasters, cascades, and updates all models.
        
        Args:
            time_step: Time step number (optional, auto-increments if not provided)
        
        Returns:
            Twin status after time step
        """
        if not self.is_initialized:
            return {"error": "Twin not initialized. Call initialize_twin first."}
        
        # Update time step
        if time_step is not None:
            self.current_time_step = time_step
        else:
            self.current_time_step += 1
        
        # 1. Propagate disasters (if disaster manager available)
        if self.disaster_manager and self.grid_manager:
            self.disaster_manager.propagate_all(self.grid_manager, None)
        
        # 2. Calculate infrastructure cascades (if cascade engine available)
        if self.cascade_engine and self.infrastructure_graph:
            # Get disaster impacts
            disaster_impacts = {}
            if self.disaster_manager:
                for disaster in self.disaster_manager.active_disasters.values():
                    # Map disaster to infrastructure damage
                    pass  # Cascade engine handles this
            
            # Propagate failures
            try:
                self.cascade_engine.propagate_failures(
                    initial_failures=[],
                    time_step=self.current_time_step
                )
            except Exception:
                pass  # Continue even if cascade fails
        
        # 3. Update critical asset status
        if self.asset_registry and self.infrastructure_graph:
            self.asset_registry.update_asset_status(self.infrastructure_graph)
        
        # 4. Update population impacts
        if self.population_model and self.disaster_manager:
            # Get disaster impacts from spatial calculator
            disaster_impacts = self._get_disaster_impacts()
            self.population_model.update_population_status(disaster_impacts)
        
        # 5. Calculate economic impacts
        if self.economic_model and self.infrastructure_graph:
            infrastructure_status = self._get_infrastructure_status()
            self.economic_model.calculate_economic_loss(infrastructure_status)
        
        # 6. Update city state
        if self.city_model:
            self.city_model.update_state(self.current_time_step)
        
        return self.get_twin_status()
    
    def _get_disaster_impacts(self) -> Dict:
        """Get current disaster impacts"""
        if not self.disaster_manager or not self.grid_manager:
            return {}
        
        # Count affected cells and population
        total_cells_affected = 0
        population_affected = 0
        total_severity = 0.0
        
        for cell in self.grid_manager.cells.values():
            if cell.state.value in ["at_risk", "damaged", "destroyed"]:
                total_cells_affected += 1
                population_affected += int(cell.metadata.population_density)
                
                # Estimate severity from cell state
                severity_map = {
                    "at_risk": 0.3,
                    "damaged": 0.6,
                    "destroyed": 1.0
                }
                total_severity += severity_map.get(cell.state.value, 0.0)
        
        avg_severity = total_severity / total_cells_affected if total_cells_affected > 0 else 0.0
        
        return {
            "total_cells_affected": total_cells_affected,
            "population_affected": population_affected,
            "average_severity": avg_severity
        }
    
    def _get_infrastructure_status(self) -> Dict[str, float]:
        """Get infrastructure health by type"""
        if not self.infrastructure_graph:
            return {}
        
        # Group nodes by type and calculate average health
        status_by_type = {}
        
        for node in self.infrastructure_graph.nodes.values():
            node_type = node.node_type.value
            if node_type not in status_by_type:
                status_by_type[node_type] = {"total_health": 0.0, "count": 0}
            
            status_by_type[node_type]["total_health"] += node.capacity
            status_by_type[node_type]["count"] += 1
        
        # Calculate averages
        infrastructure_status = {}
        for node_type, data in status_by_type.items():
            infrastructure_status[node_type] = (
                data["total_health"] / data["count"] if data["count"] > 0 else 1.0
            )
        
        return infrastructure_status
    
    def get_twin_status(self) -> Dict:
        """Get comprehensive twin status"""
        if not self.is_initialized:
            return {"error": "Twin not initialized"}
        
        status = {
            "time_step": self.current_time_step,
            "timestamp": datetime.utcnow().isoformat(),
            "city": self.city_model.get_status_summary() if self.city_model else {},
            "population": self.population_model.get_status_summary() if self.population_model else {},
            "economy": self.economic_model.get_economic_summary() if self.economic_model else {},
            "critical_assets": self.asset_registry.get_operational_summary() if self.asset_registry else {},
            "active_disasters": (
                self.disaster_manager.get_active_disaster_count()
                if self.disaster_manager else 0
            )
        }
        
        return status
    
    def export_twin_state(self) -> Dict:
        """Export complete twin state"""
        if not self.is_initialized:
            return {"error": "Twin not initialized"}
        
        return {
            "city": self.city_model.export_state() if self.city_model else {},
            "population": self.population_model.get_status_summary() if self.population_model else {},
            "economy": self.economic_model.get_economic_summary() if self.economic_model else {},
            "critical_assets": (
                self.asset_registry.export_assets() if self.asset_registry else []
            ),
            "baseline": self.baseline_manager.baseline_snapshot,
            "current_time_step": self.current_time_step
        }
    
    def compare_to_baseline(self) -> Dict:
        """Compare current state to baseline"""
        if not self.is_initialized:
            return {"error": "Twin not initialized"}
        
        # Capture current state
        current_state = self.baseline_manager.capture_baseline(
            self.city_model,
            self.population_model,
            self.economic_model,
            self.asset_registry
        )
        
        # Compare
        comparison = self.baseline_manager.compare_to_baseline(current_state)
        
        return comparison
    
    def generate_impact_report(self) -> Dict:
        """Generate comprehensive impact report"""
        if not self.is_initialized:
            return {"error": "Twin not initialized"}
        
        # First compare to baseline
        self.compare_to_baseline()
        
        # Generate report
        return self.baseline_manager.generate_impact_report()
    
    def reset_to_baseline(self) -> None:
        """Reset all models to baseline state"""
        if not self.is_initialized:
            return
        
        if self.city_model:
            self.city_model.reset_to_baseline()
        
        if self.population_model:
            self.population_model.reset()
        
        if self.economic_model:
            self.economic_model.reset()
        
        self.current_time_step = 0
    
    def get_resilience_metrics(self) -> Dict:
        """Get comprehensive resilience metrics"""
        if not self.is_initialized:
            return {"error": "Twin not initialized"}
        
        return {
            "city_resilience_score": (
                self.city_model.get_resilience_score() if self.city_model else 0.0
            ),
            "infrastructure_health": (
                self.city_model.calculate_city_metrics().infrastructure_health
                if self.city_model else 0.0
            ),
            "business_continuity": (
                self.economic_model.business_continuity_index
                if self.economic_model else 0.0
            ),
            "critical_asset_availability": (
                self.asset_registry.get_operational_summary()["operational_assets"] /
                self.asset_registry.get_operational_summary()["total_assets"]
                if self.asset_registry and self.asset_registry.get_operational_summary()["total_assets"] > 0
                else 0.0
            ),
            "population_vulnerability": (
                self.population_model.get_population_vulnerability()["vulnerability_index"]
                if self.population_model else 0.0
            )
        }
