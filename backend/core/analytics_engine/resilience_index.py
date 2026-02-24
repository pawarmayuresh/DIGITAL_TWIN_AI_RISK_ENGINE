"""
Resilience Index - Calculates city resilience metrics.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ResilienceScore:
    """Resilience score components."""
    robustness: float  # Ability to withstand shocks
    redundancy: float  # Backup systems availability
    resourcefulness: float  # Ability to mobilize resources
    rapidity: float  # Speed of recovery
    overall_score: float


class ResilienceIndex:
    """Calculates resilience index for cities."""
    
    def __init__(self):
        self.resilience_history: List[ResilienceScore] = []
        self.weights = {
            'robustness': 0.3,
            'redundancy': 0.2,
            'resourcefulness': 0.25,
            'rapidity': 0.25
        }
    
    def calculate_resilience(
        self,
        city_data: Dict[str, Any],
        disaster_response: Dict[str, Any]
    ) -> ResilienceScore:
        """Calculate overall resilience score."""
        
        robustness = self._calculate_robustness(city_data, disaster_response)
        redundancy = self._calculate_redundancy(city_data)
        resourcefulness = self._calculate_resourcefulness(city_data, disaster_response)
        rapidity = self._calculate_rapidity(disaster_response)
        
        overall = (
            robustness * self.weights['robustness'] +
            redundancy * self.weights['redundancy'] +
            resourcefulness * self.weights['resourcefulness'] +
            rapidity * self.weights['rapidity']
        )
        
        score = ResilienceScore(
            robustness=robustness,
            redundancy=redundancy,
            resourcefulness=resourcefulness,
            rapidity=rapidity,
            overall_score=overall
        )
        
        self.resilience_history.append(score)
        return score
    
    def _calculate_robustness(self, city_data: Dict, response: Dict) -> float:
        """Calculate robustness score (0-100)."""
        infrastructure_health = city_data.get('infrastructure_health', 100)
        building_codes = city_data.get('building_code_compliance', 0.8)
        
        score = (infrastructure_health / 100.0) * 0.6 + building_codes * 0.4
        return score * 100
    
    def _calculate_redundancy(self, city_data: Dict) -> float:
        """Calculate redundancy score (0-100)."""
        backup_systems = city_data.get('backup_systems', 0.5)
        resource_stockpiles = city_data.get('resource_stockpiles', 0.6)
        
        score = (backup_systems + resource_stockpiles) / 2
        return score * 100
    
    def _calculate_resourcefulness(self, city_data: Dict, response: Dict) -> float:
        """Calculate resourcefulness score (0-100)."""
        resources_available = city_data.get('resources_available', 5000)
        resources_mobilized = response.get('resources_mobilized', 0)
        
        mobilization_rate = min(resources_mobilized / max(resources_available, 1), 1.0)
        return mobilization_rate * 100
    
    def _calculate_rapidity(self, response: Dict) -> float:
        """Calculate rapidity score (0-100)."""
        response_time = response.get('response_time', 60)
        target_time = 30
        
        score = max(0, 1 - (response_time - target_time) / target_time)
        return score * 100
    
    def get_resilience_category(self, score: float) -> str:
        """Get resilience category."""
        if score >= 80:
            return "highly_resilient"
        elif score >= 60:
            return "resilient"
        elif score >= 40:
            return "moderately_resilient"
        else:
            return "vulnerable"
