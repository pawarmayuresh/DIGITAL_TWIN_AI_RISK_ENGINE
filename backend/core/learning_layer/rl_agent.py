"""
RL Agent - Core reinforcement learning agent for disaster response.
"""

from typing import Dict, Any, List, Optional, Tuple
import random
import math
from collections import defaultdict


class RLAgent:
    """Reinforcement Learning Agent using Q-Learning with function approximation."""
    
    def __init__(
        self,
        action_space: List[str],
        learning_rate: float = 0.01,
        discount_factor: float = 0.95,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01
    ):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # Q-table approximation (state features -> action -> Q-value)
        self.q_table: Dict[str, Dict[str, float]] = defaultdict(lambda: {a: 0.0 for a in action_space})
        
        # Training statistics
        self.training_steps = 0
        self.episodes_completed = 0
        self.total_reward = 0.0
    
    def select_action(
        self,
        state: Dict[str, Any],
        explore: bool = True
    ) -> Tuple[str, Dict[str, Any]]:
        """Select an action using epsilon-greedy policy."""
        
        # Epsilon-greedy exploration
        if explore and random.random() < self.epsilon:
            action_type = random.choice(self.action_space)
            action_params = self._generate_action_params(action_type, state)
            return action_type, action_params
        
        # Exploitation: choose best action
        state_key = self._state_to_key(state)
        q_values = self.q_table[state_key]
        
        best_action = max(q_values.items(), key=lambda x: x[1])[0]
        action_params = self._generate_action_params(best_action, state)
        
        return best_action, action_params
    
    def update(
        self,
        state: Dict[str, Any],
        action: str,
        reward: float,
        next_state: Dict[str, Any],
        done: bool
    ):
        """Update Q-values using Q-learning update rule."""
        
        state_key = self._state_to_key(state)
        next_state_key = self._state_to_key(next_state)
        
        # Current Q-value
        current_q = self.q_table[state_key][action]
        
        # Maximum Q-value for next state
        if done:
            max_next_q = 0.0
        else:
            max_next_q = max(self.q_table[next_state_key].values())
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        
        self.q_table[state_key][action] = new_q
        
        # Update statistics
        self.training_steps += 1
        self.total_reward += reward
        
        # Decay epsilon
        if done:
            self.episodes_completed += 1
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def _state_to_key(self, state: Dict[str, Any]) -> str:
        """Convert state dict to a hashable key."""
        # Extract key features for state representation
        features = []
        
        # Disaster severity
        features.append(f"sev_{state.get('disaster_severity', 0):.1f}")
        
        # Infrastructure health
        features.append(f"inf_{state.get('infrastructure_health', 100):.0f}")
        
        # Resource availability
        features.append(f"res_{state.get('resources_available', 0):.0f}")
        
        # Casualties
        casualties = state.get('casualties', 0)
        if casualties < 10:
            features.append("cas_low")
        elif casualties < 100:
            features.append("cas_med")
        else:
            features.append("cas_high")
        
        # Time step
        time_step = state.get('time_step', 0)
        if time_step < 5:
            features.append("time_early")
        elif time_step < 15:
            features.append("time_mid")
        else:
            features.append("time_late")
        
        return "|".join(features)
    
    def _generate_action_params(
        self,
        action_type: str,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate parameters for an action based on state."""
        
        params = {
            'action_type': action_type,
            'timestamp': state.get('timestamp', ''),
            'priority': 'high' if state.get('disaster_severity', 0) > 7 else 'medium'
        }
        
        # Action-specific parameters
        if action_type == 'evacuate':
            params['zones'] = self._select_evacuation_zones(state)
            params['resources'] = min(state.get('resources_available', 0) * 0.3, 1000)
        
        elif action_type == 'deploy_resources':
            params['resource_type'] = 'emergency_services'
            params['amount'] = min(state.get('resources_available', 0) * 0.5, 2000)
            params['target_area'] = 'high_risk_zone'
        
        elif action_type == 'infrastructure_repair':
            params['target'] = 'critical_infrastructure'
            params['resources'] = min(state.get('resources_available', 0) * 0.4, 1500)
        
        elif action_type == 'form_coalition':
            params['agents'] = ['emergency', 'infrastructure', 'government']
            params['objective'] = 'disaster_response'
        
        elif action_type == 'monitor':
            params['duration'] = 1
            params['areas'] = ['all']
        
        return params
    
    def _select_evacuation_zones(self, state: Dict[str, Any]) -> List[str]:
        """Select zones for evacuation based on state."""
        severity = state.get('disaster_severity', 0)
        if severity > 8:
            return ['zone_a', 'zone_b', 'zone_c']
        elif severity > 5:
            return ['zone_a', 'zone_b']
        else:
            return ['zone_a']
    
    def get_policy(self) -> Dict[str, Dict[str, float]]:
        """Get the current policy (Q-values)."""
        return dict(self.q_table)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get training statistics."""
        return {
            'training_steps': self.training_steps,
            'episodes_completed': self.episodes_completed,
            'total_reward': self.total_reward,
            'avg_reward_per_episode': self.total_reward / max(self.episodes_completed, 1),
            'epsilon': self.epsilon,
            'q_table_size': len(self.q_table),
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor
        }
    
    def save_policy(self, filepath: str):
        """Save policy to file."""
        import json
        with open(filepath, 'w') as f:
            json.dump({
                'q_table': dict(self.q_table),
                'statistics': self.get_statistics(),
                'hyperparameters': {
                    'learning_rate': self.learning_rate,
                    'discount_factor': self.discount_factor,
                    'epsilon': self.epsilon
                }
            }, f, indent=2)
    
    def load_policy(self, filepath: str):
        """Load policy from file."""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.q_table = defaultdict(lambda: {a: 0.0 for a in self.action_space})
        for state_key, actions in data['q_table'].items():
            self.q_table[state_key] = actions
        
        stats = data.get('statistics', {})
        self.training_steps = stats.get('training_steps', 0)
        self.episodes_completed = stats.get('episodes_completed', 0)
        self.total_reward = stats.get('total_reward', 0.0)
