"""
Optimization Scorer - Scores and ranks disaster response strategies
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class OptimizationMetric(Enum):
    """Optimization metrics"""
    LIVES_SAVED = "lives_saved"
    COST_EFFECTIVENESS = "cost_effectiveness"
    SPEED = "speed"
    COVERAGE = "coverage"
    RESILIENCE = "resilience"
    SUSTAINABILITY = "sustainability"


@dataclass
class ScoringWeights:
    """Weights for different optimization metrics"""
    lives_saved: float = 0.35
    cost_effectiveness: float = 0.25
    speed: float = 0.15
    coverage: float = 0.10
    resilience: float = 0.10
    sustainability: float = 0.05
    
    def to_dict(self) -> Dict:
        return {
            "lives_saved": self.lives_saved,
            "cost_effectiveness": self.cost_effectiveness,
            "speed": self.speed,
            "coverage": self.coverage,
            "resilience": self.resilience,
            "sustainability": self.sustainability
        }


class OptimizationScorer:
    """
    Scores disaster response strategies using multiple optimization metrics.
    Provides multi-objective optimization scoring.
    """
    
    def __init__(self, weights: Optional[ScoringWeights] = None):
        self.weights = weights or ScoringWeights()
        self.scores: List[Dict] = []
    
    def score_strategy(
        self,
        strategy: Dict,
        outcomes: Dict,
        constraints: Optional[Dict] = None
    ) -> Dict:
        """
        Score a disaster response strategy.
        
        Args:
            strategy: Strategy definition
            outcomes: Projected outcomes
            constraints: Optional constraints
        
        Returns:
            Comprehensive score breakdown
        """
        # Calculate individual metric scores
        scores = {
            "lives_saved": self._score_lives_saved(outcomes),
            "cost_effectiveness": self._score_cost_effectiveness(strategy, outcomes),
            "speed": self._score_speed(strategy),
            "coverage": self._score_coverage(outcomes),
            "resilience": self._score_resilience(outcomes),
            "sustainability": self._score_sustainability(strategy, outcomes)
        }
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[metric] * getattr(self.weights, metric)
            for metric in scores
        )
        
        # Check constraints
        constraint_satisfaction = self._check_constraints(strategy, constraints) if constraints else 1.0
        
        # Final score adjusted by constraint satisfaction
        final_score = overall_score * constraint_satisfaction
        
        result = {
            "strategy_id": strategy.get("strategy_id", "unknown"),
            "overall_score": final_score,
            "metric_scores": scores,
            "weights_used": self.weights.to_dict(),
            "constraint_satisfaction": constraint_satisfaction,
            "rank": None  # Will be set during ranking
        }
        
        self.scores.append(result)
        return result
    
    def _score_lives_saved(self, outcomes: Dict) -> float:
        """Score based on lives saved"""
        lives_saved = outcomes.get("lives_saved", 0)
        casualties_prevented = outcomes.get("casualties_prevented", 0)
        
        total_impact = lives_saved + casualties_prevented
        
        # Normalize to 0-1 scale (assume 1000 is excellent)
        return min(1.0, total_impact / 1000.0)
    
    def _score_cost_effectiveness(self, strategy: Dict, outcomes: Dict) -> float:
        """Score based on cost-effectiveness"""
        cost = strategy.get("cost", 1)
        benefit = outcomes.get("total_benefit", 0)
        
        if cost == 0:
            return 1.0
        
        ratio = benefit / cost
        
        # Normalize (assume ratio of 10 is excellent)
        return min(1.0, ratio / 10.0)
    
    def _score_speed(self, strategy: Dict) -> float:
        """Score based on implementation speed"""
        duration = strategy.get("duration_days", 365)
        
        # Faster is better (normalize to 0-1, 30 days = 1.0, 365 days = 0.0)
        return max(0.0, 1.0 - (duration - 30) / 335.0)
    
    def _score_coverage(self, outcomes: Dict) -> float:
        """Score based on population coverage"""
        coverage = outcomes.get("coverage", 0.5)
        people_supported = outcomes.get("people_supported", 0)
        total_affected = outcomes.get("total_affected", 1)
        
        if total_affected > 0:
            coverage_ratio = people_supported / total_affected
            return min(1.0, coverage_ratio)
        
        return coverage
    
    def _score_resilience(self, outcomes: Dict) -> float:
        """Score based on resilience improvement"""
        resilience_improvement = outcomes.get("resilience_improvement", 0)
        infrastructure_health = outcomes.get("infrastructure_health_improvement", 0)
        
        # Combine metrics
        resilience_score = (resilience_improvement + infrastructure_health) / 2.0
        
        return min(1.0, resilience_score)
    
    def _score_sustainability(self, strategy: Dict, outcomes: Dict) -> float:
        """Score based on long-term sustainability"""
        long_term_benefit = outcomes.get("long_term_benefit", 0.5)
        environmental_impact = outcomes.get("environmental_impact", 0.5)
        
        # Higher is better
        return (long_term_benefit + environmental_impact) / 2.0
    
    def _check_constraints(self, strategy: Dict, constraints: Dict) -> float:
        """Check constraint satisfaction (0.0 to 1.0)"""
        violations = 0
        total_constraints = len(constraints)
        
        if total_constraints == 0:
            return 1.0
        
        # Check budget constraint
        if "max_budget" in constraints:
            if strategy.get("cost", 0) > constraints["max_budget"]:
                violations += 1
        
        # Check time constraint
        if "max_duration" in constraints:
            if strategy.get("duration_days", 0) > constraints["max_duration"]:
                violations += 1
        
        # Check resource constraints
        if "required_resources" in constraints:
            available = strategy.get("available_resources", {})
            for resource, amount in constraints["required_resources"].items():
                if available.get(resource, 0) < amount:
                    violations += 1
        
        satisfaction = 1.0 - (violations / max(total_constraints, 1))
        return max(0.0, satisfaction)
    
    def rank_strategies(
        self,
        strategies: List[Dict],
        outcomes_list: List[Dict],
        constraints: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Rank multiple strategies.
        
        Args:
            strategies: List of strategies
            outcomes_list: List of outcomes for each strategy
            constraints: Optional constraints
        
        Returns:
            Ranked list of strategies with scores
        """
        scored_strategies = []
        
        for strategy, outcomes in zip(strategies, outcomes_list):
            score_result = self.score_strategy(strategy, outcomes, constraints)
            scored_strategies.append(score_result)
        
        # Sort by overall score
        ranked = sorted(
            scored_strategies,
            key=lambda x: x["overall_score"],
            reverse=True
        )
        
        # Assign ranks
        for i, strategy in enumerate(ranked):
            strategy["rank"] = i + 1
        
        return ranked
    
    def get_pareto_optimal(
        self,
        strategies: List[Dict]
    ) -> List[Dict]:
        """
        Find Pareto-optimal strategies (multi-objective optimization).
        
        Args:
            strategies: List of scored strategies
        
        Returns:
            Pareto-optimal strategies
        """
        pareto_optimal = []
        
        for strategy in strategies:
            is_dominated = False
            
            for other in strategies:
                if strategy == other:
                    continue
                
                # Check if other dominates strategy
                if self._dominates(other, strategy):
                    is_dominated = True
                    break
            
            if not is_dominated:
                pareto_optimal.append(strategy)
        
        return pareto_optimal
    
    def _dominates(self, strategy1: Dict, strategy2: Dict) -> bool:
        """Check if strategy1 dominates strategy2"""
        scores1 = strategy1.get("metric_scores", {})
        scores2 = strategy2.get("metric_scores", {})
        
        # strategy1 dominates if it's better or equal in all metrics
        # and strictly better in at least one
        better_in_all = all(
            scores1.get(metric, 0) >= scores2.get(metric, 0)
            for metric in scores1
        )
        
        strictly_better_in_one = any(
            scores1.get(metric, 0) > scores2.get(metric, 0)
            for metric in scores1
        )
        
        return better_in_all and strictly_better_in_one
    
    def get_scores(self) -> List[Dict]:
        """Get all scores"""
        return self.scores
