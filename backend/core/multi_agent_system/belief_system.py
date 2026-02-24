"""
Belief System - Manages agent beliefs about the world
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class BeliefType(Enum):
    """Types of beliefs"""
    FACT = "fact"  # Believed to be true
    ASSUMPTION = "assumption"  # Assumed but uncertain
    GOAL = "goal"  # Desired state
    PREFERENCE = "preference"  # Value judgment


@dataclass
class Belief:
    """Represents a single belief"""
    belief_id: str
    belief_type: BeliefType
    content: Dict[str, Any]
    confidence: float = 1.0  # 0.0 to 1.0
    source: str = "self"
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "belief_id": self.belief_id,
            "belief_type": self.belief_type.value,
            "content": self.content,
            "confidence": self.confidence,
            "source": self.source,
            "timestamp": self.timestamp
        }


class BeliefSystem:
    """
    Manages an agent's beliefs about the world.
    Handles belief updates, conflicts, and reasoning.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.beliefs: Dict[str, Belief] = {}
        self.belief_history: List[Dict] = []
    
    def add_belief(self, belief: Belief) -> None:
        """Add or update a belief"""
        self.beliefs[belief.belief_id] = belief
        
        self.belief_history.append({
            "action": "added",
            "belief_id": belief.belief_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def remove_belief(self, belief_id: str) -> None:
        """Remove a belief"""
        if belief_id in self.beliefs:
            del self.beliefs[belief_id]
            
            self.belief_history.append({
                "action": "removed",
                "belief_id": belief_id,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def update_belief(self, belief_id: str, new_content: Dict, new_confidence: float = None) -> None:
        """Update existing belief"""
        if belief_id in self.beliefs:
            belief = self.beliefs[belief_id]
            belief.content = new_content
            if new_confidence is not None:
                belief.confidence = new_confidence
            belief.timestamp = datetime.utcnow().isoformat()
    
    def get_belief(self, belief_id: str) -> Belief:
        """Get a specific belief"""
        return self.beliefs.get(belief_id)
    
    def get_beliefs_by_type(self, belief_type: BeliefType) -> List[Belief]:
        """Get all beliefs of a specific type"""
        return [
            belief for belief in self.beliefs.values()
            if belief.belief_type == belief_type
        ]
    
    def get_high_confidence_beliefs(self, threshold: float = 0.8) -> List[Belief]:
        """Get beliefs with confidence above threshold"""
        return [
            belief for belief in self.beliefs.values()
            if belief.confidence >= threshold
        ]
    
    def resolve_conflict(self, belief1_id: str, belief2_id: str) -> str:
        """
        Resolve conflict between two beliefs.
        Returns ID of belief to keep.
        """
        belief1 = self.beliefs.get(belief1_id)
        belief2 = self.beliefs.get(belief2_id)
        
        if not belief1 or not belief2:
            return belief1_id if belief1 else belief2_id
        
        # Keep belief with higher confidence
        return belief1_id if belief1.confidence >= belief2.confidence else belief2_id
    
    def get_all_beliefs(self) -> List[Dict]:
        """Get all beliefs"""
        return [belief.to_dict() for belief in self.beliefs.values()]
