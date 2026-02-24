"""
Simulation Statistics Tracker - Tracks simulation performance metrics.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict
import statistics


class SimulationStatisticsTracker:
    """Tracks and analyzes simulation statistics."""
    
    def __init__(self):
        self.simulations: List[Dict[str, Any]] = []
        self.statistics_by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def record_simulation(
        self,
        simulation_id: str,
        disaster_type: str,
        duration_seconds: float,
        steps: int,
        final_state: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a simulation run."""
        record = {
            'simulation_id': simulation_id,
            'disaster_type': disaster_type,
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration_seconds,
            'steps': steps,
            'final_state': final_state,
            'metadata': metadata or {}
        }
        
        self.simulations.append(record)
        self.statistics_by_type[disaster_type].append(record)
    
    def get_statistics(self, disaster_type: Optional[str] = None) -> Dict[str, Any]:
        """Get simulation statistics."""
        sims = self.statistics_by_type[disaster_type] if disaster_type else self.simulations
        
        if not sims:
            return {'total_simulations': 0}
        
        durations = [s['duration_seconds'] for s in sims]
        steps = [s['steps'] for s in sims]
        
        return {
            'total_simulations': len(sims),
            'avg_duration_seconds': statistics.mean(durations),
            'avg_steps': statistics.mean(steps),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_runtime_hours': sum(durations) / 3600
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        if not self.simulations:
            return {}
        
        recent = self.simulations[-10:]
        durations = [s['duration_seconds'] for s in recent]
        
        return {
            'recent_avg_duration': statistics.mean(durations),
            'performance_trend': 'improving' if len(durations) > 1 and durations[-1] < durations[0] else 'stable'
        }
