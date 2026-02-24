"""
Batch 3 Demo — Multi-disaster scenario with cascade effects.

Demonstrates:
- All 5 disaster types (flood, earthquake, wildfire, pandemic, cyber)
- Cascading failures (e.g., earthquake triggers fires)
- Multi-infrastructure damage tracking
- Aggregated impact calculation
- Intervention priority identification
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from core.spatial_engine import (
    GridManager,
    ZoningEngine,
    SpatialRiskCalculator,
    GridVisualExporter,
)
from core.disaster_engine import (
    DisasterEvent,
    DisasterType,
    DisasterManager,
    SpatialImpactCalculator,
    DisasterConfigLoader,
)


def demo_scenario_1_single_flood():
    """Demo 1: Single flood event and impacts."""
    print("\n" + "=" * 80)
    print("DEMO 1: Single Flood Event")
    print("=" * 80)
    
    # Create grid
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    from core.spatial_engine import CellMetadata
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    print(f"✓ Created {len(list(grid.get_all_cells()))} grid cells (20x20)")
    
    # Add zones
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    print(f"✓ Assigned zones to all cells")
    
    # Create disaster manager
    dm = DisasterManager()
    
    # Create flood event
    flood = DisasterEvent(
        event_id="flood-1",
        disaster_type=DisasterType.FLOOD,
        severity=0.7,
        epicenter=(10, 10),
        radius_km=5.0,
        onset_time=0,
    )
    flood_model = dm._create_disaster(flood)
    dm.add_disaster(flood_model)
    print(f"✓ Added flood disaster: severity={flood.severity}")
    
    # Run simulation
    spatial_calc = SpatialImpactCalculator(dm)
    print("\nSimulation Ticks:")
    for tick in range(15):
        dm.propagate_all(grid, None)
        impact_report = spatial_calc.apply_impacts(grid)
        
        if tick % 3 == 0 or tick < 3:
            print(
                f"  Tick {tick:2d}: "
                f"{impact_report['total_cells_affected']:3d} cells affected, "
                f"{impact_report['population_affected']:6d} people at risk, "
                f"Active disasters: {dm.get_active_disaster_count()}"
            )
    
    # Final report
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    
    print("\nFinal Impact Report:")
    print(f"  Total affected cells: {final_report['total_cells_affected']}")
    print(f"  Population affected: {int(final_report['population_affected'])}")
    infrastructure_failures = ", ".join(
        f"{k}:{v}" for k, v in final_report["infrastructure_failures"].items()
    )
    print(f"  Infrastructure failures: {infrastructure_failures}")
    print(f"  Critical zones: {len(final_report['critical_zones'])}")
    
    print("\nInfrastructure Status:")
    for infra, health in infra_status.items():
        health_pct = health * 100
        status_bar = "█" * int(health_pct / 5) + "░" * (20 - int(health_pct / 5))
        print(f"  {infra:15s}: {status_bar} {health_pct:5.1f}%")


def demo_scenario_2_earthquake_cascade():
    """Demo 2: Earthquake triggering fires (cascade)."""
    print("\n" + "=" * 80)
    print("DEMO 2: Earthquake with Cascade to Wildfire")
    print("=" * 80)
    
    # Create grid
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    from core.spatial_engine import CellMetadata
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    print(f"✓ Created {len(list(grid.get_all_cells()))} grid cells (20x20)")
    
    # Add zones
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    print(f"✓ Assigned zones to all cells")
    
    # Create disaster manager
    dm = DisasterManager()
    
    # Create earthquake
    earthquake = DisasterEvent(
        event_id="earthquake-1",
        disaster_type=DisasterType.EARTHQUAKE,
        severity=0.8,
        epicenter=(10, 10),
        radius_km=6.0,
        onset_time=0,
    )
    eq_model = dm._create_disaster(earthquake)
    dm.add_disaster(eq_model)
    print(f"✓ Added earthquake: severity={earthquake.severity}")
    
    # Run simulation with cascade checking
    spatial_calc = SpatialImpactCalculator(dm)
    print("\nSimulation Ticks:")
    for tick in range(20):
        dm.propagate_all(grid, None)
        
        # Check for cascades
        for disaster in list(dm.active_disasters.values()):
            dm.trigger_cascades(grid, disaster)
        
        impact_report = spatial_calc.apply_impacts(grid)
        
        active_by_type = dm.get_active_disasters_by_type()
        disaster_types = " + ".join(f"{k}({v})" for k, v in active_by_type.items())
        
        if tick % 3 == 0 or tick < 5:
            print(
                f"  Tick {tick:2d}: "
                f"{impact_report['total_cells_affected']:3d} cells affected, "
                f"Disasters: {disaster_types}"
            )
    
    # Final report
    final_report = spatial_calc.apply_impacts(grid)
    
    print("\nFinal Status:")
    print(f"  Total affected cells: {final_report['total_cells_affected']}")
    print(f"  Population affected: {final_report['population_affected']}")
    print(f"  Active disasters: {dm.get_active_disaster_count()}")
    
    final_summary = dm.get_summary()
    print(f"  Disaster types triggered: {final_summary['by_type']}")


def demo_scenario_3_pandemic_spread():
    """Demo 3: Pandemic spread across population."""
    print("\n" + "=" * 80)
    print("DEMO 3: Pandemic Wave")
    print("=" * 80)
    
    # Create grid
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    from core.spatial_engine import CellMetadata
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=150.0)
            grid.create_cell(x, y, metadata)
    print(f"✓ Created {len(list(grid.get_all_cells()))} grid cells (20x20)")
    
    # Add zones (high population density in urban areas)
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    print(f"✓ Assigned zones with elevated populations")
    total_pop = sum(c.metadata.population_density for c in grid.get_all_cells())
    print(f"  Total grid population: {total_pop}")
    print(f"  Total grid population: {total_pop}")
    
    # Create disaster manager
    dm = DisasterManager()
    
    # Create pandemic
    pandemic = DisasterEvent(
        event_id="pandemic-1",
        disaster_type=DisasterType.PANDEMIC,
        severity=0.6,
        epicenter=(10, 10),
        radius_km=8.0,
        onset_time=0,
    )
    pandemic_model = dm._create_disaster(pandemic)
    dm.add_disaster(pandemic_model)
    print(f"✓ Added pandemic: severity={pandemic.severity}")
    
    # Run simulation
    spatial_calc = SpatialImpactCalculator(dm)
    print("\nSimulation Ticks:")
    for tick in range(25):
        dm.propagate_all(grid, None)
        impact_report = spatial_calc.apply_impacts(grid)
        vuln = spatial_calc.get_population_vulnerability(grid)
        
        if tick % 4 == 0 or tick < 5:
            print(
                f"  Tick {tick:2d}: "
                f"{int(impact_report['population_affected']):6d} at risk, "
                f"Vulnerability: {vuln['vulnerability_index']:.2f}, "
                f"Active: {dm.get_active_disaster_count()}"
            )
    
    # Final report
    vuln = spatial_calc.get_population_vulnerability(grid)
    priorities = spatial_calc.identify_intervention_priorities(grid)
    
    print("\nFinal Status:")
    print(f"  Total population: {vuln['total_population']}")
    print(f"  At-risk population: {vuln['at_risk_population']}")
    print(f"  Vulnerability index: {vuln['vulnerability_index']:.3f}")
    print(f"  Intervention priorities identified: {len(priorities)}")


def demo_scenario_4_multi_disaster():
    """Demo 4: Multi-disaster scenario with multiple sequential/simultaneous events."""
    print("\n" + "=" * 80)
    print("DEMO 4: Multi-Disaster Scenario (Earthquake + Flood + Fire + Cyber)")
    print("=" * 80)
    
    # Create grid
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    from core.spatial_engine import CellMetadata
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    print(f"✓ Created {len(list(grid.get_all_cells()))} grid cells (20x20)")
    
    # Add zones
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    print(f"✓ Assigned zones to all cells")
    
    # Create disaster manager
    dm = DisasterManager()
    
    # Load preset multi-disaster scenario
    scenario = DisasterConfigLoader.get_preset_scenario("multi_disaster")
    print(f"✓ Loaded scenario: {scenario['name']}")
    print(f"  Description: {scenario['description']}")
    
    # Instantiate scenario
    events = DisasterConfigLoader.load_scenario(scenario)
    for event in events:
        disaster = dm._create_disaster(event)
        if disaster:
            dm.add_disaster(disaster)
            print(
                f"  - {event.disaster_type.value} "
                f"(severity={event.severity}, tick={event.onset_time})"
            )
    
    # Run simulation
    spatial_calc = SpatialImpactCalculator(dm)
    print("\nSimulation Ticks:")
    for tick in range(30):
        # Check for new disasters to start
        for event in events:
            if event.onset_time == tick:
                disaster = dm._create_disaster(event)
                if disaster and f"{event.disaster_type.value}_{tick}" not in dm.active_disasters:
                    dm.add_disaster(disaster)
                    print(f"  Tick {tick}: NEW {event.disaster_type.value} disaster!")
        
        dm.propagate_all(grid, None)
        
        # Check cascades
        for disaster in list(dm.active_disasters.values()):
            dm.trigger_cascades(grid, disaster)
        
        impact_report = spatial_calc.apply_impacts(grid)
        active_by_type = dm.get_active_disasters_by_type()
        disaster_types = " + ".join(f"{k}({v})" for k, v in active_by_type.items())
        
        if tick % 5 == 0 or tick < 3:
            print(
                f"  Tick {tick:2d}: "
                f"{impact_report['total_cells_affected']:3d} affected cells, "
                f"Disasters: {disaster_types}"
            )
    
    # Final report with all metrics
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    vuln = spatial_calc.get_population_vulnerability(grid)
    priorities = spatial_calc.identify_intervention_priorities(grid)
    
    print("\nFinal Impact Summary:")
    print(f"  Affected cells: {final_report['total_cells_affected']}")
    print(f"  Population at risk: {final_report['population_affected']}")
    print(f"  Critical zones: {len(final_report['critical_zones'])}")
    print(f"  Intervention priorities: {len(priorities)}")
    
    print("\nInfrastructure Status (% Operational):")
    for infra, health in infra_status.items():
        health_pct = health * 100
        if health_pct >= 80:
            status = "✓ Good"
        elif health_pct >= 50:
            status = "⚠ Degraded"
        else:
            status = "✗ Critical"
        print(f"  {infra:15s}: {health_pct:5.1f}% {status}")
    
    print("\nPopulation Vulnerability:")
    print(f"  Total population: {vuln['total_population']}")
    print(f"  At-risk population: {vuln['at_risk_population']}")
    print(f"  Vulnerability index: {vuln['vulnerability_index']:.3f}")


def demo_scenario_5_cyber_cascade():
    """Demo 5: Cyber attack triggering infrastructure cascade."""
    print("\n" + "=" * 80)
    print("DEMO 5: Cyber Attack with Infrastructure Cascade")
    print("=" * 80)
    
    # Create grid
    grid = GridManager(width=15, height=15, cell_size=1.0)
    
    # Create cells
    from core.spatial_engine import CellMetadata
    for x in range(15):
        for y in range(15):
            metadata = CellMetadata(x=x, y=y, population_density=120.0)
            grid.create_cell(x, y, metadata)
    print(f"✓ Created {len(list(grid.get_all_cells()))} grid cells (15x15)")
    
    # Add zones
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()  # Mostly urban (networked)
    print(f"✓ Assigned zones with high network connectivity")
    
    # Create disaster manager
    dm = DisasterManager()
    
    # Create cyber attack
    cyber = DisasterEvent(
        event_id="cyber-1",
        disaster_type=DisasterType.CYBER_ATTACK,
        severity=0.75,
        epicenter=(7, 7),
        radius_km=4.0,
        onset_time=0,
    )
    cyber_model = dm._create_disaster(cyber)
    dm.add_disaster(cyber_model)
    print(f"✓ Added cyber attack: severity={cyber.severity}")
    
    # Run simulation
    spatial_calc = SpatialImpactCalculator(dm)
    print("\nSimulation Ticks (showing cascade effects):")
    for tick in range(20):
        dm.propagate_all(grid, None)
        impact_report = spatial_calc.apply_impacts(grid)
        
        if impact_report["infrastructure_failures"]:
            failures_str = ", ".join(
                f"{k}:{v}" for k, v in impact_report["infrastructure_failures"].items()
            )
            print(f"  Tick {tick:2d}: {impact_report['total_cells_affected']:3d} cells, Failures: {failures_str}")
    
    # Final status
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    
    print("\nFinal Status:")
    print(f"  Compromised cells: {final_report['total_cells_affected']}")
    print(f"  Infrastructure failures by type:")
    for infra, count in final_report["infrastructure_failures"].items():
        print(f"    {infra}: {count} cells")
    
    print("\nInfrastructure Health:")
    for infra, health in infra_status.items():
        health_pct = health * 100
        status_bar = "█" * int(health_pct / 5) + "░" * (20 - int(health_pct / 5))
        print(f"  {infra:15s}: {status_bar} {health_pct:5.1f}%")


def main():
    """Run all batch 3 demos."""
    print("\n" + "=" * 80)
    print("BATCH 3 DEMO: Multi-Hazard Disaster Simulation Engine")
    print("=" * 80)
    
    demo_scenario_1_single_flood()
    demo_scenario_2_earthquake_cascade()
    demo_scenario_3_pandemic_spread()
    demo_scenario_4_multi_disaster()
    demo_scenario_5_cyber_cascade()
    
    print("\n" + "=" * 80)
    print("All Batch 3 demos completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
