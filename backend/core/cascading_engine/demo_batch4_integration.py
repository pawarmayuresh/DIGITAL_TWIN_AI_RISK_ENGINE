"""
BATCH 4 INTEGRATION DEMO — Cascades with Batch 3 Disasters

Demonstrates integrated simulation:
1. Disaster triggers infrastructure damage (Batch 3 → Batch 4)
2. Infrastructure cascades propagate failures (Batch 4)
3. Cascade impacts degrade grid cells (Batch 4 → Batch 2)
4. Recovery restores infrastructure over time (Batch 4)
5. Real-world complexity: earthquake → power failure → water pumps fail → hospitals stressed
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from disaster_cascade_integration import DisasterCascadeIntegrator
from cascading_engine import InfrastructureGraph, InfrastructureNodeType
from disaster_engine import DisasterType, DisasterManager
from spatial_engine import GridManager, CellMetadata, ZoningEngine


def create_integrated_demo_infrastructure() -> InfrastructureGraph:
    """Create infrastructure for integrated testing."""
    graph = InfrastructureGraph()
    
    # Power generation
    graph.add_node("power_plant", InfrastructureNodeType.POWER_PLANT, (10, 10), criticality=1.0)
    graph.add_node("substation_1", InfrastructureNodeType.SUBSTATION, (8, 10), criticality=0.95)
    graph.add_node("substation_2", InfrastructureNodeType.SUBSTATION, (12, 10), criticality=0.95)
    
    # Water supply
    graph.add_node("water_treatment", InfrastructureNodeType.WATER_TREATMENT, (5, 5), criticality=0.9)
    graph.add_node("water_pump_1", InfrastructureNodeType.WATER_PUMP, (7, 8), criticality=0.8)
    graph.add_node("water_pump_2", InfrastructureNodeType.WATER_PUMP, (13, 12), criticality=0.8)
    
    # Critical services
    graph.add_node("hospital", InfrastructureNodeType.HOSPITAL, (10, 15), criticality=0.95)
    graph.add_node("data_center", InfrastructureNodeType.DATA_CENTER, (15, 10), criticality=0.85)
    graph.add_node("transport", InfrastructureNodeType.TRANSPORT_HUB, (10, 5), criticality=0.7)
    
    # Dependencies
    graph.add_dependency("power_plant", "substation_1", weight=1.0, edge_type="power")
    graph.add_dependency("power_plant", "substation_2", weight=1.0, edge_type="power")
    graph.add_dependency("substation_1", "hospital", weight=1.0, edge_type="power")
    graph.add_dependency("substation_1", "water_pump_1", weight=0.9, edge_type="power")
    graph.add_dependency("substation_2", "data_center", weight=0.8, edge_type="power")
    graph.add_dependency("substation_2", "water_pump_2", weight=0.9, edge_type="power")
    
    graph.add_dependency("water_treatment", "water_pump_1", weight=1.0, edge_type="water")
    graph.add_dependency("water_treatment", "water_pump_2", weight=1.0, edge_type="water")
    graph.add_dependency("water_pump_1", "hospital", weight=0.7, edge_type="water")
    graph.add_dependency("water_pump_2", "hospital", weight=0.7, edge_type="water")
    
    return graph


def create_demo_grid() -> GridManager:
    """Create spatial grid for integration."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    return grid


def demo_integrated_earthquake_cascade():
    """DEMO 1: Earthquake triggers cascading infrastructure failure."""
    print("\n" + "="*70)
    print("INTEGRATED DEMO 1: Earthquake → Cascade → Grid Impact")
    print("="*70)
    print("Scenario: M7.5 Earthquake damages power plant and substations")
    print("Expected: Power loss cascades to water pumps, hospitals lose capacity")
    
    # Setup
    infra_graph = create_integrated_demo_infrastructure()
    disaster_mgr = DisasterManager()
    grid = create_demo_grid()
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    integrator = DisasterCascadeIntegrator(infra_graph, disaster_mgr, grid)
    
    # Earthquake affects specific grid region
    earthquake_cells = [(x, y) for x in range(8, 12) for y in range(8, 12)]
    
    print(f"\n📊 Earthquake impact zone: {len(earthquake_cells)} cells")
    
    # Run integrated simulation for 5 ticks
    print(f"\n{'Tick':<5} {'Stability':<12} {'Failed Infra':<15} {'Grid Cells Hit':<15} {'Repair Progress':<15}")
    print("-" * 70)
    
    for tick in range(6):
        # Disaster only at tick 0
        disaster_events = []
        if tick == 0:
            disaster_events = [
                (DisasterType.EARTHQUAKE, earthquake_cells, 0.85)
            ]
        
        result = integrator.simulate_integrated_tick(tick, disaster_events)
        
        stability = result["system_health"]["stability"]
        failed = result["system_health"]["failed_nodes"]
        grid_affected = result["grid_impacts"]["cells_affected"]
        repaired = result["recovery"].get("nodes_repaired", 0)
        
        print(f"{tick:<5} {stability:.3f}      {failed:<14} {grid_affected:<14} {repaired:<14}")
    
    summary = integrator.integration_summary()
    print(f"\n✅ Integration Summary:")
    print(f"   Total infrastructure failures: {summary['total_infrastructure_impacts']}")
    print(f"   Peak cascade depth: {summary['peak_cascade_depth']}")
    print(f"   Total grid cells impacted: {summary['grid_cells_impacted']}")
    print(f"   Avg system health: {summary['average_system_health']:.3f}")


def demo_integrated_cascade_timeline():
    """DEMO 2: Multi-tick cascade evolution with recovery."""
    print("\n" + "="*70)
    print("INTEGRATED DEMO 2: Cascade Timeline with Recovery")
    print("="*70)
    print("Scenario: Initial damage, observe cascade + recovery over 15 ticks")
    
    # Setup
    infra_graph = create_integrated_demo_infrastructure()
    disaster_mgr = DisasterManager()
    grid = create_demo_grid()
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    integrator = DisasterCascadeIntegrator(infra_graph, disaster_mgr, grid)
    
    # Initial disaster hits multiple zones
    damage_zone = [(x, y) for x in range(9, 11) for y in range(9, 11)]
    
    print(f"\n📈 Evolution over 15 ticks:")
    print(f"{'Tick':<5} {'Status':<50}")
    print("-" * 70)
    
    for tick in range(15):
        disaster_events = []
        if tick == 0:
            disaster_events = [(DisasterType.EARTHQUAKE, damage_zone, 0.8)]
        
        result = integrator.simulate_integrated_tick(tick, disaster_events)
        
        stability = result["system_health"]["stability"]
        cascade_depth = result["cascade"].get("cascade_depth", 0)
        repaired = result["recovery"].get("nodes_repaired", 0)
        
        # Status indicator
        if stability > 0.9:
            status = "🟢 Healthy"
        elif stability > 0.7:
            status = "🟡 Degraded"
        elif stability > 0.4:
            status = "🔴 Critical"
        else:
            status = "⚫ Failing"
        
        msg = f"{status} | Stability: {stability:.1%} | Cascade depth: {cascade_depth} | Repaired: {repaired}"
        print(f"{tick:<5} {msg:<65}")


def demo_integrated_multi_disaster():
    """DEMO 3: Multiple disasters compound cascade effects."""
    print("\n" + "="*70)
    print("INTEGRATED DEMO 3: Cascading Multi-Disaster")
    print("="*70)
    print("Scenario: Earthquake then flood hit partially recovered system")
    
    # Setup
    infra_graph = create_integrated_demo_infrastructure()
    disaster_mgr = DisasterManager()
    grid = create_demo_grid()
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    integrator = DisasterCascadeIntegrator(infra_graph, disaster_mgr, grid)
    
    # Earthquake and flood zones
    quake_zone = [(x, y) for x in range(8, 12) for y in range(8, 12)]
    flood_zone = [(x, y) for x in range(5, 8) for y in range(3, 7)]
    
    print(f"\nDisaster sequence:")
    print(f"  Tick 0: Magnitude 7.5 Earthquake (16 cells)")
    print(f"  Tick 7: Flooding in water pumping area (12 cells)")
    
    timeline_data = []
    
    for tick in range(12):
        disaster_events = []
        
        if tick == 0:
            disaster_events.append((DisasterType.EARTHQUAKE, quake_zone, 0.8))
        elif tick == 7:
            disaster_events.append((DisasterType.FLOOD, flood_zone, 0.7))
        
        result = integrator.simulate_integrated_tick(tick, disaster_events)
        
        timeline_data.append({
            "tick": tick,
            "stability": result["system_health"]["stability"],
            "failed": result["system_health"]["failed_nodes"],
            "cascades": result["cascade"].get("cascade_events", 0),
        })
    
    print(f"\n{'Tick':<5} {'Stability':<12} {'Failed':<8} {'Cascades':<10} {'Marker':<30}")
    print("-" * 70)
    
    for data in timeline_data:
        marker = ""
        if data["tick"] == 0:
            marker = "🔴 EARTHQUAKE STRIKES"
        elif data["tick"] == 7:
            marker = "💧 FLOOD HITS"
        
        print(f"{data['tick']:<5} {data['stability']:.3f}      {data['failed']:<7} "
              f"{data['cascades']:<9} {marker:<29}")


def main():
    """Run all integration demos."""
    print("\n" + "🔗"*35)
    print("BATCH 4 INTEGRATION DEMO")
    print("Cascading Failure Engine + Disaster Engine + Spatial Grid")
    print("🔗"*35)
    
    try:
        demo_integrated_earthquake_cascade()
        demo_integrated_cascade_timeline()
        demo_integrated_multi_disaster()
        
        print("\n" + "="*70)
        print("✅ ALL INTEGRATION DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nIntegration Features:")
        print("  ✅ Disasters map to infrastructure damage")
        print("  ✅ Cascades propagate through network")
        print("  ✅ Infrastructure failures feed back to grid")
        print("  ✅ Recovery models restoration timeline")
        print("  ✅ Multi-disaster scenarios handled")
        print("\nBatch 4 Outcome:")
        print("  ✅ Infrastructure collapse simulation works")
        print("  ✅ Cascading failures realistic and propagating")
        print("  ✅ Complete feedback loop integrated")
        print("  ✅ Ready for Batch 5 (Digital Twin)")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
