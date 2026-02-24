"""
Infrastructure Agent - Manages infrastructure systems
"""

from typing import Dict, List
from .agent_base import AgentBase, AgentType


class InfrastructureAgent(AgentBase):
    """
    Represents infrastructure system managers.
    Focuses on maintaining and repairing critical infrastructure.
    """
    
    def __init__(self, agent_id: str, name: str, managed_assets: List[str] = None,
                 infrastructure_type: str = "general", system_health: float = 1.0, 
                 repair_capacity: float = 100.0):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.INFRASTRUCTURE,
            name=name
        )
        
        # Infrastructure-specific attributes
        self.managed_assets: List[str] = managed_assets or []
        self.infrastructure_type: str = infrastructure_type
        self.system_health: float = system_health
        self.repair_capacity: float = repair_capacity
        self.maintenance_schedule: List[Dict] = []
        
        # Default goals
        self.goals = [
            "maintain_infrastructure",
            "repair_damage",
            "prevent_cascading_failures",
            "restore_services"
        ]
        
        # Default preferences
        self.preferences = {
            "system_reliability": 0.90,
            "rapid_response": 0.80,
            "preventive_maintenance": 0.70,
            "cost_efficiency": 0.60
        }
    
    def _calculate_utility(self, option: Dict) -> float:
        """Calculate utility for infrastructure agent"""
        utility = super()._calculate_utility(option)
        
        # Prioritize system health
        if option.get("improves_health", False):
            health_improvement = option.get("health_improvement", 0)
            utility += health_improvement * 100.0
        
        # Consider repair capacity
        repair_needed = option.get("repair_capacity_needed", 0)
        if repair_needed > self.repair_capacity:
            utility -= 50.0  # Penalize if beyond capacity
        
        # Prioritize critical infrastructure
        if option.get("is_critical", False):
            utility += 50.0
        
        return utility
    
    def repair_system(self, damage_amount: float) -> Dict:
        """Repair infrastructure damage"""
        if damage_amount > self.repair_capacity:
            # Partial repair
            repaired = self.repair_capacity
            remaining = damage_amount - repaired
        else:
            repaired = damage_amount
            remaining = 0
        
        # Improve system health
        health_improvement = repaired / 100.0
        self.system_health = min(1.0, self.system_health + health_improvement)
        
        return {
            "repaired": repaired,
            "remaining_damage": remaining,
            "system_health": self.system_health
        }
    
    def schedule_maintenance(self, task: Dict) -> None:
        """Schedule maintenance task"""
        self.maintenance_schedule.append(task)
    
    def get_status(self) -> Dict:
        """Get infrastructure agent status"""
        status = super().get_status()
        status.update({
            "infrastructure_type": self.infrastructure_type,
            "system_health": self.system_health,
            "repair_capacity": self.repair_capacity,
            "scheduled_tasks": len(self.maintenance_schedule)
        })
        return status
