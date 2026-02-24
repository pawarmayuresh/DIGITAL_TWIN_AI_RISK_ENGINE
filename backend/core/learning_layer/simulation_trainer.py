"""
Simulation Trainer - Trains RL agents using disaster simulations.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import random


class SimulationTrainer:
    """Trains RL agents using disaster simulation environments."""
    
    def __init__(self):
        self.simulation_scenarios: List[Dict[str, Any]] = []
        self.training_sessions: List[Dict[str, Any]] = []
        self.current_session: Optional[Dict[str, Any]] = None
    
    def create_simulation_environment(
        self,
        disaster_type: str,
        severity: float,
        city_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a simulation environment for training."""
        
        return {
            'disaster_type': disaster_type,
            'severity': severity,
            'city_config': city_config,
            'state': {
                'time_step': 0,
                'disaster_severity': severity,
                'infrastructure_health': 100,
                'casualties': 0,
                'resources_available': city_config.get('initial_resources', 5000),
                'economic_loss': 0,
                'cascading_failures': 0,
                'coalition_strength': 0,
                'done': False
            }
        }
    
    def simulation_step(
        self,
        environment: Dict[str, Any],
        action: str,
        action_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute one step in the simulation."""
        
        state = environment['state']
        disaster_type = environment['disaster_type']
        severity = environment['severity']
        
        # Simulate action effects
        new_state = state.copy()
        new_state['time_step'] += 1
        
        # Apply action effects
        if action == 'evacuate':
            # Evacuation reduces casualties but costs resources
            casualties_prevented = random.randint(10, 50) * (severity / 10)
            new_state['casualties'] = max(0, state['casualties'] - casualties_prevented)
            new_state['resources_available'] -= action_params.get('resources', 500)
        
        elif action == 'deploy_resources':
            # Resource deployment improves infrastructure
            infra_improvement = random.uniform(5, 15)
            new_state['infrastructure_health'] = min(100, state['infrastructure_health'] + infra_improvement)
            new_state['resources_available'] -= action_params.get('amount', 1000)
        
        elif action == 'infrastructure_repair':
            # Repairs prevent cascading failures
            new_state['cascading_failures'] = max(0, state['cascading_failures'] - 1)
            new_state['infrastructure_health'] = min(100, state['infrastructure_health'] + 10)
            new_state['resources_available'] -= action_params.get('resources', 800)
        
        elif action == 'form_coalition':
            # Coalitions improve coordination
            new_state['coalition_strength'] = min(10, state['coalition_strength'] + 2)
        
        elif action == 'monitor':
            # Monitoring has minimal cost
            new_state['resources_available'] -= 50
        
        # Simulate disaster progression
        disaster_impact = self._simulate_disaster_impact(disaster_type, severity, new_state)
        new_state.update(disaster_impact)
        
        # Check termination conditions
        if new_state['time_step'] >= 20 or new_state['resources_available'] <= 0:
            new_state['done'] = True
        
        environment['state'] = new_state
        return new_state
    
    def _simulate_disaster_impact(
        self,
        disaster_type: str,
        severity: float,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate ongoing disaster impact."""
        
        impact = {}
        
        # Base disaster damage
        base_damage = severity * random.uniform(0.5, 1.5)
        
        # Infrastructure degradation
        infra_damage = base_damage * 0.5
        impact['infrastructure_health'] = max(0, state['infrastructure_health'] - infra_damage)
        
        # Casualties increase if infrastructure is poor
        if state['infrastructure_health'] < 50:
            casualty_increase = int(base_damage * 2)
            impact['casualties'] = state['casualties'] + casualty_increase
        else:
            impact['casualties'] = state['casualties']
        
        # Economic losses
        economic_damage = base_damage * 1000
        impact['economic_loss'] = state['economic_loss'] + economic_damage
        
        # Cascading failures
        if state['infrastructure_health'] < 30:
            if random.random() < 0.3:
                impact['cascading_failures'] = state['cascading_failures'] + 1
        
        return impact
    
    def train_on_scenario(
        self,
        training_pipeline: Any,
        scenario: Dict[str, Any],
        num_episodes: int = 10
    ) -> Dict[str, Any]:
        """Train agent on a specific disaster scenario."""
        
        disaster_type = scenario['disaster_type']
        severity = scenario['severity']
        city_config = scenario.get('city_config', {})
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_session = {
            'session_id': session_id,
            'scenario': scenario,
            'episodes_completed': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # Create environment step function
        environment = None
        
        def environment_step_fn(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
            nonlocal environment
            
            if command == 'reset':
                environment = self.create_simulation_environment(
                    disaster_type, severity, city_config
                )
                return environment['state']
            
            elif command == 'step':
                action_type = params.get('action_type', 'monitor')
                action_params = params.get('action_params', {})
                return self.simulation_step(environment, action_type, action_params)
            
            return {}
        
        # Train using pipeline
        training_result = training_pipeline.train_batch(
            environment_step_fn,
            num_episodes=num_episodes,
            max_steps_per_episode=20,
            context=disaster_type
        )
        
        # Record session
        self.current_session['episodes_completed'] = num_episodes
        self.current_session['end_time'] = datetime.now().isoformat()
        self.current_session['results'] = training_result
        self.training_sessions.append(self.current_session)
        
        return training_result
    
    def train_on_multiple_scenarios(
        self,
        training_pipeline: Any,
        scenarios: List[Dict[str, Any]],
        episodes_per_scenario: int = 5
    ) -> Dict[str, Any]:
        """Train agent on multiple disaster scenarios."""
        
        all_results = []
        
        for scenario in scenarios:
            result = self.train_on_scenario(
                training_pipeline,
                scenario,
                episodes_per_scenario
            )
            all_results.append({
                'scenario': scenario['disaster_type'],
                'result': result
            })
        
        # Aggregate results
        total_episodes = sum(r['result']['episodes_completed'] for r in all_results)
        avg_reward = sum(r['result']['avg_reward_per_episode'] for r in all_results) / len(all_results)
        
        return {
            'scenarios_trained': len(scenarios),
            'total_episodes': total_episodes,
            'avg_reward_across_scenarios': avg_reward,
            'scenario_results': all_results
        }
    
    def generate_training_scenarios(self, num_scenarios: int = 10) -> List[Dict[str, Any]]:
        """Generate diverse training scenarios."""
        
        disaster_types = ['earthquake', 'flood', 'wildfire', 'pandemic', 'cyber_attack']
        scenarios = []
        
        for i in range(num_scenarios):
            scenario = {
                'scenario_id': f"scenario_{i+1}",
                'disaster_type': random.choice(disaster_types),
                'severity': random.uniform(3.0, 9.0),
                'city_config': {
                    'population': random.randint(50000, 500000),
                    'initial_resources': random.randint(3000, 10000),
                    'infrastructure_quality': random.uniform(0.5, 1.0)
                }
            }
            scenarios.append(scenario)
        
        self.simulation_scenarios.extend(scenarios)
        return scenarios
    
    def get_training_history(self) -> List[Dict[str, Any]]:
        """Get history of training sessions."""
        return self.training_sessions
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics about training sessions."""
        if not self.training_sessions:
            return {'total_sessions': 0}
        
        total_episodes = sum(s['episodes_completed'] for s in self.training_sessions)
        
        return {
            'total_sessions': len(self.training_sessions),
            'total_episodes': total_episodes,
            'scenarios_trained': len(set(s['scenario']['disaster_type'] for s in self.training_sessions)),
            'avg_episodes_per_session': total_episodes / len(self.training_sessions)
        }
