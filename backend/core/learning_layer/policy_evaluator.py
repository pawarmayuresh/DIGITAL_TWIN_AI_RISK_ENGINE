"""
Policy Evaluator - Evaluates RL policy performance.
"""

from typing import Dict, Any, List, Optional
import statistics


class PolicyEvaluator:
    """Evaluates and compares RL policy performance."""
    
    def __init__(self):
        self.evaluation_results: List[Dict[str, Any]] = []
        self.baseline_performance: Optional[Dict[str, float]] = None
    
    def evaluate_policy(
        self,
        agent: Any,
        test_scenarios: List[Dict[str, Any]],
        simulation_trainer: Any,
        num_episodes_per_scenario: int = 5
    ) -> Dict[str, Any]:
        """Evaluate policy on test scenarios."""
        
        scenario_results = []
        
        for scenario in test_scenarios:
            # Run episodes without exploration
            episode_rewards = []
            
            for _ in range(num_episodes_per_scenario):
                episode_reward = self._run_evaluation_episode(
                    agent,
                    scenario,
                    simulation_trainer
                )
                episode_rewards.append(episode_reward)
            
            scenario_result = {
                'disaster_type': scenario['disaster_type'],
                'severity': scenario['severity'],
                'avg_reward': statistics.mean(episode_rewards),
                'std_reward': statistics.stdev(episode_rewards) if len(episode_rewards) > 1 else 0,
                'min_reward': min(episode_rewards),
                'max_reward': max(episode_rewards),
                'episodes': len(episode_rewards)
            }
            scenario_results.append(scenario_result)
        
        # Overall evaluation metrics
        all_rewards = [r['avg_reward'] for r in scenario_results]
        
        evaluation = {
            'scenarios_evaluated': len(test_scenarios),
            'total_episodes': len(test_scenarios) * num_episodes_per_scenario,
            'overall_avg_reward': statistics.mean(all_rewards),
            'overall_std_reward': statistics.stdev(all_rewards) if len(all_rewards) > 1 else 0,
            'best_scenario_performance': max(scenario_results, key=lambda x: x['avg_reward']),
            'worst_scenario_performance': min(scenario_results, key=lambda x: x['avg_reward']),
            'scenario_results': scenario_results,
            'agent_stats': agent.get_statistics()
        }
        
        self.evaluation_results.append(evaluation)
        return evaluation
    
    def _run_evaluation_episode(
        self,
        agent: Any,
        scenario: Dict[str, Any],
        simulation_trainer: Any
    ) -> float:
        """Run a single evaluation episode."""
        
        # Create environment
        environment = simulation_trainer.create_simulation_environment(
            scenario['disaster_type'],
            scenario['severity'],
            scenario.get('city_config', {})
        )
        
        episode_reward = 0.0
        state = environment['state']
        
        for step in range(20):  # Max 20 steps
            # Select action without exploration
            action_type, action_params = agent.select_action(state, explore=False)
            
            # Execute action
            next_state = simulation_trainer.simulation_step(
                environment,
                action_type,
                action_params
            )
            
            # Calculate reward (simplified)
            reward = self._calculate_evaluation_reward(state, next_state)
            episode_reward += reward
            
            state = next_state
            
            if state.get('done', False):
                break
        
        return episode_reward
    
    def _calculate_evaluation_reward(
        self,
        state: Dict[str, Any],
        next_state: Dict[str, Any]
    ) -> float:
        """Calculate reward for evaluation."""
        
        reward = 0.0
        
        # Lives saved
        casualties_reduced = state.get('casualties', 0) - next_state.get('casualties', 0)
        reward += casualties_reduced * 10
        
        # Infrastructure preserved
        infra_improved = next_state.get('infrastructure_health', 0) - state.get('infrastructure_health', 0)
        reward += infra_improved * 5
        
        # Cascading failures prevented
        cascades_reduced = state.get('cascading_failures', 0) - next_state.get('cascading_failures', 0)
        reward += cascades_reduced * 8
        
        return reward
    
    def compare_with_baseline(
        self,
        current_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare current policy with baseline."""
        
        if self.baseline_performance is None:
            self.baseline_performance = {
                'avg_reward': current_evaluation['overall_avg_reward']
            }
            return {
                'is_baseline': True,
                'improvement': 0.0
            }
        
        baseline_reward = self.baseline_performance['avg_reward']
        current_reward = current_evaluation['overall_avg_reward']
        
        improvement = ((current_reward - baseline_reward) / abs(baseline_reward)) * 100
        
        return {
            'is_baseline': False,
            'baseline_reward': baseline_reward,
            'current_reward': current_reward,
            'improvement_percent': improvement,
            'is_better': current_reward > baseline_reward
        }
    
    def set_baseline(self, evaluation: Dict[str, Any]):
        """Set a new baseline for comparison."""
        self.baseline_performance = {
            'avg_reward': evaluation['overall_avg_reward']
        }
    
    def get_performance_trend(self) -> Dict[str, Any]:
        """Get performance trend over evaluations."""
        
        if len(self.evaluation_results) < 2:
            return {'status': 'insufficient_data'}
        
        rewards = [e['overall_avg_reward'] for e in self.evaluation_results]
        
        # Calculate trend
        first_half = rewards[:len(rewards)//2]
        second_half = rewards[len(rewards)//2:]
        
        avg_first = statistics.mean(first_half)
        avg_second = statistics.mean(second_half)
        
        trend = 'improving' if avg_second > avg_first else 'declining'
        improvement = ((avg_second - avg_first) / abs(avg_first)) * 100
        
        return {
            'status': 'success',
            'trend': trend,
            'improvement_percent': improvement,
            'evaluations_analyzed': len(self.evaluation_results),
            'avg_reward_first_half': avg_first,
            'avg_reward_second_half': avg_second
        }
    
    def generate_evaluation_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report."""
        
        if not self.evaluation_results:
            return {'status': 'no_evaluations'}
        
        latest = self.evaluation_results[-1]
        trend = self.get_performance_trend()
        comparison = self.compare_with_baseline(latest)
        
        return {
            'latest_evaluation': latest,
            'performance_trend': trend,
            'baseline_comparison': comparison,
            'total_evaluations': len(self.evaluation_results),
            'recommendation': self._generate_recommendation(latest, trend, comparison)
        }
    
    def _generate_recommendation(
        self,
        latest: Dict[str, Any],
        trend: Dict[str, Any],
        comparison: Dict[str, Any]
    ) -> str:
        """Generate training recommendation."""
        
        if comparison.get('is_better', False) and trend.get('trend') == 'improving':
            return "Policy is performing well. Continue current training approach."
        
        elif trend.get('trend') == 'declining':
            return "Performance is declining. Consider adjusting hyperparameters or training on more diverse scenarios."
        
        elif not comparison.get('is_better', True):
            return "Policy is underperforming baseline. Increase training episodes or adjust reward function."
        
        else:
            return "Policy shows mixed results. Evaluate on additional scenarios for better assessment."
