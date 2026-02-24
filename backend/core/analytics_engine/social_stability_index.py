"""
Social Stability Index - Measures social cohesion and stability.
"""

from typing import Dict, Any, List


class SocialStabilityIndex:
    """Calculates social stability metrics."""
    
    def __init__(self):
        self.stability_history: List[float] = []
    
    def calculate_stability(
        self,
        population_data: Dict[str, Any],
        disaster_impact: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate social stability index."""
        
        # Component scores
        public_trust = self._calculate_public_trust(population_data)
        social_cohesion = self._calculate_social_cohesion(population_data)
        resource_equity = self._calculate_resource_equity(population_data, disaster_impact)
        communication = self._calculate_communication_effectiveness(population_data)
        
        # Overall stability (0-100)
        overall = (public_trust + social_cohesion + resource_equity + communication) / 4
        
        self.stability_history.append(overall)
        
        return {
            'overall_stability': overall,
            'public_trust': public_trust,
            'social_cohesion': social_cohesion,
            'resource_equity': resource_equity,
            'communication_effectiveness': communication,
            'stability_level': self._get_stability_level(overall)
        }
    
    def _calculate_public_trust(self, data: Dict) -> float:
        """Calculate public trust score (0-100)."""
        trust_level = data.get('public_trust_level', 0.7)
        government_approval = data.get('government_approval', 0.6)
        
        return ((trust_level + government_approval) / 2) * 100
    
    def _calculate_social_cohesion(self, data: Dict) -> float:
        """Calculate social cohesion score (0-100)."""
        community_engagement = data.get('community_engagement', 0.6)
        volunteer_rate = data.get('volunteer_rate', 0.3)
        
        return ((community_engagement + volunteer_rate) / 2) * 100
    
    def _calculate_resource_equity(self, pop_data: Dict, impact: Dict) -> float:
        """Calculate resource distribution equity (0-100)."""
        gini_coefficient = pop_data.get('gini_coefficient', 0.4)
        resource_distribution_fairness = impact.get('resource_distribution_fairness', 0.7)
        
        equity = (1 - gini_coefficient) * 0.5 + resource_distribution_fairness * 0.5
        return equity * 100
    
    def _calculate_communication_effectiveness(self, data: Dict) -> float:
        """Calculate communication effectiveness (0-100)."""
        info_reach = data.get('information_reach', 0.8)
        message_clarity = data.get('message_clarity', 0.7)
        
        return ((info_reach + message_clarity) / 2) * 100
    
    def _get_stability_level(self, score: float) -> str:
        """Get stability level category."""
        if score >= 75:
            return "stable"
        elif score >= 50:
            return "moderate"
        elif score >= 25:
            return "unstable"
        else:
            return "critical"
