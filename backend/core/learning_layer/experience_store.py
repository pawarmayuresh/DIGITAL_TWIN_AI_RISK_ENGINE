"""
Experience Store - Stores and manages RL experiences (state, action, reward, next_state).
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import random


@dataclass
class Experience:
    """Single experience tuple for RL."""
    state: Dict[str, Any]
    action: Dict[str, Any]
    reward: float
    next_state: Dict[str, Any]
    done: bool
    timestamp: str
    episode_id: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExperienceStore:
    """Stores and manages experiences for replay and training."""
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.experiences: List[Experience] = []
        self.episodes: Dict[str, List[Experience]] = {}
        self.current_episode_id: Optional[str] = None
    
    def start_episode(self, episode_id: Optional[str] = None) -> str:
        """Start a new episode."""
        if episode_id is None:
            episode_id = f"episode_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        self.current_episode_id = episode_id
        self.episodes[episode_id] = []
        return episode_id
    
    def add_experience(
        self,
        state: Dict[str, Any],
        action: Dict[str, Any],
        reward: float,
        next_state: Dict[str, Any],
        done: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Experience:
        """Add a new experience to the store."""
        if self.current_episode_id is None:
            self.start_episode()
        
        experience = Experience(
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=done,
            timestamp=datetime.now().isoformat(),
            episode_id=self.current_episode_id,
            metadata=metadata or {}
        )
        
        self.experiences.append(experience)
        self.episodes[self.current_episode_id].append(experience)
        
        # Maintain max size
        if len(self.experiences) > self.max_size:
            removed = self.experiences.pop(0)
            # Clean up episode if empty
            if removed.episode_id in self.episodes:
                self.episodes[removed.episode_id] = [
                    e for e in self.episodes[removed.episode_id] 
                    if e != removed
                ]
                if not self.episodes[removed.episode_id]:
                    del self.episodes[removed.episode_id]
        
        return experience
    
    def end_episode(self) -> Optional[str]:
        """End the current episode."""
        episode_id = self.current_episode_id
        self.current_episode_id = None
        return episode_id
    
    def sample_batch(self, batch_size: int) -> List[Experience]:
        """Sample a random batch of experiences."""
        if len(self.experiences) < batch_size:
            return self.experiences.copy()
        return random.sample(self.experiences, batch_size)
    
    def get_episode(self, episode_id: str) -> List[Experience]:
        """Get all experiences from a specific episode."""
        return self.episodes.get(episode_id, [])
    
    def get_recent_episodes(self, n: int = 10) -> List[List[Experience]]:
        """Get the n most recent episodes."""
        episode_ids = sorted(self.episodes.keys(), reverse=True)[:n]
        return [self.episodes[eid] for eid in episode_ids]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored experiences."""
        if not self.experiences:
            return {
                'total_experiences': 0,
                'total_episodes': 0,
                'avg_episode_length': 0,
                'avg_reward': 0
            }
        
        return {
            'total_experiences': len(self.experiences),
            'total_episodes': len(self.episodes),
            'avg_episode_length': len(self.experiences) / max(len(self.episodes), 1),
            'avg_reward': sum(e.reward for e in self.experiences) / len(self.experiences),
            'max_reward': max(e.reward for e in self.experiences),
            'min_reward': min(e.reward for e in self.experiences)
        }
    
    def clear(self):
        """Clear all stored experiences."""
        self.experiences.clear()
        self.episodes.clear()
        self.current_episode_id = None
    
    def save_to_file(self, filepath: str):
        """Save experiences to a JSON file."""
        data = {
            'experiences': [e.to_dict() for e in self.experiences],
            'statistics': self.get_statistics()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load experiences from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.clear()
        for exp_dict in data['experiences']:
            exp = Experience(**exp_dict)
            self.experiences.append(exp)
            if exp.episode_id not in self.episodes:
                self.episodes[exp.episode_id] = []
            self.episodes[exp.episode_id].append(exp)
