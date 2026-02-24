"""
Demo scenarios for Batch 7 - Multi-Agent System

Demonstrates agent interactions, negotiations, coalitions, and rewards.
"""

from backend.core.multi_agent_system import (
    AgentManager,
    CitizenAgent,
    GovernmentAgent,
    InfrastructureAgent,
    EmergencyAgent,
    NegotiationEngine,
    CoalitionBuilder,
    RewardTracker,
    RewardType
)


def demo_basic_agents():
    """Demo: Create and manage different agent types"""
    print("\n=== DEMO: Basic Agent Creation ===")
    
    manager = AgentManager()
    
    # Create different agent types
    citizen = CitizenAgent("citizen_001", name="John Doe", family_size=3, location="downtown")
    government = GovernmentAgent("gov_001", name="City Government", budget=1000000)
    infrastructure = InfrastructureAgent("infra_001", name="Infrastructure Manager", managed_assets=["power_plant_1", "water_station_1"])
    emergency = EmergencyAgent("emer_001", name="Fire Unit Alpha", unit_type="fire")
    
    # Register agents
    manager.register_agent(citizen)
    manager.register_agent(government)
    manager.register_agent(infrastructure)
    manager.register_agent(emergency)
    
    print(f"Registered {len(manager.get_all_agents())} agents")
    
    # Show agent details
    for agent in manager.get_all_agents():
        print(f"  - {agent.agent_id} ({agent.agent_type.value}): {agent.state.value}")
    
    return manager


def demo_agent_communication():
    """Demo: Agents sending messages to each other"""
    print("\n=== DEMO: Agent Communication ===")
    
    manager = AgentManager()
    
    citizen = CitizenAgent("citizen_001", name="Jane Smith", family_size=2, location="suburb")
    emergency = EmergencyAgent("emer_001", name="Medical Unit 1", unit_type="medical")
    
    manager.register_agent(citizen)
    manager.register_agent(emergency)
    
    # Citizen requests help
    citizen.send_message(emergency, {
        "type": "help_request",
        "urgency": "high",
        "needs": ["medical_supplies", "evacuation"]
    })
    
    print(f"Citizen sent message to emergency responder")
    print(f"Emergency responder has {len(emergency.message_history)} messages")
    print(f"Latest message: {emergency.message_history[-1]}")
    
    # Emergency responds
    emergency.send_message(citizen, {
        "type": "help_response",
        "status": "en_route",
        "eta": "10 minutes"
    })
    
    print(f"Emergency responder replied")
    print(f"Citizen has {len(citizen.message_history)} messages")
    
    return manager


def demo_negotiation():
    """Demo: Agents negotiating resource allocation"""
    print("\n=== DEMO: Agent Negotiation ===")
    
    engine = NegotiationEngine()
    
    # Government proposes resource allocation to infrastructure manager
    proposal = engine.create_proposal(
        proposer_id="gov_001",
        recipient_id="infra_001",
        offer={
            "budget": 500000,
            "repair_crews": 10,
            "priority_assets": ["power_plant_1", "hospital_1"]
        }
    )
    
    print(f"Created proposal: {proposal.proposal_id}")
    print(f"  Proposer: {proposal.proposer_id}")
    print(f"  Recipient: {proposal.recipient_id}")
    print(f"  Offer: {proposal.offer}")
    
    # Infrastructure manager makes counter-offer
    counter = engine.counter_offer(
        proposal_id=proposal.proposal_id,
        counter_offer={
            "budget": 750000,  # Requesting more
            "repair_crews": 15,
            "priority_assets": ["power_plant_1", "hospital_1", "water_station_1"]
        }
    )
    
    print(f"\nCounter-offer made:")
    print(f"  Status: {counter.status.value}")
    print(f"  Counter-offer: {counter.counter_offer}")
    
    # Government accepts counter-offer
    result = engine.accept_proposal(proposal.proposal_id)
    
    print(f"\nNegotiation result: {result['outcome']}")
    print(f"  Completed at: {result['timestamp']}")
    
    return engine


def demo_coalition_formation():
    """Demo: Agents forming coalitions"""
    print("\n=== DEMO: Coalition Formation ===")
    
    builder = CoalitionBuilder()
    
    # Emergency responders form coalition
    coalition = builder.create_coalition(
        name="Emergency Response Team",
        leader_id="emer_001",
        goals=["rescue_citizens", "provide_medical_aid", "secure_area"]
    )
    
    print(f"Created coalition: {coalition.name}")
    print(f"  Leader: {coalition.leader_id}")
    print(f"  Goals: {coalition.goals}")
    
    # Add more members
    builder.add_member(coalition.coalition_id, "emer_002")
    builder.add_member(coalition.coalition_id, "emer_003")
    
    print(f"  Members: {len(coalition.members)}")
    
    # Members contribute resources
    builder.contribute_resources(
        coalition_id=coalition.coalition_id,
        agent_id="emer_001",
        resources={"medical_supplies": 100, "vehicles": 2}
    )
    
    builder.contribute_resources(
        coalition_id=coalition.coalition_id,
        agent_id="emer_002",
        resources={"medical_supplies": 50, "personnel": 5}
    )
    
    print(f"  Pooled resources: {coalition.resources}")
    
    # Activate coalition
    builder.activate_coalition(coalition.coalition_id)
    print(f"  Status: {coalition.status.value}")
    
    # Check coalition strength
    strength = builder.get_coalition_strength(coalition.coalition_id)
    print(f"  Strength metrics: {strength}")
    
    return builder


def demo_reward_system():
    """Demo: Tracking and distributing rewards"""
    print("\n=== DEMO: Reward System ===")
    
    tracker = RewardTracker()
    
    # Give individual rewards
    reward1 = tracker.give_reward(
        agent_id="emer_001",
        reward_type=RewardType.TASK_COMPLETION,
        amount=100.0,
        reason="Successfully rescued 5 citizens"
    )
    
    print(f"Reward given to emer_001:")
    print(f"  Type: {reward1.reward_type.value}")
    print(f"  Amount: {reward1.amount}")
    print(f"  Reason: {reward1.reason}")
    
    # Give more rewards
    tracker.give_reward("emer_001", RewardType.COOPERATION, 50.0, "Worked well with team")
    tracker.give_reward("emer_002", RewardType.TASK_COMPLETION, 80.0, "Provided medical aid")
    tracker.give_reward("infra_001", RewardType.EFFICIENCY, 120.0, "Rapid infrastructure repair")
    
    # Check agent statistics
    stats = tracker.get_reward_statistics("emer_001")
    print(f"\nAgent emer_001 statistics:")
    print(f"  Total rewards: {stats['total_rewards']}")
    print(f"  Total amount: {stats['total_amount']}")
    print(f"  Average: {stats['average_reward']}")
    print(f"  By type: {stats['by_type']}")
    
    # Distribute coalition reward
    coalition_members = ["emer_001", "emer_002", "emer_003"]
    rewards = tracker.distribute_coalition_reward(
        coalition_members=coalition_members,
        total_reward=300.0,
        distribution_strategy="equal"
    )
    
    print(f"\nDistributed coalition reward:")
    print(f"  Total: 300.0")
    print(f"  Strategy: equal")
    print(f"  Per member: {300.0 / len(coalition_members)}")
    
    # Show leaderboard
    leaderboard = tracker.get_top_performers(limit=5)
    print(f"\nTop performers:")
    for i, performer in enumerate(leaderboard, 1):
        print(f"  {i}. {performer['agent_id']}: {performer['total_reward']} points ({performer['reward_count']} rewards)")
    
    return tracker


def demo_complex_scenario():
    """Demo: Complex multi-agent disaster response scenario"""
    print("\n=== DEMO: Complex Disaster Response Scenario ===")
    
    # Initialize all systems
    manager = AgentManager()
    negotiation = NegotiationEngine()
    coalitions = CoalitionBuilder()
    rewards = RewardTracker()
    
    # Create agents
    print("\n1. Creating agents...")
    gov = GovernmentAgent("gov_001", name="City Government", budget=2000000)
    infra = InfrastructureAgent("infra_001", name="Infrastructure Manager", managed_assets=["power_plant_1", "hospital_1"])
    emer1 = EmergencyAgent("emer_001", name="Fire Unit Alpha", unit_type="fire")
    emer2 = EmergencyAgent("emer_002", name="Medical Unit 1", unit_type="medical")
    citizen1 = CitizenAgent("citizen_001", name="John Doe", family_size=3, location="downtown")
    citizen2 = CitizenAgent("citizen_002", name="Jane Smith", family_size=2, location="suburb")
    
    for agent in [gov, infra, emer1, emer2, citizen1, citizen2]:
        manager.register_agent(agent)
    
    print(f"   Registered {len(manager.get_all_agents())} agents")
    
    # Form emergency coalition
    print("\n2. Forming emergency response coalition...")
    coalition = coalitions.create_coalition(
        name="Disaster Response Team",
        leader_id="emer_001",
        goals=["rescue_operations", "medical_support", "infrastructure_protection"]
    )
    coalitions.add_member(coalition.coalition_id, "emer_002")
    coalitions.activate_coalition(coalition.coalition_id)
    print(f"   Coalition '{coalition.name}' formed with {len(coalition.members)} members")
    
    # Government negotiates with infrastructure
    print("\n3. Government negotiating with infrastructure manager...")
    proposal = negotiation.create_proposal(
        proposer_id="gov_001",
        recipient_id="infra_001",
        offer={
            "budget": 800000,
            "repair_priority": ["power_plant_1", "hospital_1"],
            "timeline": "48 hours"
        }
    )
    negotiation.accept_proposal(proposal.proposal_id)
    print(f"   Negotiation completed: {proposal.offer}")
    
    # Citizens request help
    print("\n4. Citizens requesting emergency assistance...")
    citizen1.send_message(emer1, {
        "type": "emergency",
        "situation": "trapped_in_building",
        "location": "downtown"
    })
    citizen2.send_message(emer2, {
        "type": "emergency",
        "situation": "medical_emergency",
        "location": "suburb"
    })
    print(f"   Emergency requests sent")
    
    # Distribute rewards for successful operations
    print("\n5. Distributing rewards...")
    rewards.give_reward("emer_001", RewardType.TASK_COMPLETION, 150.0, "Rescued citizen_001")
    rewards.give_reward("emer_002", RewardType.TASK_COMPLETION, 120.0, "Provided medical aid to citizen_002")
    rewards.give_reward("infra_001", RewardType.EFFICIENCY, 200.0, "Restored power plant in 36 hours")
    rewards.distribute_coalition_reward(
        coalition_members=["emer_001", "emer_002"],
        total_reward=200.0,
        distribution_strategy="equal"
    )
    print(f"   Rewards distributed")
    
    # Show final statistics
    print("\n6. Final Statistics:")
    print(f"   Active agents: {len(manager.get_all_agents())}")
    print(f"   Active coalitions: {len(coalitions.get_active_coalitions())}")
    print(f"   Completed negotiations: {len(negotiation.completed_negotiations)}")
    print(f"   Total rewards given: {len(rewards.get_all_rewards())}")
    
    leaderboard = rewards.get_top_performers(limit=3)
    print(f"\n   Top performers:")
    for i, performer in enumerate(leaderboard, 1):
        print(f"     {i}. {performer['agent_id']}: {performer['total_reward']} points")
    
    print("\n✅ Complex scenario completed successfully!")
    
    return {
        "manager": manager,
        "negotiation": negotiation,
        "coalitions": coalitions,
        "rewards": rewards
    }


if __name__ == "__main__":
    print("=" * 60)
    print("BATCH 7 - MULTI-AGENT SYSTEM DEMOS")
    print("=" * 60)
    
    # Run all demos
    demo_basic_agents()
    demo_agent_communication()
    demo_negotiation()
    demo_coalition_formation()
    demo_reward_system()
    demo_complex_scenario()
    
    print("\n" + "=" * 60)
    print("ALL DEMOS COMPLETED!")
    print("=" * 60)
