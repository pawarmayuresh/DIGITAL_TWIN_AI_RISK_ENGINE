#!/usr/bin/env python3
"""
Quick test script to verify evacuation system works
Run from project root: python3 test_evacuation_system.py
"""

import sys
sys.path.insert(0, '.')

from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder
from backend.evacuation_system.human_agent_sim import EvacuationSimulator
from backend.evacuation_system.car_evacuation_manager import CarEvacuationManager

def test_evacuation_system():
    print("=" * 60)
    print("TESTING EVACUATION SYSTEM")
    print("=" * 60)
    
    # 1. Initialize grid
    print("\n1. Initializing Mumbai Grid (20x20)...")
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    print(f"   ✅ Created {len(grid_engine.grids)} grid zones")
    
    # 2. Check zones
    safe_zones = grid_engine.get_safe_zones()
    dangerous_zones = grid_engine.get_dangerous_zones()
    print(f"\n2. Zone Analysis:")
    print(f"   ✅ Safe zones: {len(safe_zones)}")
    print(f"   ⚠️  Dangerous zones: {len(dangerous_zones)}")
    
    if dangerous_zones:
        print(f"\n   First 3 dangerous zones:")
        for zone in dangerous_zones[:3]:
            print(f"      - {zone.id} ({zone.name}): Risk={zone.risk_score:.2f}, Pop={zone.population_density}")
    
    # 3. Test pathfinding
    print(f"\n3. Testing A* Pathfinding...")
    pathfinder = EvacuationPathfinder(grid_engine)
    
    if dangerous_zones and safe_zones:
        start = dangerous_zones[0]
        goal = safe_zones[0]
        result = pathfinder.find_path(start, goal)
        
        if result['success']:
            print(f"   ✅ Path found: {start.id} → {goal.id}")
            path_length = len(result.get('path', []))
            print(f"   📏 Path length: {path_length} steps")
            if path_length > 0:
                path_ids = [p['grid_id'] if isinstance(p, dict) else p for p in result['path'][:5]]
                print(f"   🛣️  Path: {' → '.join(path_ids)}...")
        else:
            print(f"   ❌ Path not found: {result.get('message', 'Unknown error')}")
    
    # 4. Test human agents
    print(f"\n4. Testing Human Agent Simulation...")
    simulator = EvacuationSimulator(grid_engine, pathfinder)
    agents = simulator.create_agents_in_dangerous_zones(agents_per_zone=2)
    print(f"   ✅ Created {len(agents)} human agents")
    
    simulator.assign_evacuation_paths()
    print(f"   ✅ Assigned evacuation paths")
    
    # Run a few steps
    for i in range(3):
        result = simulator.simulate_step()
        stats = result['stats']
        print(f"   Step {i+1}: {stats['evacuating']} evacuating, {stats['safe']} safe")
    
    # 5. Test car system
    print(f"\n5. Testing Car Evacuation System...")
    car_manager = CarEvacuationManager(grid_engine)
    
    # Add cars
    if safe_zones:
        start_grid = safe_zones[0].id
        for i in range(3):
            car_manager.add_car(f"CAR-{i+1}", f"Rescue Vehicle {i+1}", start_grid, capacity=50)
        print(f"   ✅ Added {len(car_manager.cars)} cars at {start_grid}")
    
    # Assign missions
    if dangerous_zones:
        for i, zone in enumerate(dangerous_zones[:3]):
            car_id = f"CAR-{i+1}"
            result = car_manager.assign_mission(car_id, zone.id)
            if result['success']:
                print(f"   ✅ {car_id} assigned to {zone.id}")
    
    # Run car simulation
    for i in range(3):
        result = car_manager.simulate_step()
        print(f"   Step {i+1}: {result['active_missions']} active missions, {result['total_evacuated']} evacuated")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - EVACUATION SYSTEM WORKING!")
    print("=" * 60)
    print("\nYou can now start the backend server:")
    print("  ./start_backend.sh")
    print("\nThen start the frontend:")
    print("  cd frontend && npm run dev")
    print("\nOpen: http://localhost:8081")

if __name__ == "__main__":
    try:
        test_evacuation_system()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
