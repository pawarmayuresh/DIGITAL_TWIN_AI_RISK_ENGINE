"""
Training Pipeline - Orchestrates the RL training process.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from .experience_store import ExperienceStore
from .reward_model import RewardModel
from .rl_agent import RLAgent
from .adaptive_policy import AdaptivePolicyLearner
from .model_updater import ModelUpdater


class TrainingPipeline:
    """Orchestrates the complete RL training process."""
    
    def __init__(
        self,
        agent: RLAgent,
        experience_store: ExperienceStore,
        reward_model: RewardModel,
        policy_learner: AdaptivePolicyLearner,
        model_updater: ModelUpdater
    ):
        self.agent = agent
        self.experience_store = experience_store
        self.reward_model = reward_model
        self.policy_learner = policy_learner
        self.model_updater = model_updater
        
        self.training_active = False
        self.training_history: List[Dict[str, Any]] = []
        self.callbacks: List[Callable] = []
    
    def train_episode(
        self,
        environment_step_fn: Callable,
        max_steps: int = 100,
        context: str = 'default'
    ) -> Dict[str, Any]:
        """Train for one episode."""
        
        episode_id = self.experience_store.start_episode()
        episode_reward = 0.0
        episode_data = []
        
        # Initialize environment
        state = environment_step_fn('reset', {})
        
        for step in range(max_steps):
            # Select action
            action_type, action_params = self.agent.select_action(state, explore=True)
            
            # Adapt action based on learned policy
            adapted_action = self.policy_learner.get_adapted_action(
                state, action_type, context
            )
            if adapted_action != action_type:
                action_type = adapted_action
                action_params = self.agent._generate_action_params(action_type, state)
            
            # Execute action in environment
            next_state = environment_step_fn('step', {
                'action_type': action_type,
                'action_params': action_params
            })
            
            # Calculate reward
            reward_info = self.reward_model.calculate_reward(state, action_params, next_state)
            reward = reward_info['total_reward']
            
            # Check if episode is done
            done = next_state.get('done', False) or step == max_steps - 1
            
            # Store experience
            self.experience_store.add_experience(
                state=state,
                action={'type': action_type, **action_params},
                reward=reward,
                next_state=next_state,
                done=done,
                metadata={'step': step, 'context': context}
            )
            
            # Update agent
            self.agent.update(state, action_type, reward, next_state, done)
            
            # Record step data
            episode_data.append({
                'state': state,
                'action': {'type': action_type, **action_params},
                'reward': reward,
                'next_state': next_state,
                'done': done
            })
            
            episode_reward += reward
            state = next_state
            
            if done:
                break
        
        # End episode
        self.experience_store.end_episode()
        
        # Learn from episode
        self.policy_learner.learn_from_episode(episode_data, episode_reward, context)
        
        # Check for model updates
        if self.model_updater.should_update(self.agent.training_steps):
            update_result = self.model_updater.apply_updates(self.agent)
        else:
            update_result = {'updates_applied': 0}
        
        # Record training history
        episode_summary = {
            'episode_id': episode_id,
            'context': context,
            'steps': len(episode_data),
            'total_reward': episode_reward,
            'avg_reward': episode_reward / len(episode_data),
            'epsilon': self.agent.epsilon,
            'updates_applied': update_result['updates_applied'],
            'timestamp': datetime.now().isoformat()
        }
        self.training_history.append(episode_summary)
        
        # Execute callbacks
        for callback in self.callbacks:
            callback(episode_summary)
        
        return episode_summary
    
    def train_batch(
        self,
        environment_step_fn: Callable,
        num_episodes: int = 10,
        max_steps_per_episode: int = 100,
        context: str = 'default'
    ) -> Dict[str, Any]:
        """Train for multiple episodes."""
        
        self.training_active = True
        batch_results = []
        
        for episode_num in range(num_episodes):
            if not self.training_active:
                break
            
            episode_result = self.train_episode(
                environment_step_fn,
                max_steps_per_episode,
                context
            )
            batch_results.append(episode_result)
        
        # Batch statistics
        total_reward = sum(r['total_reward'] for r in batch_results)
        avg_reward = total_reward / len(batch_results)
        
        return {
            'episodes_completed': len(batch_results),
            'total_reward': total_reward,
            'avg_reward_per_episode': avg_reward,
            'best_episode_reward': max(r['total_reward'] for r in batch_results),
            'worst_episode_reward': min(r['total_reward'] for r in batch_results),
            'final_epsilon': self.agent.epsilon,
            'training_steps': self.agent.training_steps
        }
    
    def train_from_replay(self, batch_size: int = 32, num_batches: int = 10) -> Dict[str, Any]:
        """Train from experience replay."""
        
        if len(self.experience_store.experiences) < batch_size:
            return {'status': 'insufficient_data', 'updates': 0}
        
        updates_performed = 0
        
        for _ in range(num_batches):
            # Sample batch
            batch = self.experience_store.sample_batch(batch_size)
            
            # Update from each experience
            for exp in batch:
                action_type = exp.action.get('type', 'unknown')
                self.agent.update(
                    exp.state,
                    action_type,
                    exp.reward,
                    exp.next_state,
                    exp.done
                )
                updates_performed += 1
        
        return {
            'status': 'success',
            'updates': updates_performed,
            'batch_size': batch_size,
            'num_batches': num_batches
        }
    
    def stop_training(self):
        """Stop ongoing training."""
        self.training_active = False
    
    def add_callback(self, callback: Callable):
        """Add a callback function to be called after each episode."""
        self.callbacks.append(callback)
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get summary of training progress."""
        if not self.training_history:
            return {'status': 'no_training'}
        
        recent_episodes = self.training_history[-10:]
        
        return {
            'total_episodes': len(self.training_history),
            'total_steps': self.agent.training_steps,
            'recent_avg_reward': sum(e['total_reward'] for e in recent_episodes) / len(recent_episodes),
            'overall_avg_reward': sum(e['total_reward'] for e in self.training_history) / len(self.training_history),
            'current_epsilon': self.agent.epsilon,
            'experience_store_size': len(self.experience_store.experiences),
            'model_version': self.model_updater.current_version
        }
