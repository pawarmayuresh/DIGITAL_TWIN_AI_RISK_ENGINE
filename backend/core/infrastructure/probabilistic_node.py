"""
Probabilistic Infrastructure Node - BATCH 1
Replaces static health with probability distributions
"""
from typing import Dict, List, Tuple
from enum import Enum
import random


class NodeState(Enum):
    HEALTHY = "Healthy"
    DEGRADED = "Degraded"
    FAILED = "Failed"


class ProbabilisticNode:
    """Infrastructure node with probability distribution over states"""
    
    def __init__(
        self,
        node_id: str,
        node_type: str,
        p_healthy: float = 0.85,
        p_degraded: float = 0.10,
        p_failed: float = 0.05,
        latitude: float = 0.0,
        longitude: float = 0.0,
        ward: str = ""
    ):
        self.node_id = node_id
        self.node_type = node_type
        self.latitude = latitude
        self.longitude = longitude
        self.ward = ward
        
        # Probability distribution
        self.probabilities = {
            NodeState.HEALTHY: p_healthy,
            NodeState.DEGRADED: p_degraded,
            NodeState.FAILED: p_failed
        }
        
        # Normalize probabilities
        self._normalize_probabilities()
        
        # Dependencies
        self.parents: List[Tuple['ProbabilisticNode', float]] = []  # (node, weight)
        self.children: List[Tuple['ProbabilisticNode', float]] = []
        
        # History for temporal modeling
        self.previous_state = NodeState.HEALTHY
        self.state_history: List[NodeState] = []
        
    def _normalize_probabilities(self):
        """Ensure probabilities sum to 1"""
        total = sum(self.probabilities.values())
        if total > 0:
            for state in self.probabilities:
                self.probabilities[state] /= total
    
    def get_health_score(self) -> float:
        """Calculate health score from probability distribution"""
        return self.probabilities[NodeState.HEALTHY] * 100
    
    def get_risk_score(self) -> float:
        """Calculate risk score from failure probability"""
        return self.probabilities[NodeState.FAILED] * 100
    
    def get_degradation_score(self) -> float:
        """Calculate degradation score"""
        return self.probabilities[NodeState.DEGRADED] * 100
    
    def get_most_likely_state(self) -> NodeState:
        """Return most probable state"""
        return max(self.probabilities.items(), key=lambda x: x[1])[0]
    
    def update_probability(self, state: NodeState, delta: float):
        """Update probability for a state (with normalization)"""
        self.probabilities[state] = max(0.0, min(1.0, self.probabilities[state] + delta))
        self._normalize_probabilities()
    
    def set_probabilities(self, p_healthy: float, p_degraded: float, p_failed: float):
        """Set new probability distribution"""
        self.probabilities = {
            NodeState.HEALTHY: p_healthy,
            NodeState.DEGRADED: p_degraded,
            NodeState.FAILED: p_failed
        }
        self._normalize_probabilities()
    
    def add_parent(self, parent_node: 'ProbabilisticNode', weight: float):
        """Add parent dependency"""
        self.parents.append((parent_node, weight))
    
    def add_child(self, child_node: 'ProbabilisticNode', weight: float):
        """Add child dependency"""
        self.children.append((child_node, weight))
    
    def sample_state(self) -> NodeState:
        """Sample a state from probability distribution"""
        r = random.random()
        cumulative = 0.0
        
        for state, prob in self.probabilities.items():
            cumulative += prob
            if r <= cumulative:
                return state
        
        return NodeState.HEALTHY
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        health_score = self.get_health_score()
        return {
            "node_id": self.node_id,
            "type": self.node_type,
            "ward": self.ward,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "probabilities": {
                "healthy": self.probabilities[NodeState.HEALTHY],
                "degraded": self.probabilities[NodeState.DEGRADED],
                "failed": self.probabilities[NodeState.FAILED]
            },
            "health_score": health_score,
            "utility": health_score,  # Add utility field (same as health_score for compatibility)
            "risk_score": self.get_risk_score(),
            "degradation_score": self.get_degradation_score(),
            "most_likely_state": self.get_most_likely_state().value,
            "num_dependencies": len(self.parents) + len(self.children)
        }
