"""
Agent Base Class - Foundation for all agent types
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class AgentType(Enum):
    """Types of agents in the system"""
    CITIZEN = "citizen"
    GOVERNMENT = "government"
    INFRASTRUCTURE = "infrastructure"
    EMERGENCY = "emergency"
    BUSINESS = "business"
    NGO = "ngo"


class AgentState(Enum):
    """Agent operational states"""
    ACTIVE = "active"
    IDLE = "idle"
    NEGOTIATING = "negotiating"
    EXECUTING = "executing"
    WAITING = "waiting"
    DISABLED = "disabled"


@dataclass
class AgentBase:
    """
    Base class for all agents in the multi-agent system.
    Provides common functionality for perception, decision-making, and action.
    """
    agent_id: str
    agent_type: AgentType
    name: str
    state: AgentState = AgentState.IDLE
    
    # Agent properties
    resources: Dict[str, float] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    beliefs: Dict[str, Any] = field(default_factory=dict)
    preferences: Dict[str, float] = field(default_factory=dict)
    
    # Performance tracking
    actions_taken: List[Dict] = field(default_factory=list)
    rewards_received: float = 0.0
    interactions: List[Dict] = field(default_factory=list)
    message_history: List[Dict] = field(default_factory=list)
    
    # Relationships
    allies: List[str] = field(default_factory=list)
    opponents: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def __post_init__(self):
        """Initialize agent-specific attributes"""
        if not self.agent_id:
            self.agent_id = f"{self.agent_type.value}_{uuid.uuid4().hex[:8]}"
    
    def perceive(self, environment: Dict) -> Dict:
        """
        Perceive the environment and update beliefs.
        
        Args:
            environment: Current environment state
        
        Returns:
            Perceived information relevant to agent
        """
        # Base perception - can be overridden by subclasses
        perception = {
            "timestamp": datetime.utcnow().isoformat(),
            "environment_state": environment.copy(),
            "relevant_info": self._filter_relevant_info(environment)
        }
        
        # Update beliefs based on perception
        self._update_beliefs(perception)
        
        return perception
    
    def _filter_relevant_info(self, environment: Dict) -> Dict:
        """Filter environment info relevant to this agent"""
        # Base implementation - override in subclasses
        return environment
    
    def _update_beliefs(self, perception: Dict) -> None:
        """Update agent beliefs based on perception"""
        # Update belief about environment state
        self.beliefs["last_perception"] = perception
        self.beliefs["last_update"] = datetime.utcnow().isoformat()
    
    def decide(self, options: List[Dict]) -> Optional[Dict]:
        """
        Make a decision given available options.
        
        Args:
            options: List of possible actions/decisions
        
        Returns:
            Selected option or None
        """
        if not options:
            return None
        
        # Base decision-making: choose option with highest utility
        scored_options = [
            (option, self._calculate_utility(option))
            for option in options
        ]
        
        # Sort by utility
        scored_options.sort(key=lambda x: x[1], reverse=True)
        
        return scored_options[0][0] if scored_options else None
    
    def _calculate_utility(self, option: Dict) -> float:
        """
        Calculate utility of an option.
        
        Args:
            option: Option to evaluate
        
        Returns:
            Utility score
        """
        # Base utility calculation
        utility = 0.0
        
        # Consider resource cost
        cost = option.get("cost", 0)
        utility -= cost * 0.1
        
        # Consider expected benefit
        benefit = option.get("benefit", 0)
        utility += benefit
        
        # Consider alignment with goals
        if "goal_alignment" in option:
            utility += option["goal_alignment"] * 10.0
        
        return utility
    
    def act(self, action: Dict, environment: Dict) -> Dict:
        """
        Execute an action in the environment.
        
        Args:
            action: Action to execute
            environment: Current environment
        
        Returns:
            Action result
        """
        self.state = AgentState.EXECUTING
        
        # Record action
        action_record = {
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "environment_state": environment.copy()
        }
        self.actions_taken.append(action_record)
        
        # Execute action (base implementation)
        result = self._execute_action(action, environment)
        
        self.state = AgentState.IDLE
        
        return result
    
    def _execute_action(self, action: Dict, environment: Dict) -> Dict:
        """Execute action - override in subclasses"""
        return {
            "success": True,
            "action": action,
            "agent_id": self.agent_id
        }
    
    def communicate(self, message: Dict, recipient_id: str) -> Dict:
        """
        Send a message to another agent.
        
        Args:
            message: Message content
            recipient_id: Target agent ID
        
        Returns:
            Communication result
        """
        communication = {
            "sender_id": self.agent_id,
            "recipient_id": recipient_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.interactions.append(communication)
        
        return communication
    
    def send_message(self, recipient: 'AgentBase', message: Dict) -> Dict:
        """
        Send a message to another agent (convenience method).
        
        Args:
            recipient: Recipient agent object
            message: Message content
        
        Returns:
            Communication result
        """
        communication = self.communicate(message, recipient.agent_id)
        self.message_history.append(communication)
        
        # Deliver to recipient
        recipient.receive_message(message, self.agent_id)
        
        return communication
    
    def receive_message(self, message: Dict, sender_id: str) -> Dict:
        """
        Receive and process a message.
        
        Args:
            message: Message content
            sender_id: Sender agent ID
        
        Returns:
            Response or acknowledgment
        """
        # Record in message history
        received_msg = {
            "type": "received",
            "sender_id": sender_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.message_history.append(received_msg)
        
        # Record interaction
        self.interactions.append(received_msg)
        
        # Process message (base implementation)
        return self._process_message(message, sender_id)
    
    def _process_message(self, message: Dict, sender_id: str) -> Dict:
        """Process received message - override in subclasses"""
        return {
            "acknowledged": True,
            "agent_id": self.agent_id
        }
    
    def update_resources(self, resource_changes: Dict[str, float]) -> None:
        """Update agent resources"""
        for resource, change in resource_changes.items():
            current = self.resources.get(resource, 0.0)
            self.resources[resource] = max(0.0, current + change)
    
    def add_reward(self, reward: float, reason: str = "") -> None:
        """Add reward to agent"""
        self.rewards_received += reward
        
        # Record reward
        self.interactions.append({
            "type": "reward",
            "amount": reward,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def form_alliance(self, other_agent_id: str) -> None:
        """Form alliance with another agent"""
        if other_agent_id not in self.allies:
            self.allies.append(other_agent_id)
    
    def break_alliance(self, other_agent_id: str) -> None:
        """Break alliance with another agent"""
        if other_agent_id in self.allies:
            self.allies.remove(other_agent_id)
    
    def get_status(self) -> Dict:
        """Get agent status summary"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "name": self.name,
            "state": self.state.value,
            "resources": self.resources,
            "goals": self.goals,
            "rewards_received": self.rewards_received,
            "actions_taken": len(self.actions_taken),
            "interactions": len(self.interactions),
            "allies": len(self.allies),
            "created_at": self.created_at
        }
    
    def to_dict(self) -> Dict:
        """Serialize agent to dictionary"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "name": self.name,
            "state": self.state.value,
            "resources": self.resources,
            "goals": self.goals,
            "beliefs": self.beliefs,
            "preferences": self.preferences,
            "rewards_received": self.rewards_received,
            "actions_count": len(self.actions_taken),
            "interactions_count": len(self.interactions),
            "allies": self.allies,
            "opponents": self.opponents,
            "created_at": self.created_at
        }
