"""
Agent Manager - Manages all agents in the system
"""

from typing import Dict, List, Optional
from .agent_base import AgentBase, AgentType


class AgentManager:
    """
    Manages all agents in the multi-agent system.
    Handles agent creation, coordination, and interaction.
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentBase] = {}
        self.agent_groups: Dict[AgentType, List[str]] = {
            agent_type: [] for agent_type in AgentType
        }
    
    def register_agent(self, agent: AgentBase) -> None:
        """Register a new agent"""
        self.agents[agent.agent_id] = agent
        
        # Add to type group
        if agent.agent_type not in self.agent_groups:
            self.agent_groups[agent.agent_type] = []
        self.agent_groups[agent.agent_type].append(agent.agent_id)
    
    def unregister_agent(self, agent_id: str) -> None:
        """Remove an agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            del self.agents[agent_id]
            
            # Remove from type group
            if agent.agent_type in self.agent_groups:
                if agent_id in self.agent_groups[agent.agent_type]:
                    self.agent_groups[agent.agent_type].remove(agent_id)
    
    def get_agent(self, agent_id: str) -> Optional[AgentBase]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[AgentBase]:
        """Get all agents of a specific type"""
        agent_ids = self.agent_groups.get(agent_type, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]
    
    def broadcast_message(self, message: Dict, sender_id: str) -> List[Dict]:
        """Broadcast message to all agents"""
        responses = []
        
        for agent_id, agent in self.agents.items():
            if agent_id != sender_id:
                response = agent.receive_message(message, sender_id)
                responses.append(response)
        
        return responses
    
    def facilitate_interaction(
        self,
        agent1_id: str,
        agent2_id: str,
        interaction_type: str
    ) -> Dict:
        """Facilitate interaction between two agents"""
        agent1 = self.get_agent(agent1_id)
        agent2 = self.get_agent(agent2_id)
        
        if not agent1 or not agent2:
            return {"error": "Agent not found"}
        
        # Record interaction
        interaction = {
            "agent1_id": agent1_id,
            "agent2_id": agent2_id,
            "interaction_type": interaction_type,
            "result": "completed"
        }
        
        return interaction
    
    def update_all_agents(self, environment: Dict) -> None:
        """Update all agents with environment state"""
        for agent in self.agents.values():
            agent.perceive(environment)
    
    def get_all_agents(self) -> List[AgentBase]:
        """Get all agent objects"""
        return list(self.agents.values())
    
    def get_all_agents_dict(self) -> List[Dict]:
        """Get all agents as dictionaries"""
        return [agent.to_dict() for agent in self.agents.values()]
    
    def get_agent_count(self) -> int:
        """Get total number of agents"""
        return len(self.agents)
    
    def get_agent_count_by_type(self) -> Dict[str, int]:
        """Get agent count by type"""
        return {
            agent_type.value: len(agent_ids)
            for agent_type, agent_ids in self.agent_groups.items()
        }
