"""
Emergency Agent - Represents emergency responders
"""

from typing import Dict, List
from .agent_base import AgentBase, AgentType


class EmergencyAgent(AgentBase):
    """
    Represents emergency responders (fire, police, medical).
    Focuses on immediate response and life-saving actions.
    """
    
    def __init__(self, agent_id: str, name: str, unit_type: str = "general",
                 team_size: int = 10, equipment_level: float = 0.8):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.EMERGENCY,
            name=name
        )
        
        # Emergency-specific attributes
        self.unit_type: str = unit_type
        self.team_size: int = team_size
        self.equipment_level: float = equipment_level
        self.active_missions: List[Dict] = []
        self.lives_saved: int = 0
        
        # Default goals
        self.goals = [
            "save_lives",
            "provide_emergency_care",
            "secure_area",
            "coordinate_evacuation"
        ]
        
        # Default preferences
        self.preferences = {
            "life_saving": 1.0,
            "rapid_response": 0.95,
            "team_safety": 0.85,
            "resource_efficiency": 0.60
        }
    
    def _calculate_utility(self, option: Dict) -> float:
        """Calculate utility for emergency agent"""
        utility = super()._calculate_utility(option)
        
        # Heavily prioritize life-saving
        lives_saved = option.get("potential_lives_saved", 0)
        utility += lives_saved * 1000.0
        
        # Consider response time
        response_time = option.get("response_time", 1.0)
        utility -= response_time * 10.0  # Faster is better
        
        # Consider team capacity
        team_needed = option.get("team_size_needed", 0)
        if team_needed > self.team_size:
            utility -= 100.0  # Penalize if beyond capacity
        
        # Consider danger level
        danger_level = option.get("danger_level", 0)
        utility -= danger_level * self.preferences.get("team_safety", 0.85) * 50.0
        
        return utility
    
    def deploy_mission(self, mission: Dict) -> Dict:
        """Deploy on a mission"""
        self.active_missions.append(mission)
        
        return {
            "success": True,
            "mission_id": mission.get("mission_id"),
            "team_deployed": self.team_size,
            "active_missions": len(self.active_missions)
        }
    
    def complete_mission(self, mission_id: str, lives_saved: int = 0) -> Dict:
        """Complete a mission"""
        # Find and remove mission
        mission = None
        for m in self.active_missions:
            if m.get("mission_id") == mission_id:
                mission = m
                self.active_missions.remove(m)
                break
        
        if not mission:
            return {"success": False, "reason": "Mission not found"}
        
        # Update statistics
        self.lives_saved += lives_saved
        
        return {
            "success": True,
            "mission_id": mission_id,
            "lives_saved": lives_saved,
            "total_lives_saved": self.lives_saved
        }
    
    def get_status(self) -> Dict:
        """Get emergency agent status"""
        status = super().get_status()
        status.update({
            "unit_type": self.unit_type,
            "team_size": self.team_size,
            "equipment_level": self.equipment_level,
            "active_missions": len(self.active_missions),
            "lives_saved": self.lives_saved
        })
        return status
