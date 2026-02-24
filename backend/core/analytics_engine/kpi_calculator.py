"""
KPI Calculator - Calculates Key Performance Indicators for disaster response.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class KPI:
    """Key Performance Indicator."""
    name: str
    value: float
    unit: str
    target: Optional[float] = None
    status: str = "unknown"  # 'good', 'warning', 'critical', 'unknown'
    trend: str = "stable"  # 'improving', 'stable', 'declining'
    
    def calculate_status(self):
        """Calculate KPI status based on target."""
        if self.target is None:
            self.status = "unknown"
            return
        
        ratio = self.value / self.target if self.target != 0 else 0
        
        # For metrics where lower is better (e.g., casualties, losses)
        if self.name in ['casualties', 'economic_loss', 'response_time']:
            if ratio <= 0.7:
                self.status = "good"
            elif ratio <= 1.0:
                self.status = "warning"
            else:
                self.status = "critical"
        # For metrics where higher is better (e.g., resources, efficiency)
        else:
            if ratio >= 1.0:
                self.status = "good"
            elif ratio >= 0.7:
                self.status = "warning"
            else:
                self.status = "critical"


class KPICalculator:
    """Calculates and tracks Key Performance Indicators."""
    
    def __init__(self):
        self.kpi_history: Dict[str, List[KPI]] = {}
        self.targets: Dict[str, float] = {
            'casualties': 100,
            'economic_loss': 1000000,
            'response_time': 60,
            'resources_utilized': 0.8,
            'infrastructure_preserved': 0.9,
            'population_evacuated': 0.95
        }
    
    def calculate_kpis(
        self,
        simulation_data: Dict[str, Any],
        scenario_id: Optional[str] = None
    ) -> Dict[str, KPI]:
        """Calculate all KPIs from simulation data."""
        
        kpis = {}
        
        # Response Effectiveness KPIs
        kpis['casualties'] = self._calculate_casualties_kpi(simulation_data)
        kpis['lives_saved'] = self._calculate_lives_saved_kpi(simulation_data)
        kpis['response_time'] = self._calculate_response_time_kpi(simulation_data)
        
        # Resource Efficiency KPIs
        kpis['resources_utilized'] = self._calculate_resource_utilization_kpi(simulation_data)
        kpis['resource_efficiency'] = self._calculate_resource_efficiency_kpi(simulation_data)
        
        # Infrastructure KPIs
        kpis['infrastructure_preserved'] = self._calculate_infrastructure_kpi(simulation_data)
        kpis['cascading_failures_prevented'] = self._calculate_cascading_kpi(simulation_data)
        
        # Population KPIs
        kpis['population_evacuated'] = self._calculate_evacuation_kpi(simulation_data)
        kpis['population_affected'] = self._calculate_affected_population_kpi(simulation_data)
        
        # Economic KPIs
        kpis['economic_loss'] = self._calculate_economic_loss_kpi(simulation_data)
        kpis['economic_efficiency'] = self._calculate_economic_efficiency_kpi(simulation_data)
        
        # Calculate status for each KPI
        for kpi in kpis.values():
            kpi.calculate_status()
        
        # Store in history
        for name, kpi in kpis.items():
            if name not in self.kpi_history:
                self.kpi_history[name] = []
            self.kpi_history[name].append(kpi)
            
            # Calculate trend
            if len(self.kpi_history[name]) > 1:
                kpi.trend = self._calculate_trend(name)
        
        return kpis
    
    def _calculate_casualties_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate casualties KPI."""
        casualties = data.get('casualties', 0)
        return KPI(
            name='casualties',
            value=casualties,
            unit='people',
            target=self.targets.get('casualties')
        )
    
    def _calculate_lives_saved_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate lives saved KPI."""
        initial_at_risk = data.get('initial_population_at_risk', 0)
        casualties = data.get('casualties', 0)
        lives_saved = max(0, initial_at_risk - casualties)
        
        return KPI(
            name='lives_saved',
            value=lives_saved,
            unit='people',
            target=initial_at_risk * 0.9 if initial_at_risk > 0 else None
        )
    
    def _calculate_response_time_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate response time KPI."""
        response_time = data.get('response_time', 0)
        return KPI(
            name='response_time',
            value=response_time,
            unit='minutes',
            target=self.targets.get('response_time')
        )
    
    def _calculate_resource_utilization_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate resource utilization KPI."""
        resources_used = data.get('resources_used', 0)
        resources_available = data.get('resources_available', 1)
        
        utilization = resources_used / resources_available if resources_available > 0 else 0
        
        return KPI(
            name='resources_utilized',
            value=utilization,
            unit='ratio',
            target=self.targets.get('resources_utilized')
        )
    
    def _calculate_resource_efficiency_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate resource efficiency KPI."""
        lives_saved = data.get('initial_population_at_risk', 0) - data.get('casualties', 0)
        resources_used = data.get('resources_used', 1)
        
        efficiency = lives_saved / resources_used if resources_used > 0 else 0
        
        return KPI(
            name='resource_efficiency',
            value=efficiency,
            unit='lives/resource',
            target=None
        )
    
    def _calculate_infrastructure_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate infrastructure preservation KPI."""
        infrastructure_health = data.get('infrastructure_health', 100) / 100.0
        
        return KPI(
            name='infrastructure_preserved',
            value=infrastructure_health,
            unit='ratio',
            target=self.targets.get('infrastructure_preserved')
        )
    
    def _calculate_cascading_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate cascading failures prevented KPI."""
        potential_cascades = data.get('potential_cascading_failures', 0)
        actual_cascades = data.get('actual_cascading_failures', 0)
        prevented = max(0, potential_cascades - actual_cascades)
        
        return KPI(
            name='cascading_failures_prevented',
            value=prevented,
            unit='count',
            target=potential_cascades if potential_cascades > 0 else None
        )
    
    def _calculate_evacuation_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate population evacuated KPI."""
        evacuated = data.get('population_evacuated', 0)
        at_risk = data.get('population_at_risk', 1)
        
        ratio = evacuated / at_risk if at_risk > 0 else 0
        
        return KPI(
            name='population_evacuated',
            value=ratio,
            unit='ratio',
            target=self.targets.get('population_evacuated')
        )
    
    def _calculate_affected_population_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate affected population KPI."""
        affected = data.get('population_affected', 0)
        
        return KPI(
            name='population_affected',
            value=affected,
            unit='people',
            target=None
        )
    
    def _calculate_economic_loss_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate economic loss KPI."""
        loss = data.get('economic_loss', 0)
        
        return KPI(
            name='economic_loss',
            value=loss,
            unit='currency',
            target=self.targets.get('economic_loss')
        )
    
    def _calculate_economic_efficiency_kpi(self, data: Dict[str, Any]) -> KPI:
        """Calculate economic efficiency KPI."""
        loss_prevented = data.get('economic_loss_prevented', 0)
        resources_spent = data.get('resources_spent', 1)
        
        efficiency = loss_prevented / resources_spent if resources_spent > 0 else 0
        
        return KPI(
            name='economic_efficiency',
            value=efficiency,
            unit='ratio',
            target=None
        )
    
    def _calculate_trend(self, kpi_name: str) -> str:
        """Calculate trend for a KPI."""
        history = self.kpi_history.get(kpi_name, [])
        
        if len(history) < 2:
            return "stable"
        
        recent = history[-3:] if len(history) >= 3 else history
        values = [kpi.value for kpi in recent]
        
        # Calculate simple trend
        if len(values) < 2:
            return "stable"
        
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        change = (second_half - first_half) / abs(first_half) if first_half != 0 else 0
        
        # For metrics where lower is better
        if kpi_name in ['casualties', 'economic_loss', 'response_time']:
            if change < -0.1:
                return "improving"
            elif change > 0.1:
                return "declining"
        # For metrics where higher is better
        else:
            if change > 0.1:
                return "improving"
            elif change < -0.1:
                return "declining"
        
        return "stable"
    
    def get_kpi_summary(self, kpis: Dict[str, KPI]) -> Dict[str, Any]:
        """Get summary of KPIs."""
        status_counts = {'good': 0, 'warning': 0, 'critical': 0, 'unknown': 0}
        trend_counts = {'improving': 0, 'stable': 0, 'declining': 0}
        
        for kpi in kpis.values():
            status_counts[kpi.status] += 1
            trend_counts[kpi.trend] += 1
        
        return {
            'total_kpis': len(kpis),
            'status_counts': status_counts,
            'trend_counts': trend_counts,
            'critical_kpis': [name for name, kpi in kpis.items() if kpi.status == 'critical'],
            'improving_kpis': [name for name, kpi in kpis.items() if kpi.trend == 'improving']
        }
    
    def set_target(self, kpi_name: str, target: float):
        """Set target for a KPI."""
        self.targets[kpi_name] = target
    
    def get_kpi_history(self, kpi_name: str, limit: int = 10) -> List[KPI]:
        """Get history for a specific KPI."""
        return self.kpi_history.get(kpi_name, [])[-limit:]
