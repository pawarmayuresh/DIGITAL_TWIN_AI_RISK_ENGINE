"""
Reward Model - Calculates rewards for disaster response actions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class RewardWeights:
    """Weights for different reward components."""
    lives_saved: float = 10.0
    economic_impact: float = 0.001
    infrastructure_preserved: float = 5.0
    response_time: float = -0.1
    resource_efficiency: float = 2.0
    cascading_prevented: float = 8.0
    coalition_strength: float = 3.0


class RewardModel:
    """Calculates rewards for disaster response actions."""
    
    def __init__(self, weights: Optional[RewardWeights] = None):
        self.weights = weights or RewardWeights()
        self.reward_history: List[Dict[str, Any]] = []
    
    def calculate_reward(
        self,
        state_before: Dict[str, Any],
        action: Dict[str, Any],
        state_after: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate reward for a state transition."""
        
        # Extract metrics
        lives_saved = self._calculate_lives_saved(state_before, state_after)
        economic_impact = self._calculate_economic_impact(state_before, state_after)
        infrastructure_score = self._calculate_infrastructure_score(state_before, state_after)
        response_time_penalty = self._calculate_response_time_penalty(action)
        resource_efficiency = self._calculate_resource_efficiency(action, state_after)
        cascading_prevention = self._calculate_cascading_prevention(state_before, state_after)
        coalition_bonus = self._calculate_coalition_bonus(state_after)
        
        # Calculate weighted reward
        reward_components = {
            'lives_saved': lives_saved * self.weights.lives_saved,
            'economic_impact': economic_impact * self.weights.economic_impact,
            'infrastructure_preserved': infrastructure_score * self.weights.infrastructure_preserved,
            'response_time': response_time_penalty * self.weights.response_time,
            'resource_efficiency': resource_efficiency * self.weights.resource_efficiency,
            'cascading_prevented': cascading_prevention * self.weights.cascading_prevented,
            'coalition_strength': coalition_bonus * self.weights.coalition_strength
        }
        
        total_reward = sum(reward_components.values())
        
        reward_info = {
            'total_reward': total_reward,
            'components': reward_components,
            'raw_metrics': {
                'lives_saved': lives_saved,
                'economic_impact': economic_impact,
                'infrastructure_score': infrastructure_score,
                'response_time_penalty': response_time_penalty,
                'resource_efficiency': resource_efficiency,
                'cascading_prevention': cascading_prevention,
                'coalition_bonus': coalition_bonus
            }
        }
        
        self.reward_history.append(reward_info)
        return reward_info
    
    def _calculate_lives_saved(self, state_before: Dict, state_after: Dict) -> float:
        """Calculate lives saved metric."""
        casualties_before = state_before.get('casualties', 0)
        casualties_after = state_after.get('casualties', 0)
        return max(0, casualties_before - casualties_after)
    
    def _calculate_economic_impact(self, state_before: Dict, state_after: Dict) -> float:
        """Calculate economic impact (negative for losses)."""
        loss_before = state_before.get('economic_loss', 0)
        loss_after = state_after.get('economic_loss', 0)
        return loss_before - loss_after  # Positive if loss decreased
    
    def _calculate_infrastructure_score(self, state_before: Dict, state_after: Dict) -> float:
        """Calculate infrastructure preservation score."""
        infra_before = state_before.get('infrastructure_health', 100)
        infra_after = state_after.get('infrastructure_health', 100)
        return max(0, infra_after - infra_before)
    
    def _calculate_response_time_penalty(self, action: Dict) -> float:
        """Calculate penalty for slow response."""
        response_time = action.get('response_time', 0)
        return -response_time  # Negative penalty
    
    def _calculate_resource_efficiency(self, action: Dict, state_after: Dict) -> float:
        """Calculate resource efficiency score."""
        resources_used = action.get('resources_allocated', 0)
        effectiveness = state_after.get('action_effectiveness', 0.5)
        
        if resources_used == 0:
            return 0
        
        return effectiveness / (resources_used + 1)  # Avoid division by zero
    
    def _calculate_cascading_prevention(self, state_before: Dict, state_after: Dict) -> float:
        """Calculate cascading failure prevention score."""
        cascades_before = state_before.get('cascading_failures', 0)
        cascades_after = state_after.get('cascading_failures', 0)
        return max(0, cascades_before - cascades_after)
    
    def _calculate_coalition_bonus(self, state_after: Dict) -> float:
        """Calculate bonus for strong coalitions."""
        coalition_strength = state_after.get('coalition_strength', 0)
        return coalition_strength
    
    def update_weights(self, new_weights: RewardWeights):
        """Update reward weights."""
        self.weights = new_weights
    
    def get_average_reward(self, last_n: Optional[int] = None) -> float:
        """Get average reward over last n episodes."""
        if not self.reward_history:
            return 0.0
        
        history = self.reward_history[-last_n:] if last_n else self.reward_history
        return sum(r['total_reward'] for r in history) / len(history)
    
    def get_reward_breakdown(self) -> Dict[str, float]:
        """Get average breakdown of reward components."""
        if not self.reward_history:
            return {}
        
        components = {}
        for reward_info in self.reward_history:
            for key, value in reward_info['components'].items():
                components[key] = components.get(key, 0) + value
        
        n = len(self.reward_history)
        return {k: v / n for k, v in components.items()}
