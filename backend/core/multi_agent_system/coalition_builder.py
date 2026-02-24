"""
Coalition Builder - Manages coalition formation and operations
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CoalitionStatus(Enum):
    """Status of coalition"""
    FORMING = "forming"
    ACTIVE = "active"
    DISSOLVED = "dissolved"


@dataclass
class Coalition:
    """Represents a coalition of agents"""
    coalition_id: str
    name: str
    members: Set[str] = field(default_factory=set)
    leader_id: Optional[str] = None
    goals: List[str] = field(default_factory=list)
    resources: Dict = field(default_factory=dict)
    status: CoalitionStatus = CoalitionStatus.FORMING
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "coalition_id": self.coalition_id,
            "name": self.name,
            "members": list(self.members),
            "leader_id": self.leader_id,
            "goals": self.goals,
            "resources": self.resources,
            "status": self.status.value,
            "created_at": self.created_at,
            "member_count": len(self.members)
        }


class CoalitionBuilder:
    """
    Manages coalition formation and operations.
    Handles member recruitment, resource pooling, and goal coordination.
    """
    
    def __init__(self):
        self.coalitions: Dict[str, Coalition] = {}
        self.agent_coalitions: Dict[str, Set[str]] = {}  # agent_id -> coalition_ids
    
    def create_coalition(
        self,
        name: str,
        leader_id: str,
        goals: List[str]
    ) -> Coalition:
        """Create a new coalition"""
        coalition_id = f"coal_{len(self.coalitions)}_{datetime.utcnow().timestamp()}"
        
        coalition = Coalition(
            coalition_id=coalition_id,
            name=name,
            leader_id=leader_id,
            goals=goals,
            members={leader_id}
        )
        
        self.coalitions[coalition_id] = coalition
        
        # Track agent membership
        if leader_id not in self.agent_coalitions:
            self.agent_coalitions[leader_id] = set()
        self.agent_coalitions[leader_id].add(coalition_id)
        
        return coalition
    
    def add_member(
        self,
        coalition_id: str,
        agent_id: str
    ) -> bool:
        """Add a member to coalition"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition:
            return False
        
        coalition.members.add(agent_id)
        
        # Track agent membership
        if agent_id not in self.agent_coalitions:
            self.agent_coalitions[agent_id] = set()
        self.agent_coalitions[agent_id].add(coalition_id)
        
        return True
    
    def remove_member(
        self,
        coalition_id: str,
        agent_id: str
    ) -> bool:
        """Remove a member from coalition"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition or agent_id not in coalition.members:
            return False
        
        coalition.members.discard(agent_id)
        
        # Update agent membership
        if agent_id in self.agent_coalitions:
            self.agent_coalitions[agent_id].discard(coalition_id)
        
        # Dissolve if no members left
        if len(coalition.members) == 0:
            coalition.status = CoalitionStatus.DISSOLVED
        
        return True
    
    def activate_coalition(self, coalition_id: str) -> bool:
        """Activate a coalition"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition:
            return False
        
        coalition.status = CoalitionStatus.ACTIVE
        return True
    
    def dissolve_coalition(self, coalition_id: str) -> bool:
        """Dissolve a coalition"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition:
            return False
        
        coalition.status = CoalitionStatus.DISSOLVED
        
        # Remove from all members' tracking
        for agent_id in coalition.members:
            if agent_id in self.agent_coalitions:
                self.agent_coalitions[agent_id].discard(coalition_id)
        
        return True
    
    def contribute_resources(
        self,
        coalition_id: str,
        agent_id: str,
        resources: Dict
    ) -> bool:
        """Agent contributes resources to coalition"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition or agent_id not in coalition.members:
            return False
        
        # Add resources to coalition pool
        for resource_type, amount in resources.items():
            if resource_type not in coalition.resources:
                coalition.resources[resource_type] = 0
            coalition.resources[resource_type] += amount
        
        return True
    
    def get_coalition(self, coalition_id: str) -> Optional[Coalition]:
        """Get coalition by ID"""
        return self.coalitions.get(coalition_id)
    
    def get_agent_coalitions(self, agent_id: str) -> List[Coalition]:
        """Get all coalitions an agent belongs to"""
        coalition_ids = self.agent_coalitions.get(agent_id, set())
        return [self.coalitions[cid] for cid in coalition_ids if cid in self.coalitions]
    
    def get_active_coalitions(self) -> List[Coalition]:
        """Get all active coalitions"""
        return [
            c for c in self.coalitions.values()
            if c.status == CoalitionStatus.ACTIVE
        ]
    
    def get_all_coalitions(self) -> List[Dict]:
        """Get all coalitions"""
        return [c.to_dict() for c in self.coalitions.values()]
    
    def find_compatible_coalitions(
        self,
        agent_goals: List[str],
        min_overlap: int = 1
    ) -> List[Coalition]:
        """Find coalitions with compatible goals"""
        compatible = []
        
        for coalition in self.coalitions.values():
            if coalition.status != CoalitionStatus.ACTIVE:
                continue
            
            # Count goal overlap
            overlap = len(set(agent_goals) & set(coalition.goals))
            if overlap >= min_overlap:
                compatible.append(coalition)
        
        return compatible
    
    def get_coalition_strength(self, coalition_id: str) -> Dict:
        """Calculate coalition strength metrics"""
        coalition = self.coalitions.get(coalition_id)
        if not coalition:
            return {}
        
        total_resources = sum(coalition.resources.values())
        
        return {
            "member_count": len(coalition.members),
            "total_resources": total_resources,
            "goal_count": len(coalition.goals),
            "resource_diversity": len(coalition.resources),
            "status": coalition.status.value
        }
