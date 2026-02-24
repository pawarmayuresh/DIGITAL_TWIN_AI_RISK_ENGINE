"""
Citizen Agent - Represents individual citizens
"""

from typing import Dict, List
from .agent_base import AgentBase, AgentType, AgentState


class CitizenAgent(AgentBase):
    """
    Represents a citizen in the disaster scenario.
    Focuses on personal safety, family welfare, and basic needs.
    """
    
    def __init__(self, agent_id: str, name: str, family_size: int = 1, location: str = "unknown"):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.CITIZEN,
            name=name
        )
        
        # Citizen-specific attributes
        self.safety_level: float = 1.0  # 0.0 to 1.0
        self.needs_met: Dict[str, float] = {
            "food": 1.0,
            "water": 1.0,
            "shelter": 1.0,
            "medical": 1.0
        }
        self.family_size: int = family_size
        self.location: str = location
        
        # Default goals
        self.goals = [
            "ensure_safety",
            "meet_basic_needs",
            "protect_family",
            "access_information"
        ]
        
        # Default preferences
        self.preferences = {
            "safety": 0.9,
            "family_welfare": 0.8,
            "property_protection": 0.5,
            "community_help": 0.6
        }
    
    def _filter_relevant_info(self, environment: Dict) -> Dict:
        """Filter info relevant to citizens"""
        relevant = {}
        
        # Safety information
        if "disaster_status" in environment:
            relevant["disaster_status"] = environment["disaster_status"]
        
        # Resource availability
        if "resources" in environment:
            relevant["resources"] = environment["resources"]
        
        # Evacuation orders
        if "evacuation_orders" in environment:
            relevant["evacuation_orders"] = environment["evacuation_orders"]
        
        return relevant
    
    def _calculate_utility(self, option: Dict) -> float:
        """Calculate utility for citizen"""
        utility = super()._calculate_utility(option)
        
        # Prioritize safety
        if option.get("improves_safety", False):
            utility += 50.0 * self.preferences.get("safety", 0.9)
        
        # Consider family impact
        if "family_benefit" in option:
            utility += option["family_benefit"] * self.preferences.get("family_welfare", 0.8)
        
        # Consider basic needs
        for need in ["food", "water", "shelter", "medical"]:
            if option.get(f"provides_{need}", False):
                need_level = self.needs_met.get(need, 1.0)
                # Higher utility if need is low
                utility += (1.0 - need_level) * 20.0
        
        return utility
    
    def update_safety(self, safety_change: float) -> None:
        """Update safety level"""
        self.safety_level = max(0.0, min(1.0, self.safety_level + safety_change))
    
    def update_needs(self, need_changes: Dict[str, float]) -> None:
        """Update basic needs"""
        for need, change in need_changes.items():
            if need in self.needs_met:
                current = self.needs_met[need]
                self.needs_met[need] = max(0.0, min(1.0, current + change))
    
    def get_status(self) -> Dict:
        """Get citizen status"""
        status = super().get_status()
        status.update({
            "safety_level": self.safety_level,
            "needs_met": self.needs_met,
            "family_size": self.family_size,
            "location": self.location,
            "overall_wellbeing": self._calculate_wellbeing()
        })
        return status
    
    def _calculate_wellbeing(self) -> float:
        """Calculate overall wellbeing score"""
        # Weighted average of safety and needs
        needs_avg = sum(self.needs_met.values()) / len(self.needs_met)
        wellbeing = (self.safety_level * 0.6 + needs_avg * 0.4)
        return wellbeing
