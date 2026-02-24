"""
Multi-Agent System API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from backend.core.multi_agent_system import (
    AgentManager,
    AgentType,
    CitizenAgent,
    GovernmentAgent,
    InfrastructureAgent,
    EmergencyAgent,
    NegotiationEngine,
    CoalitionBuilder,
    RewardTracker,
    RewardType
)

router = APIRouter()

# Global instances
agent_manager = AgentManager()
negotiation_engine = NegotiationEngine()
coalition_builder = CoalitionBuilder()
reward_tracker = RewardTracker()


# ============= Request Models =============

class CreateAgentRequest(BaseModel):
    agent_type: str
    agent_id: str
    position: Optional[Dict] = None
    resources: Optional[Dict] = None


class SendMessageRequest(BaseModel):
    sender_id: str
    recipient_id: str
    message: Dict


class CreateProposalRequest(BaseModel):
    proposer_id: str
    recipient_id: str
    offer: Dict


class CounterOfferRequest(BaseModel):
    proposal_id: str
    counter_offer: Dict


class ProposalActionRequest(BaseModel):
    proposal_id: str
    reason: Optional[str] = ""


class CreateCoalitionRequest(BaseModel):
    name: str
    leader_id: str
    goals: List[str]


class CoalitionMemberRequest(BaseModel):
    coalition_id: str
    agent_id: str


class ContributeResourcesRequest(BaseModel):
    coalition_id: str
    agent_id: str
    resources: Dict


class GiveRewardRequest(BaseModel):
    agent_id: str
    reward_type: str
    amount: float
    reason: str
    metadata: Optional[Dict] = None


class DistributeRewardRequest(BaseModel):
    coalition_members: List[str]
    total_reward: float
    distribution_strategy: str = "equal"


# ============= Agent Management =============

@router.post("/agents/create")
def create_agent(request: CreateAgentRequest):
    """Create a new agent"""
    try:
        agent_type = AgentType(request.agent_type)
        
        # Create appropriate agent type
        if agent_type == AgentType.CITIZEN:
            agent = CitizenAgent(
                agent_id=request.agent_id,
                name=request.agent_id,  # Use agent_id as name if not provided
                family_size=request.resources.get("family_size", 1) if request.resources else 1,
                location=request.resources.get("location", "unknown") if request.resources else "unknown"
            )
        elif agent_type == AgentType.GOVERNMENT:
            agent = GovernmentAgent(
                agent_id=request.agent_id,
                name=request.agent_id,
                budget=request.resources.get("budget", 1000000) if request.resources else 1000000
            )
        elif agent_type == AgentType.INFRASTRUCTURE:
            agent = InfrastructureAgent(
                agent_id=request.agent_id,
                name=request.agent_id,
                managed_assets=request.resources.get("assets", []) if request.resources else []
            )
        elif agent_type == AgentType.EMERGENCY:
            agent = EmergencyAgent(
                agent_id=request.agent_id,
                name=request.agent_id,
                unit_type=request.resources.get("unit_type", "general") if request.resources else "general"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown agent type: {request.agent_type}")
        
        agent_manager.register_agent(agent)
        
        return {
            "success": True,
            "agent": agent.to_dict()
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/agents")
def get_all_agents():
    """Get all registered agents"""
    agents = agent_manager.get_all_agents_dict()
    return {
        "agents": agents,
        "count": len(agents)
    }


@router.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    """Get specific agent"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent.to_dict()


@router.delete("/agents/{agent_id}")
def remove_agent(agent_id: str):
    """Remove an agent"""
    success = agent_manager.unregister_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {"success": True, "message": f"Agent {agent_id} removed"}


@router.get("/agents/type/{agent_type}")
def get_agents_by_type(agent_type: str):
    """Get agents by type"""
    try:
        agent_type_enum = AgentType(agent_type)
        agents = agent_manager.get_agents_by_type(agent_type_enum)
        return {
            "agents": [a.to_dict() for a in agents],
            "count": len(agents)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid agent type: {agent_type}")


# ============= Communication =============

@router.post("/communication/send")
def send_message(request: SendMessageRequest):
    """Send message between agents"""
    sender = agent_manager.get_agent(request.sender_id)
    recipient = agent_manager.get_agent(request.recipient_id)
    
    if not sender or not recipient:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    sender.send_message(recipient, request.message)
    
    return {
        "success": True,
        "message": "Message sent",
        "from": request.sender_id,
        "to": request.recipient_id
    }


@router.get("/communication/{agent_id}/messages")
def get_agent_messages(agent_id: str):
    """Get agent's message history"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent_id,
        "messages": agent.message_history
    }


# ============= Negotiation =============

@router.post("/negotiation/propose")
def create_proposal(request: CreateProposalRequest):
    """Create a negotiation proposal"""
    proposal = negotiation_engine.create_proposal(
        proposer_id=request.proposer_id,
        recipient_id=request.recipient_id,
        offer=request.offer
    )
    
    return {
        "success": True,
        "proposal": proposal.to_dict()
    }


@router.post("/negotiation/counter")
def counter_offer(request: CounterOfferRequest):
    """Make a counter-offer"""
    proposal = negotiation_engine.counter_offer(
        proposal_id=request.proposal_id,
        counter_offer=request.counter_offer
    )
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {
        "success": True,
        "proposal": proposal.to_dict()
    }


@router.post("/negotiation/accept")
def accept_proposal(request: ProposalActionRequest):
    """Accept a proposal"""
    result = negotiation_engine.accept_proposal(request.proposal_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {
        "success": True,
        "result": result
    }


@router.post("/negotiation/reject")
def reject_proposal(request: ProposalActionRequest):
    """Reject a proposal"""
    result = negotiation_engine.reject_proposal(
        proposal_id=request.proposal_id,
        reason=request.reason
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    return {
        "success": True,
        "result": result
    }


@router.get("/negotiation/proposals")
def get_all_proposals():
    """Get all proposals"""
    proposals = negotiation_engine.get_all_proposals()
    return {
        "proposals": proposals,
        "count": len(proposals)
    }


@router.get("/negotiation/agent/{agent_id}")
def get_agent_proposals(agent_id: str):
    """Get active proposals for an agent"""
    proposals = negotiation_engine.get_active_proposals(agent_id)
    return {
        "agent_id": agent_id,
        "proposals": [p.to_dict() for p in proposals],
        "count": len(proposals)
    }


# ============= Coalitions =============

@router.post("/coalitions/create")
def create_coalition(request: CreateCoalitionRequest):
    """Create a new coalition"""
    coalition = coalition_builder.create_coalition(
        name=request.name,
        leader_id=request.leader_id,
        goals=request.goals
    )
    
    return {
        "success": True,
        "coalition": coalition.to_dict()
    }


@router.post("/coalitions/add-member")
def add_coalition_member(request: CoalitionMemberRequest):
    """Add member to coalition"""
    success = coalition_builder.add_member(
        coalition_id=request.coalition_id,
        agent_id=request.agent_id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Coalition not found")
    
    return {
        "success": True,
        "message": f"Agent {request.agent_id} added to coalition"
    }


@router.post("/coalitions/remove-member")
def remove_coalition_member(request: CoalitionMemberRequest):
    """Remove member from coalition"""
    success = coalition_builder.remove_member(
        coalition_id=request.coalition_id,
        agent_id=request.agent_id
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove member")
    
    return {
        "success": True,
        "message": f"Agent {request.agent_id} removed from coalition"
    }


@router.post("/coalitions/{coalition_id}/activate")
def activate_coalition(coalition_id: str):
    """Activate a coalition"""
    success = coalition_builder.activate_coalition(coalition_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Coalition not found")
    
    return {
        "success": True,
        "message": f"Coalition {coalition_id} activated"
    }


@router.post("/coalitions/{coalition_id}/dissolve")
def dissolve_coalition(coalition_id: str):
    """Dissolve a coalition"""
    success = coalition_builder.dissolve_coalition(coalition_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Coalition not found")
    
    return {
        "success": True,
        "message": f"Coalition {coalition_id} dissolved"
    }


@router.post("/coalitions/contribute")
def contribute_resources(request: ContributeResourcesRequest):
    """Contribute resources to coalition"""
    success = coalition_builder.contribute_resources(
        coalition_id=request.coalition_id,
        agent_id=request.agent_id,
        resources=request.resources
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to contribute resources")
    
    return {
        "success": True,
        "message": "Resources contributed"
    }


@router.get("/coalitions")
def get_all_coalitions():
    """Get all coalitions"""
    coalitions = coalition_builder.get_all_coalitions()
    return {
        "coalitions": coalitions,
        "count": len(coalitions)
    }


@router.get("/coalitions/{coalition_id}")
def get_coalition(coalition_id: str):
    """Get specific coalition"""
    coalition = coalition_builder.get_coalition(coalition_id)
    
    if not coalition:
        raise HTTPException(status_code=404, detail="Coalition not found")
    
    return coalition.to_dict()


@router.get("/coalitions/agent/{agent_id}")
def get_agent_coalitions(agent_id: str):
    """Get coalitions an agent belongs to"""
    coalitions = coalition_builder.get_agent_coalitions(agent_id)
    return {
        "agent_id": agent_id,
        "coalitions": [c.to_dict() for c in coalitions],
        "count": len(coalitions)
    }


@router.get("/coalitions/{coalition_id}/strength")
def get_coalition_strength(coalition_id: str):
    """Get coalition strength metrics"""
    strength = coalition_builder.get_coalition_strength(coalition_id)
    
    if not strength:
        raise HTTPException(status_code=404, detail="Coalition not found")
    
    return strength


# ============= Rewards =============

@router.post("/rewards/give")
def give_reward(request: GiveRewardRequest):
    """Give reward to an agent"""
    try:
        reward_type = RewardType(request.reward_type)
        reward = reward_tracker.give_reward(
            agent_id=request.agent_id,
            reward_type=reward_type,
            amount=request.amount,
            reason=request.reason,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "reward": reward.to_dict()
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid reward type: {request.reward_type}")


@router.post("/rewards/distribute")
def distribute_coalition_reward(request: DistributeRewardRequest):
    """Distribute reward among coalition members"""
    rewards = reward_tracker.distribute_coalition_reward(
        coalition_members=request.coalition_members,
        total_reward=request.total_reward,
        distribution_strategy=request.distribution_strategy
    )
    
    return {
        "success": True,
        "rewards": [r.to_dict() for r in rewards],
        "count": len(rewards)
    }


@router.get("/rewards/agent/{agent_id}")
def get_agent_rewards(agent_id: str):
    """Get all rewards for an agent"""
    rewards = reward_tracker.get_agent_rewards(agent_id)
    total = reward_tracker.get_agent_total_reward(agent_id)
    
    return {
        "agent_id": agent_id,
        "rewards": [r.to_dict() for r in rewards],
        "total_reward": total,
        "count": len(rewards)
    }


@router.get("/rewards/agent/{agent_id}/statistics")
def get_agent_reward_statistics(agent_id: str):
    """Get reward statistics for an agent"""
    stats = reward_tracker.get_reward_statistics(agent_id)
    return stats


@router.get("/rewards/leaderboard")
def get_reward_leaderboard(limit: int = 10):
    """Get top performing agents"""
    top_performers = reward_tracker.get_top_performers(limit)
    return {
        "leaderboard": top_performers,
        "count": len(top_performers)
    }


@router.get("/rewards/recent")
def get_recent_rewards(limit: int = 50):
    """Get recent rewards"""
    rewards = reward_tracker.get_recent_rewards(limit)
    return {
        "rewards": rewards,
        "count": len(rewards)
    }


@router.get("/rewards")
def get_all_rewards():
    """Get all rewards"""
    rewards = reward_tracker.get_all_rewards()
    return {
        "rewards": rewards,
        "count": len(rewards)
    }
