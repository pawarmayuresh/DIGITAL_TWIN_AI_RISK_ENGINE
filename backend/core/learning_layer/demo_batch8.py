"""
Batch 8 Demo - Learning Layer (Reinforcement Learning)
Demonstrates AI learning optimal disaster response strategies.
"""

from .experience_store import ExperienceStore
from .reward_model import RewardModel, RewardWeights
from .rl_agent import RLAgent
from .adaptive_policy import AdaptivePolicyLearner
from .model_updater import ModelUpdater
from .training_pipeline import TrainingPipeline
from .checkpoint_manager import CheckpointManager
from .simulation_trainer import SimulationTrainer
from .policy_evaluator import PolicyEvaluator


def demo_experience_store():
    """Demo: Experience storage and replay."""
    print("\n=== Experience Store Demo ===")
    
    store = ExperienceStore(max_size=100)
    
    # Start episode
    episode_id = store.start_episode()
    print(f"Started episode: {episode_id}")
    
    # Add experiences
    for i in range(5):
        store.add_experience(
            state={'time_step': i, 'casualties': 100 - i*10},
            action={'type': 'evacuate', 'zones': ['zone_a']},
            reward=10.0 + i,
            next_state={'time_step': i+1, 'casualties': 90 - i*10},
            done=False
        )
    
    store.end_episode()
    
    # Sample batch
    batch = store.sample_batch(3)
    print(f"Sampled {len(batch)} experiences")
    
    # Statistics
    stats = store.get_statistics()
    print(f"Store statistics: {stats}")
    
    return store


def demo_reward_model():
    """Demo: Reward calculation."""
    print("\n=== Reward Model Demo ===")
    
    model = RewardModel()
    
    state_before = {
        'casualties': 100,
        'infrastructure_health': 80,
        'economic_loss': 1000000,
        'cascading_failures': 2
    }
    
    action = {
        'type': 'evacuate',
        'resources': 500,
        'response_time': 2
    }
    
    state_after = {
        'casualties': 70,
        'infrastructure_health': 85,
        'economic_loss': 1200000,
        'cascading_failures': 1,
        'action_effectiveness': 0.8,
        'coalition_strength': 5
    }
    
    reward_info = model.calculate_reward(state_before, action, state_after)
    print(f"Total reward: {reward_info['total_reward']:.2f}")
    print(f"Components: {reward_info['components']}")
    
    return model


def demo_rl_agent():
    """Demo: RL agent training."""
    print("\n=== RL Agent Demo ===")
    
    action_space = ['evacuate', 'deploy_resources', 'infrastructure_repair', 'form_coalition', 'monitor']
    agent = RLAgent(action_space, learning_rate=0.1, epsilon=1.0)
    
    # Simulate training
    state = {
        'disaster_severity': 7.5,
        'infrastructure_health': 75,
        'resources_available': 3000,
        'casualties': 50,
        'time_step': 5
    }
    
    # Select action
    action_type, action_params = agent.select_action(state, explore=True)
    print(f"Selected action: {action_type}")
    print(f"Action params: {action_params}")
    
    # Simulate next state
    next_state = state.copy()
    next_state['time_step'] = 6
    next_state['casualties'] = 40
    
    # Update agent
    agent.update(state, action_type, 15.0, next_state, False)
    
    stats = agent.get_statistics()
    print(f"Agent stats: {stats}")
    
    return agent


def demo_adaptive_policy():
    """Demo: Adaptive policy learning."""
    print("\n=== Adaptive Policy Demo ===")
    
    learner = AdaptivePolicyLearner(adaptation_rate=0.1)
    
    # Simulate episode data
    episode_data = [
        {
            'state': {'disaster_severity': 6.0, 'infrastructure_health': 80},
            'action': {'action_type': 'evacuate'},
            'reward': 12.0
        },
        {
            'state': {'disaster_severity': 6.5, 'infrastructure_health': 75},
            'action': {'action_type': 'deploy_resources'},
            'reward': 15.0
        }
    ]
    
    # Learn from episode
    learner.learn_from_episode(episode_data, episode_reward=27.0, context='earthquake')
    
    # Get adapted action
    test_state = {'disaster_severity': 6.0, 'infrastructure_health': 80}
    adapted = learner.get_adapted_action(test_state, 'monitor', 'earthquake')
    print(f"Adapted action: {adapted}")
    
    # Policy summary
    summary = learner.get_policy_summary('earthquake')
    print(f"Policy summary: {summary}")
    
    return learner


def demo_training_pipeline():
    """Demo: Complete training pipeline."""
    print("\n=== Training Pipeline Demo ===")
    
    # Initialize components
    action_space = ['evacuate', 'deploy_resources', 'infrastructure_repair', 'form_coalition', 'monitor']
    agent = RLAgent(action_space)
    experience_store = ExperienceStore()
    reward_model = RewardModel()
    policy_learner = AdaptivePolicyLearner()
    model_updater = ModelUpdater(update_frequency=50)
    
    pipeline = TrainingPipeline(
        agent, experience_store, reward_model, policy_learner, model_updater
    )
    
    # Create simple environment
    env_state = {'disaster_severity': 7.0, 'infrastructure_health': 100, 'casualties': 0, 'time_step': 0}
    
    def environment_step_fn(command, params):
        nonlocal env_state
        if command == 'reset':
            env_state = {'disaster_severity': 7.0, 'infrastructure_health': 100, 'casualties': 0, 'time_step': 0, 'resources_available': 5000}
            return env_state
        elif command == 'step':
            env_state['time_step'] += 1
            env_state['casualties'] = max(0, env_state.get('casualties', 0) - 5)
            env_state['infrastructure_health'] = min(100, env_state.get('infrastructure_health', 100) + 2)
            env_state['done'] = env_state['time_step'] >= 10
            return env_state
        return env_state
    
    # Train one episode
    result = pipeline.train_episode(environment_step_fn, max_steps=10)
    print(f"Episode result: {result}")
    
    # Training summary
    summary = pipeline.get_training_summary()
    print(f"Training summary: {summary}")
    
    return pipeline


def demo_simulation_trainer():
    """Demo: Simulation-based training."""
    print("\n=== Simulation Trainer Demo ===")
    
    trainer = SimulationTrainer()
    
    # Generate scenarios
    scenarios = trainer.generate_training_scenarios(num_scenarios=3)
    print(f"Generated {len(scenarios)} scenarios")
    for scenario in scenarios:
        print(f"  - {scenario['disaster_type']} (severity: {scenario['severity']:.1f})")
    
    # Create environment
    env = trainer.create_simulation_environment(
        'earthquake',
        7.5,
        {'population': 100000, 'initial_resources': 5000}
    )
    print(f"Created environment: {env['disaster_type']}")
    
    # Simulate step
    next_state = trainer.simulation_step(
        env,
        'evacuate',
        {'zones': ['zone_a'], 'resources': 500}
    )
    print(f"After evacuation - Casualties: {next_state['casualties']}, Resources: {next_state['resources_available']}")
    
    return trainer


def demo_checkpoint_manager():
    """Demo: Checkpoint saving and loading."""
    print("\n=== Checkpoint Manager Demo ===")
    
    manager = CheckpointManager(checkpoint_dir="demo_checkpoints")
    
    # Create dummy agent and store
    action_space = ['evacuate', 'deploy_resources']
    agent = RLAgent(action_space)
    experience_store = ExperienceStore()
    
    # Save checkpoint
    checkpoint_id = manager.save_checkpoint(
        agent,
        experience_store,
        metadata={'description': 'Demo checkpoint', 'version': '1.0'}
    )
    print(f"Saved checkpoint: {checkpoint_id}")
    
    # List checkpoints
    checkpoints = manager.list_checkpoints()
    print(f"Available checkpoints: {len(checkpoints)}")
    
    # Get latest
    latest = manager.get_latest_checkpoint()
    print(f"Latest checkpoint: {latest}")
    
    return manager


def demo_policy_evaluator():
    """Demo: Policy evaluation."""
    print("\n=== Policy Evaluator Demo ===")
    
    evaluator = PolicyEvaluator()
    
    # Create test scenarios
    test_scenarios = [
        {'disaster_type': 'earthquake', 'severity': 6.0, 'city_config': {}},
        {'disaster_type': 'flood', 'severity': 7.0, 'city_config': {}}
    ]
    
    # Create dummy components for evaluation
    action_space = ['evacuate', 'deploy_resources', 'monitor']
    agent = RLAgent(action_space)
    simulation_trainer = SimulationTrainer()
    
    # Evaluate (simplified)
    print("Evaluating policy on test scenarios...")
    # Note: Full evaluation requires trained agent
    
    # Set baseline
    evaluator.set_baseline({'overall_avg_reward': 50.0})
    print("Baseline set: 50.0")
    
    # Compare
    comparison = evaluator.compare_with_baseline({'overall_avg_reward': 65.0})
    print(f"Comparison: {comparison}")
    
    return evaluator


def run_all_demos():
    """Run all Batch 8 demos."""
    print("\n" + "="*60)
    print("BATCH 8 - LEARNING LAYER (RL) DEMONSTRATIONS")
    print("="*60)
    
    # Run individual demos
    store = demo_experience_store()
    model = demo_reward_model()
    agent = demo_rl_agent()
    learner = demo_adaptive_policy()
    pipeline = demo_training_pipeline()
    trainer = demo_simulation_trainer()
    manager = demo_checkpoint_manager()
    evaluator = demo_policy_evaluator()
    
    print("\n" + "="*60)
    print("BATCH 8 COMPLETE - AI LEARNS OPTIMAL DISASTER STRATEGIES")
    print("="*60)
    
    return {
        'experience_store': store,
        'reward_model': model,
        'agent': agent,
        'policy_learner': learner,
        'training_pipeline': pipeline,
        'simulation_trainer': trainer,
        'checkpoint_manager': manager,
        'policy_evaluator': evaluator
    }


if __name__ == "__main__":
    run_all_demos()
