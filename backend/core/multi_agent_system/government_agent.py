"""
Government Agent - Represents government decision-makers
"""

from typing import Dict, List
from .agent_base import AgentBase, AgentType


class GovernmentAgent(AgentBase):
    """
    Represents government officials and decision-makers.
    Focuses on public welfare, resource allocation, and policy implementation.
    """
    
    def __init__(self, agent_id: str, name: str, budget: float = 10_000_000, 
                 authority_level: float = 0.8, jurisdiction: str = "city"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.GOVERNMENT,
            name=name
        )
        
        # Government-specific attributes
        self.budget: float = budget
        self.authority_level: float = authority_level
        self.jurisdiction: str = jurisdiction
        self.policies_enacted: List[str] = []
        
        # Default goals
        self.goals = [
            "protect_citizens",
            "maintain_order",
            "allocate_resources",
            "coordinate_response"
        ]
        
        # Default preferences
        self.preferences = {
            "public_safety": 0.95,
            "economic_stability": 0.75,
            "political_approval": 0.60,
            "long_term_planning": 0.70
        }
    
    def _calculate_utility(self, option: Dict) -> float:
        """Calculate utility for government"""
        utility = super()._calculate_utility(option)
        
        # Prioritize public safety
        if option.get("improves_public_safety", False):
            utility += 100.0 * self.preferences.get("public_safety", 0.95)
        
        # Consider budget constraints
        cost = option.get("cost", 0)
        if cost > self.budget:
            utility -= 1000.0  # Heavily penalize unaffordable options
        
        # Consider political impact
        if "political_approval_change" in option:
            utility += option["political_approval_change"] * self.preferences.get("political_approval", 0.6)
        
        # Consider number of citizens helped
        if "citizens_helped" in option:
            utility += option["citizens_helped"] * 0.1
        
        return utility
    
    def enact_policy(self, policy_id: str, cost: float) -> Dict:
        """Enact a policy"""
        if cost > self.budget:
            return {
                "success": False,
                "reason": "Insufficient budget"
            }
        
        self.budget -= cost
        self.policies_enacted.append(policy_id)
        
        return {
            "success": True,
            "policy_id": policy_id,
            "cost": cost,
            "remaining_budget": self.budget
        }
    
    def allocate_budget(self, allocation: Dict[str, float]) -> Dict:
        """Allocate budget across different needs"""
        total_allocation = sum(allocation.values())
        
        if total_allocation > self.budget:
            return {
                "success": False,
                "reason": "Allocation exceeds budget"
            }
        
        self.budget -= total_allocation
        
        return {
            "success": True,
            "allocation": allocation,
            "remaining_budget": self.budget
        }
    
    def get_status(self) -> Dict:
        """Get government agent status"""
        status = super().get_status()
        status.update({
            "budget": self.budget,
            "authority_level": self.authority_level,
            "jurisdiction": self.jurisdiction,
            "policies_enacted": len(self.policies_enacted)
        })
        return status
