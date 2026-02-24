"""
Reward Tracker - Tracks and distributes rewards to agents
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class RewardType(Enum):
    """Types of rewards"""
    TASK_COMPLETION = "task_completion"
    COOPERATION = "cooperation"
    RESOURCE_SHARING = "resource_sharing"
    GOAL_ACHIEVEMENT = "goal_achievement"
    EFFICIENCY = "efficiency"
    INNOVATION = "innovation"


@dataclass
class Reward:
    """Represents a reward given to an agent"""
    reward_id: str
    agent_id: str
    reward_type: RewardType
    amount: float
    reason: str
    timestamp: str = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return {
            "reward_id": self.reward_id,
            "agent_id": self.agent_id,
            "reward_type": self.reward_type.value,
            "amount": self.amount,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class RewardTracker:
    """
    Tracks and distributes rewards to agents.
    Manages reward history and calculates agent performance metrics.
    """
    
    def __init__(self):
        self.rewards: Dict[str, Reward] = {}
        self.agent_rewards: Dict[str, List[str]] = {}  # agent_id -> reward_ids
        self.reward_counter = 0
    
    def give_reward(
        self,
        agent_id: str,
        reward_type: RewardType,
        amount: float,
        reason: str,
        metadata: Optional[Dict] = None
    ) -> Reward:
        """Give a reward to an agent"""
        self.reward_counter += 1
        reward_id = f"reward_{self.reward_counter}_{datetime.utcnow().timestamp()}"
        
        reward = Reward(
            reward_id=reward_id,
            agent_id=agent_id,
            reward_type=reward_type,
            amount=amount,
            reason=reason,
            metadata=metadata or {}
        )
        
        self.rewards[reward_id] = reward
        
        # Track agent rewards
        if agent_id not in self.agent_rewards:
            self.agent_rewards[agent_id] = []
        self.agent_rewards[agent_id].append(reward_id)
        
        return reward
    
    def get_agent_rewards(self, agent_id: str) -> List[Reward]:
        """Get all rewards for an agent"""
        reward_ids = self.agent_rewards.get(agent_id, [])
        return [self.rewards[rid] for rid in reward_ids if rid in self.rewards]
    
    def get_agent_total_reward(self, agent_id: str) -> float:
        """Get total reward amount for an agent"""
        rewards = self.get_agent_rewards(agent_id)
        return sum(r.amount for r in rewards)
    
    def get_agent_reward_by_type(
        self,
        agent_id: str,
        reward_type: RewardType
    ) -> float:
        """Get total reward of specific type for an agent"""
        rewards = self.get_agent_rewards(agent_id)
        return sum(r.amount for r in rewards if r.reward_type == reward_type)
    
    def get_top_performers(self, limit: int = 10) -> List[Dict]:
        """Get top performing agents by total reward"""
        agent_totals = []
        
        for agent_id in self.agent_rewards.keys():
            total = self.get_agent_total_reward(agent_id)
            agent_totals.append({
                "agent_id": agent_id,
                "total_reward": total,
                "reward_count": len(self.agent_rewards[agent_id])
            })
        
        # Sort by total reward descending
        agent_totals.sort(key=lambda x: x["total_reward"], reverse=True)
        
        return agent_totals[:limit]
    
    def get_reward_statistics(self, agent_id: str) -> Dict:
        """Get detailed reward statistics for an agent"""
        rewards = self.get_agent_rewards(agent_id)
        
        if not rewards:
            return {
                "agent_id": agent_id,
                "total_rewards": 0,
                "total_amount": 0.0,
                "average_reward": 0.0,
                "by_type": {}
            }
        
        by_type = {}
        for reward_type in RewardType:
            type_rewards = [r for r in rewards if r.reward_type == reward_type]
            if type_rewards:
                by_type[reward_type.value] = {
                    "count": len(type_rewards),
                    "total": sum(r.amount for r in type_rewards),
                    "average": sum(r.amount for r in type_rewards) / len(type_rewards)
                }
        
        total_amount = sum(r.amount for r in rewards)
        
        return {
            "agent_id": agent_id,
            "total_rewards": len(rewards),
            "total_amount": total_amount,
            "average_reward": total_amount / len(rewards),
            "by_type": by_type
        }
    
    def distribute_coalition_reward(
        self,
        coalition_members: List[str],
        total_reward: float,
        distribution_strategy: str = "equal"
    ) -> List[Reward]:
        """Distribute reward among coalition members"""
        if not coalition_members:
            return []
        
        rewards = []
        
        if distribution_strategy == "equal":
            # Equal distribution
            amount_per_member = total_reward / len(coalition_members)
            for agent_id in coalition_members:
                reward = self.give_reward(
                    agent_id=agent_id,
                    reward_type=RewardType.COOPERATION,
                    amount=amount_per_member,
                    reason="Coalition reward distribution",
                    metadata={"distribution": "equal", "coalition_size": len(coalition_members)}
                )
                rewards.append(reward)
        
        elif distribution_strategy == "leader_bonus":
            # Leader gets 40%, others split 60%
            if len(coalition_members) == 1:
                amount_per_member = total_reward
            else:
                leader_amount = total_reward * 0.4
                member_amount = (total_reward * 0.6) / (len(coalition_members) - 1)
                
                # Give leader reward
                reward = self.give_reward(
                    agent_id=coalition_members[0],
                    reward_type=RewardType.COOPERATION,
                    amount=leader_amount,
                    reason="Coalition leader reward",
                    metadata={"distribution": "leader_bonus", "role": "leader"}
                )
                rewards.append(reward)
                
                # Give member rewards
                for agent_id in coalition_members[1:]:
                    reward = self.give_reward(
                        agent_id=agent_id,
                        reward_type=RewardType.COOPERATION,
                        amount=member_amount,
                        reason="Coalition member reward",
                        metadata={"distribution": "leader_bonus", "role": "member"}
                    )
                    rewards.append(reward)
        
        return rewards
    
    def get_all_rewards(self) -> List[Dict]:
        """Get all rewards"""
        return [r.to_dict() for r in self.rewards.values()]
    
    def get_recent_rewards(self, limit: int = 50) -> List[Dict]:
        """Get most recent rewards"""
        all_rewards = list(self.rewards.values())
        all_rewards.sort(key=lambda r: r.timestamp, reverse=True)
        return [r.to_dict() for r in all_rewards[:limit]]
