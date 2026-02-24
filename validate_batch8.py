#!/usr/bin/env python3
"""
Batch 8 Validation Script - Learning Layer (RL)
Validates all RL components are working correctly.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from core.learning_layer import (
    ExperienceStore,
    RewardModel,
    RLAgent,
    AdaptivePolicyLearner,
    ModelUpdater,
    TrainingPipeline,
    CheckpointManager,
    SimulationTrainer,
    PolicyEvaluator
)


def validate_experience_store():
    """Validate experience store functionality."""
    print("✓ Testing Experience Store...")
    
    store = ExperienceStore(max_size=100)
    
    # Test episode management
    episode_id = store.start_episode()
    assert episode_id is not None, "Failed to start episode"
    
    # Test experience addition
    store.add_experience(
        state={'time': 0},
        action={'type': 'test'},
        reward=10.0,
        next_state={'time': 1},
        done=False
    )
    assert len(store.experiences) == 1, "Failed to add experience"
    
    # Test batch sampling
    batch = store.sample_batch(1)
    assert len(batch) == 1, "Failed to sample batch"
    
    # Test statistics
    stats = store.get_statistics()
    assert stats['total_experiences'] == 1, "Incorrect statistics"
    
    print("  ✓ Experience store validated")
    return True


def validate_reward_model():
    """Validate reward model functionality."""
    print("✓ Testing Reward Model...")
    
    model = RewardModel()
    
    state_before = {
        'casualties': 100,
        'infrastructure_health': 80,
        'economic_loss': 1000000
    }
    
    action = {'type': 'evacuate', 'resources': 500}
    
    state_after = {
        'casualties': 70,
        'infrastructure_health': 85,
        'economic_loss': 1200000
    }
    
    reward_info = model.calculate_reward(state_before, action, state_after)
    
    assert 'total_reward' in reward_info, "Missing total reward"
    assert 'components' in reward_info, "Missing reward components"
    assert isinstance(reward_info['total_reward'], (int, float)), "Invalid reward type"
    
    print("  ✓ Reward model validated")
    return True


def validate_rl_agent():
    """Validate RL agent functionality."""
    print("✓ Testing RL Agent...")
    
    action_space = ['evacuate', 'deploy_resources', 'monitor']
    agent = RLAgent(action_space, learning_rate=0.1)
    
    state = {
        'disaster_severity': 7.0,
        'infrastructure_health': 80,
        'resources_available': 3000,
        'casualties': 50,
        'time_step': 5
    }
    
    # Test action selection
    action_type, action_params = agent.select_action(state, explore=True)
    assert action_type in action_space, "Invalid action selected"
    assert isinstance(action_params, dict), "Invalid action params"
    
    # Test update
    next_state = state.copy()
    next_state['time_step'] = 6
    agent.update(state, action_type, 10.0, next_state, False)
    
    # Test statistics
    stats = agent.get_statistics()
    assert stats['training_steps'] == 1, "Incorrect training steps"
    
    print("  ✓ RL agent validated")
    return True


def validate_adaptive_policy():
    """Validate adaptive policy learner."""
    print("✓ Testing Adaptive Policy Learner...")
    
    learner = AdaptivePolicyLearner()
    
    episode_data = [
        {
            'state': {'disaster_severity': 6.0},
            'action': {'action_type': 'evacuate'},
            'reward': 10.0
        }
    ]
    
    learner.learn_from_episode(episode_data, 10.0, 'earthquake')
    
    summary = learner.get_policy_summary('earthquake')
    assert summary['learned'] == True, "Policy not learned"
    
    print("  ✓ Adaptive policy learner validated")
    return True


def validate_model_updater():
    """Validate model updater."""
    print("✓ Testing Model Updater...")
    
    updater = ModelUpdater(update_frequency=10)
    
    # Test should_update
    should_update = updater.should_update(10)
    assert should_update == True, "Should update at frequency"
    
    # Test queue update
    updater.queue_update('learning_rate', {'new_value': 0.05})
    assert len(updater.pending_updates) == 1, "Failed to queue update"
    
    # Test statistics
    stats = updater.get_update_statistics()
    assert 'pending_updates' in stats, "Missing statistics"
    
    print("  ✓ Model updater validated")
    return True


def validate_training_pipeline():
    """Validate training pipeline."""
    print("✓ Testing Training Pipeline...")
    
    action_space = ['evacuate', 'monitor']
    agent = RLAgent(action_space)
    experience_store = ExperienceStore()
    reward_model = RewardModel()
    policy_learner = AdaptivePolicyLearner()
    model_updater = ModelUpdater()
    
    pipeline = TrainingPipeline(
        agent, experience_store, reward_model, policy_learner, model_updater
    )
    
    # Test environment function
    env_state = {'time': 0, 'done': False}
    
    def env_fn(cmd, params):
        nonlocal env_state
        if cmd == 'reset':
            env_state = {'time': 0, 'done': False, 'disaster_severity': 5.0, 'infrastructure_health': 100, 'casualties': 0, 'resources_available': 5000}
            return env_state
        elif cmd == 'step':
            env_state['time'] += 1
            env_state['done'] = env_state['time'] >= 5
            return env_state
        return env_state
    
    # Train one episode
    result = pipeline.train_episode(env_fn, max_steps=5)
    assert 'episode_id' in result, "Missing episode ID"
    assert 'total_reward' in result, "Missing total reward"
    
    print("  ✓ Training pipeline validated")
    return True


def validate_simulation_trainer():
    """Validate simulation trainer."""
    print("✓ Testing Simulation Trainer...")
    
    trainer = SimulationTrainer()
    
    # Test scenario generation
    scenarios = trainer.generate_training_scenarios(3)
    assert len(scenarios) == 3, "Failed to generate scenarios"
    
    # Test environment creation
    env = trainer.create_simulation_environment(
        'earthquake', 7.0, {'population': 100000}
    )
    assert env['disaster_type'] == 'earthquake', "Invalid environment"
    
    # Test simulation step
    next_state = trainer.simulation_step(env, 'evacuate', {'zones': ['a']})
    assert 'time_step' in next_state, "Invalid next state"
    
    print("  ✓ Simulation trainer validated")
    return True


def validate_checkpoint_manager():
    """Validate checkpoint manager."""
    print("✓ Testing Checkpoint Manager...")
    
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        manager = CheckpointManager(checkpoint_dir=temp_dir)
        
        # Create dummy components
        agent = RLAgent(['evacuate', 'monitor'])
        experience_store = ExperienceStore()
        
        # Test save
        checkpoint_id = manager.save_checkpoint(agent, experience_store)
        assert checkpoint_id is not None, "Failed to save checkpoint"
        
        # Test list
        checkpoints = manager.list_checkpoints()
        assert len(checkpoints) >= 1, "Failed to list checkpoints"
        
        # Test load
        success = manager.load_checkpoint(checkpoint_id, agent, experience_store)
        assert success == True, "Failed to load checkpoint"
        
        print("  ✓ Checkpoint manager validated")
        return True
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def validate_policy_evaluator():
    """Validate policy evaluator."""
    print("✓ Testing Policy Evaluator...")
    
    evaluator = PolicyEvaluator()
    
    # Test baseline setting
    evaluator.set_baseline({'overall_avg_reward': 50.0})
    
    # Test comparison
    comparison = evaluator.compare_with_baseline({'overall_avg_reward': 60.0})
    assert 'improvement_percent' in comparison, "Missing improvement metric"
    assert comparison['is_better'] == True, "Incorrect comparison"
    
    print("  ✓ Policy evaluator validated")
    return True


def run_all_validations():
    """Run all validation tests."""
    print("\n" + "="*60)
    print("BATCH 8 VALIDATION - LEARNING LAYER (RL)")
    print("="*60 + "\n")
    
    tests = [
        ("Experience Store", validate_experience_store),
        ("Reward Model", validate_reward_model),
        ("RL Agent", validate_rl_agent),
        ("Adaptive Policy", validate_adaptive_policy),
        ("Model Updater", validate_model_updater),
        ("Training Pipeline", validate_training_pipeline),
        ("Simulation Trainer", validate_simulation_trainer),
        ("Checkpoint Manager", validate_checkpoint_manager),
        ("Policy Evaluator", validate_policy_evaluator)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ {test_name} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"VALIDATION COMPLETE: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_validations()
    sys.exit(0 if success else 1)
