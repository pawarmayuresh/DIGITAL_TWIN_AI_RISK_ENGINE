"""
Adaptive Policy Learner - Learns and adapts policies based on experience.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from collections import defaultdict


class AdaptivePolicyLearner:
    """Learns and adapts disaster response policies over time."""
    
    def __init__(self, adaptation_rate: float = 0.1):
        self.adaptation_rate = adaptation_rate
        self.policy_performance: Dict[str, List[float]] = defaultdict(list)
        self.context_policies: Dict[str, Dict[str, Any]] = {}
        self.adaptation_history: List[Dict[str, Any]] = []
    
    def learn_from_episode(
        self,
        episode_data: List[Dict[str, Any]],
        episode_reward: float,
        context: str = 'default'
    ):
        """Learn from a completed episode."""
        
        # Record performance
        self.policy_performance[context].append(episode_reward)
        
        # Extract patterns
        patterns = self._extract_patterns(episode_data)
        
        # Update context-specific policy
        if context not in self.context_policies:
            self.context_policies[context] = {
                'action_preferences': {},
                'state_action_pairs': [],
                'success_rate': 0.0
            }
        
        # Adapt policy based on performance
        if episode_reward > self._get_average_performance(context):
            # Reinforce successful patterns
            self._reinforce_patterns(context, patterns, episode_reward)
        else:
            # Explore alternatives
            self._explore_alternatives(context, patterns)
        
        # Record adaptation
        self.adaptation_history.append({
            'context': context,
            'episode_reward': episode_reward,
            'patterns_learned': len(patterns),
            'policy_updated': True
        })
    
    def get_adapted_action(
        self,
        state: Dict[str, Any],
        base_action: str,
        context: str = 'default'
    ) -> str:
        """Get adapted action based on learned policy."""
        
        if context not in self.context_policies:
            return base_action
        
        policy = self.context_policies[context]
        state_key = self._state_to_context(state)
        
        # Check if we have learned preferences for this state
        if state_key in policy['action_preferences']:
            preferences = policy['action_preferences'][state_key]
            # Return highest-rated action
            return max(preferences.items(), key=lambda x: x[1])[0]
        
        return base_action
    
    def _extract_patterns(self, episode_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract successful patterns from episode."""
        patterns = []
        
        for i, step in enumerate(episode_data):
            if step.get('reward', 0) > 0:
                pattern = {
                    'state_features': self._extract_state_features(step.get('state', {})),
                    'action': step.get('action', {}),
                    'reward': step.get('reward', 0),
                    'step': i
                }
                patterns.append(pattern)
        
        return patterns
    
    def _extract_state_features(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key features from state."""
        return {
            'disaster_severity': state.get('disaster_severity', 0),
            'infrastructure_health': state.get('infrastructure_health', 100),
            'resources_available': state.get('resources_available', 0),
            'casualties': state.get('casualties', 0),
            'time_step': state.get('time_step', 0)
        }
    
    def _state_to_context(self, state: Dict[str, Any]) -> str:
        """Convert state to context key."""
        features = self._extract_state_features(state)
        
        # Discretize features
        severity_bin = 'low' if features['disaster_severity'] < 5 else 'high'
        infra_bin = 'good' if features['infrastructure_health'] > 70 else 'damaged'
        resource_bin = 'abundant' if features['resources_available'] > 1000 else 'limited'
        
        return f"{severity_bin}_{infra_bin}_{resource_bin}"
    
    def _reinforce_patterns(
        self,
        context: str,
        patterns: List[Dict[str, Any]],
        episode_reward: float
    ):
        """Reinforce successful patterns."""
        policy = self.context_policies[context]
        
        for pattern in patterns:
            state_key = self._features_to_key(pattern['state_features'])
            action_type = pattern['action'].get('action_type', 'unknown')
            
            if state_key not in policy['action_preferences']:
                policy['action_preferences'][state_key] = {}
            
            # Increase preference for this action
            current_pref = policy['action_preferences'][state_key].get(action_type, 0.0)
            new_pref = current_pref + self.adaptation_rate * pattern['reward']
            policy['action_preferences'][state_key][action_type] = new_pref
    
    def _explore_alternatives(self, context: str, patterns: List[Dict[str, Any]]):
        """Explore alternative actions for unsuccessful episodes."""
        policy = self.context_policies[context]
        
        # Slightly decrease preferences for actions that didn't work well
        for pattern in patterns:
            state_key = self._features_to_key(pattern['state_features'])
            action_type = pattern['action'].get('action_type', 'unknown')
            
            if state_key in policy['action_preferences']:
                if action_type in policy['action_preferences'][state_key]:
                    current_pref = policy['action_preferences'][state_key][action_type]
                    policy['action_preferences'][state_key][action_type] = current_pref * 0.9
    
    def _features_to_key(self, features: Dict[str, Any]) -> str:
        """Convert features to a key."""
        return f"sev_{features['disaster_severity']:.1f}_inf_{features['infrastructure_health']:.0f}"
    
    def _get_average_performance(self, context: str) -> float:
        """Get average performance for a context."""
        if context not in self.policy_performance:
            return 0.0
        
        performances = self.policy_performance[context]
        if not performances:
            return 0.0
        
        # Use recent performance (last 10 episodes)
        recent = performances[-10:]
        return sum(recent) / len(recent)
    
    def get_policy_summary(self, context: str = 'default') -> Dict[str, Any]:
        """Get summary of learned policy."""
        if context not in self.context_policies:
            return {'context': context, 'learned': False}
        
        policy = self.context_policies[context]
        performances = self.policy_performance[context]
        
        return {
            'context': context,
            'learned': True,
            'num_state_action_pairs': len(policy['action_preferences']),
            'episodes_trained': len(performances),
            'avg_performance': sum(performances) / len(performances) if performances else 0,
            'recent_performance': self._get_average_performance(context),
            'improvement': self._calculate_improvement(performances)
        }
    
    def _calculate_improvement(self, performances: List[float]) -> float:
        """Calculate improvement over time."""
        if len(performances) < 2:
            return 0.0
        
        # Compare first 25% to last 25%
        n = len(performances)
        early = performances[:max(1, n // 4)]
        late = performances[-max(1, n // 4):]
        
        avg_early = sum(early) / len(early)
        avg_late = sum(late) / len(late)
        
        if avg_early == 0:
            return 0.0
        
        return ((avg_late - avg_early) / abs(avg_early)) * 100
    
    def get_all_contexts(self) -> List[str]:
        """Get all learned contexts."""
        return list(self.context_policies.keys())
