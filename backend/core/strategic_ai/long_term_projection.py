"""
Long-Term Projection - Project long-term disaster recovery outcomes
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ProjectionModel(Enum):
    """Projection model types"""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGISTIC = "logistic"
    CUSTOM = "custom"


class LongTermProjection:
    """
    Projects long-term outcomes of disaster response strategies.
    Models recovery trajectories over months/years.
    """
    
    def __init__(self, model_type: ProjectionModel = ProjectionModel.LOGISTIC):
        self.model_type = model_type
        self.projections: List[Dict] = []
    
    def project_recovery(
        self,
        initial_state: Dict[str, float],
        interventions: List[Dict],
        time_horizon_days: int = 365
    ) -> Dict:
        """
        Project recovery trajectory.
        
        Args:
            initial_state: Initial post-disaster state
            interventions: List of planned interventions
            time_horizon_days: Projection time horizon
        
        Returns:
            Recovery projection over time
        """
        trajectory = []
        current_state = initial_state.copy()
        
        # Project state for each time step
        for day in range(time_horizon_days):
            # Apply interventions scheduled for this day
            for intervention in interventions:
                if intervention.get("start_day", 0) <= day < intervention.get("end_day", 0):
                    current_state = self._apply_intervention(current_state, intervention)
            
            # Apply recovery dynamics
            current_state = self._apply_recovery_dynamics(current_state, day)
            
            # Record state
            if day % 30 == 0:  # Monthly snapshots
                trajectory.append({
                    "day": day,
                    "month": day // 30,
                    "state": current_state.copy()
                })
        
        projection = {
            "model_type": self.model_type.value,
            "time_horizon_days": time_horizon_days,
            "trajectory": trajectory,
            "final_state": current_state,
            "recovery_metrics": self._calculate_recovery_metrics(initial_state, current_state)
        }
        
        self.projections.append(projection)
        return projection
    
    def _apply_intervention(
        self,
        state: Dict[str, float],
        intervention: Dict
    ) -> Dict[str, float]:
        """Apply intervention effects to state"""
        new_state = state.copy()
        
        effects = intervention.get("effects", {})
        for key, value in effects.items():
            new_state[key] = new_state.get(key, 0) + value
        
        return new_state
    
    def _apply_recovery_dynamics(
        self,
        state: Dict[str, float],
        day: int
    ) -> Dict[str, float]:
        """Apply natural recovery dynamics"""
        new_state = state.copy()
        
        if self.model_type == ProjectionModel.LINEAR:
            # Linear recovery
            recovery_rate = 0.001  # 0.1% per day
            for key in ["infrastructure_health", "economic_activity"]:
                if key in new_state:
                    new_state[key] = min(1.0, new_state[key] + recovery_rate)
        
        elif self.model_type == ProjectionModel.EXPONENTIAL:
            # Exponential recovery (fast initially, slows down)
            for key in ["infrastructure_health", "economic_activity"]:
                if key in new_state:
                    current = new_state[key]
                    new_state[key] = 1.0 - (1.0 - current) * 0.99  # 1% improvement of gap
        
        elif self.model_type == ProjectionModel.LOGISTIC:
            # Logistic growth (S-curve)
            for key in ["infrastructure_health", "economic_activity"]:
                if key in new_state:
                    current = new_state[key]
                    growth_rate = 0.01
                    carrying_capacity = 1.0
                    new_state[key] = current + growth_rate * current * (1 - current / carrying_capacity)
        
        return new_state
    
    def _calculate_recovery_metrics(
        self,
        initial_state: Dict[str, float],
        final_state: Dict[str, float]
    ) -> Dict:
        """Calculate recovery metrics"""
        metrics = {}
        
        for key in initial_state:
            if key in final_state:
                initial = initial_state[key]
                final = final_state[key]
                
                if initial < 1.0:
                    recovery_pct = (final - initial) / (1.0 - initial) if initial < 1.0 else 1.0
                else:
                    recovery_pct = 1.0
                
                metrics[f"{key}_recovery"] = min(1.0, max(0.0, recovery_pct))
        
        # Overall recovery score
        if metrics:
            metrics["overall_recovery"] = sum(metrics.values()) / len(metrics)
        
        return metrics
    
    def compare_projections(
        self,
        projection_ids: List[int]
    ) -> Dict:
        """Compare multiple projections"""
        if not self.projections:
            return {"error": "No projections available"}
        
        projections_to_compare = [
            self.projections[i]
            for i in projection_ids
            if i < len(self.projections)
        ]
        
        if not projections_to_compare:
            return {"error": "Invalid projection IDs"}
        
        comparison = {
            "projections_compared": len(projections_to_compare),
            "projections": projections_to_compare,
            "best_recovery": max(
                projections_to_compare,
                key=lambda p: p["recovery_metrics"].get("overall_recovery", 0)
            )
        }
        
        return comparison
    
    def get_projections(self) -> List[Dict]:
        """Get all projections"""
        return self.projections
