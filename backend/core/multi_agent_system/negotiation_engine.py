"""
Negotiation Engine - Facilitates agent negotiations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class NegotiationStatus(Enum):
    """Status of negotiation"""
    PROPOSED = "proposed"
    COUNTER_OFFERED = "counter_offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class Proposal:
    """Represents a negotiation proposal"""
    proposal_id: str
    proposer_id: str
    recipient_id: str
    offer: Dict
    counter_offer: Optional[Dict] = None
    status: NegotiationStatus = NegotiationStatus.PROPOSED
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "proposal_id": self.proposal_id,
            "proposer_id": self.proposer_id,
            "recipient_id": self.recipient_id,
            "offer": self.offer,
            "counter_offer": self.counter_offer,
            "status": self.status.value,
            "timestamp": self.timestamp
        }


class NegotiationEngine:
    """
    Facilitates negotiations between agents.
    Handles proposals, counter-offers, and agreements.
    """
    
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.completed_negotiations: List[Dict] = []
    
    def create_proposal(
        self,
        proposer_id: str,
        recipient_id: str,
        offer: Dict
    ) -> Proposal:
        """Create a new proposal"""
        proposal_id = f"prop_{len(self.proposals)}_{datetime.utcnow().timestamp()}"
        
        proposal = Proposal(
            proposal_id=proposal_id,
            proposer_id=proposer_id,
            recipient_id=recipient_id,
            offer=offer
        )
        
        self.proposals[proposal_id] = proposal
        return proposal
    
    def counter_offer(
        self,
        proposal_id: str,
        counter_offer: Dict
    ) -> Optional[Proposal]:
        """Make a counter-offer"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return None
        
        proposal.counter_offer = counter_offer
        proposal.status = NegotiationStatus.COUNTER_OFFERED
        
        return proposal
    
    def accept_proposal(self, proposal_id: str) -> Optional[Dict]:
        """Accept a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return None
        
        proposal.status = NegotiationStatus.ACCEPTED
        
        # Record completed negotiation
        result = {
            "proposal": proposal.to_dict(),
            "outcome": "accepted",
            "timestamp": datetime.utcnow().isoformat()
        }
        self.completed_negotiations.append(result)
        
        return result
    
    def reject_proposal(self, proposal_id: str, reason: str = "") -> Optional[Dict]:
        """Reject a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            return None
        
        proposal.status = NegotiationStatus.REJECTED
        
        result = {
            "proposal": proposal.to_dict(),
            "outcome": "rejected",
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.completed_negotiations.append(result)
        
        return result
    
    def get_active_proposals(self, agent_id: str) -> List[Proposal]:
        """Get active proposals for an agent"""
        return [
            proposal for proposal in self.proposals.values()
            if (proposal.proposer_id == agent_id or proposal.recipient_id == agent_id)
            and proposal.status in [NegotiationStatus.PROPOSED, NegotiationStatus.COUNTER_OFFERED]
        ]
    
    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Get a specific proposal"""
        return self.proposals.get(proposal_id)
    
    def get_all_proposals(self) -> List[Dict]:
        """Get all proposals"""
        return [p.to_dict() for p in self.proposals.values()]
