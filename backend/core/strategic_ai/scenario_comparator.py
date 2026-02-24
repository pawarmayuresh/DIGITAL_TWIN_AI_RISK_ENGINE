"""
Scenario Comparator - Compare different disaster response scenarios
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Scenario:
    """Represents a disaster response scenario"""
    scenario_id: str
    name: str
    description: str
    policies: List[str]
    actions: List[str]
    projected_outcomes: Dict
    cost: float
    duration_days: int
    
    def to_dict(self) -> Dict:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "description": self.description,
            "policies": self.policies,
            "actions": self.actions,
            "projected_outcomes": self.projected_outcomes,
            "cost": self.cost,
            "duration_days": self.duration_days
        }


class ScenarioComparator:
    """
    Compares different disaster response scenarios.
    Ranks scenarios based on multiple criteria.
    """
    
    def __init__(self):
        self.scenarios: Dict[str, Scenario] = {}
        self.comparisons: List[Dict] = []
    
    def register_scenario(self, scenario: Scenario) -> None:
        """Register a scenario"""
        self.scenarios[scenario.scenario_id] = scenario
    
    def compare_scenarios(
        self,
        scenario_ids: List[str],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict:
        """
        Compare multiple scenarios.
        
        Args:
            scenario_ids: List of scenario IDs to compare
            weights: Weights for different criteria
        
        Returns:
            Comparison results with rankings
        """
        if weights is None:
            weights = {
                "lives_saved": 0.4,
                "cost_effectiveness": 0.3,
                "speed": 0.2,
                "coverage": 0.1
            }
        
        scenarios = [
            self.scenarios[sid]
            for sid in scenario_ids
            if sid in self.scenarios
        ]
        
        if not scenarios:
            return {"error": "No valid scenarios found"}
        
        # Score each scenario
        scored_scenarios = []
        for scenario in scenarios:
            score = self._calculate_scenario_score(scenario, weights)
            scored_scenarios.append({
                "scenario": scenario.to_dict(),
                "score": score,
                "breakdown": self._get_score_breakdown(scenario)
            })
        
        # Rank by score
        ranked = sorted(scored_scenarios, key=lambda x: x["score"], reverse=True)
        
        comparison = {
            "comparison_id": f"comp_{datetime.utcnow().timestamp()}",
            "scenarios_compared": len(ranked),
            "ranked_scenarios": ranked,
            "best_scenario": ranked[0] if ranked else None,
            "weights_used": weights,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.comparisons.append(comparison)
        return comparison
    
    def _calculate_scenario_score(
        self,
        scenario: Scenario,
        weights: Dict[str, float]
    ) -> float:
        """Calculate weighted score for scenario"""
        outcomes = scenario.projected_outcomes
        
        # Normalize metrics to 0-1 scale
        lives_saved_score = min(1.0, outcomes.get("lives_saved", 0) / 1000)
        cost_effectiveness = min(1.0, outcomes.get("cost_benefit_ratio", 0) / 10)
        speed_score = max(0.0, 1.0 - scenario.duration_days / 365)
        coverage_score = outcomes.get("coverage", 0.5)
        
        # Weighted sum
        score = (
            lives_saved_score * weights.get("lives_saved", 0.4) +
            cost_effectiveness * weights.get("cost_effectiveness", 0.3) +
            speed_score * weights.get("speed", 0.2) +
            coverage_score * weights.get("coverage", 0.1)
        )
        
        return score
    
    def _get_score_breakdown(self, scenario: Scenario) -> Dict:
        """Get detailed score breakdown"""
        outcomes = scenario.projected_outcomes
        
        return {
            "lives_saved": outcomes.get("lives_saved", 0),
            "cost": scenario.cost,
            "duration_days": scenario.duration_days,
            "cost_benefit_ratio": outcomes.get("cost_benefit_ratio", 0),
            "coverage": outcomes.get("coverage", 0)
        }
    
    def get_best_scenario(
        self,
        criterion: str = "overall_score"
    ) -> Optional[Dict]:
        """Get best scenario based on criterion"""
        if not self.comparisons:
            return None
        
        latest_comparison = self.comparisons[-1]
        ranked = latest_comparison.get("ranked_scenarios", [])
        
        return ranked[0] if ranked else None
    
    def get_all_scenarios(self) -> List[Dict]:
        """Get all registered scenarios"""
        return [s.to_dict() for s in self.scenarios.values()]
