"""
Non-Deterministic Planner - Plans under uncertainty
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import random


@dataclass
class Outcome:
    """Represents a possible outcome of an action"""
    outcome_id: str
    description: str
    probability: float
    effects: Dict[str, float]
    
    def to_dict(self) -> Dict:
        return {
            "outcome_id": self.outcome_id,
            "description": self.description,
            "probability": self.probability,
            "effects": self.effects
        }


class NonDeterministicPlanner:
    """
    Plans under uncertainty with probabilistic outcomes.
    Handles non-deterministic action effects.
    """
    
    def __init__(self):
        self.actions_with_outcomes: Dict[str, List[Outcome]] = {}
        self.plans: List[Dict] = []
    
    def register_action_outcomes(
        self,
        action_id: str,
        outcomes: List[Outcome]
    ) -> None:
        """Register possible outcomes for an action"""
        # Normalize probabilities
        total_prob = sum(o.probability for o in outcomes)
        if total_prob > 0:
            for outcome in outcomes:
                outcome.probability /= total_prob
        
        self.actions_with_outcomes[action_id] = outcomes
    
    def plan_with_uncertainty(
        self,
        actions: List[str],
        initial_state: Dict[str, float],
        goal_threshold: float = 0.7
    ) -> Dict:
        """
        Create plan considering uncertainty.
        
        Args:
            actions: List of action IDs to consider
            initial_state: Initial state values
            goal_threshold: Minimum probability of success
        
        Returns:
            Plan with expected outcomes
        """
        # Simulate multiple executions
        num_simulations = 100
        successful_runs = 0
        outcomes_distribution = []
        
        for _ in range(num_simulations):
            state = initial_state.copy()
            
            for action_id in actions:
                if action_id in self.actions_with_outcomes:
                    # Sample outcome based on probabilities
                    outcome = self._sample_outcome(action_id)
                    
                    # Apply effects
                    for key, value in outcome.effects.items():
                        state[key] = state.get(key, 0) + value
            
            outcomes_distribution.append(state.copy())
            
            # Check if goal achieved (simplified)
            if state.get("goal_value", 0) >= goal_threshold:
                successful_runs += 1
        
        success_rate = successful_runs / num_simulations
        
        # Calculate expected values
        expected_state = {}
        for key in initial_state.keys():
            expected_state[key] = sum(
                s.get(key, 0) for s in outcomes_distribution
            ) / num_simulations
        
        return {
            "actions": actions,
            "success_rate": success_rate,
            "expected_state": expected_state,
            "simulations_run": num_simulations,
            "meets_threshold": success_rate >= goal_threshold
        }
    
    def _sample_outcome(self, action_id: str) -> Outcome:
        """Sample an outcome based on probabilities"""
        outcomes = self.actions_with_outcomes.get(action_id, [])
        if not outcomes:
            return Outcome("default", "No effect", 1.0, {})
        
        # Weighted random choice
        rand = random.random()
        cumulative = 0.0
        
        for outcome in outcomes:
            cumulative += outcome.probability
            if rand <= cumulative:
                return outcome
        
        return outcomes[-1]  # Fallback
    
    def calculate_expected_value(
        self,
        action_id: str,
        value_function: Dict[str, float]
    ) -> float:
        """Calculate expected value of an action"""
        outcomes = self.actions_with_outcomes.get(action_id, [])
        
        expected_value = 0.0
        for outcome in outcomes:
            outcome_value = sum(
                outcome.effects.get(key, 0) * value_function.get(key, 0)
                for key in value_function
            )
            expected_value += outcome.probability * outcome_value
        
        return expected_value
