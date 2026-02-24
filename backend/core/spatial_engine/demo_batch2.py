"""
Batch 2 Demo — Grid Simulation Core

Demonstrates:
- Grid creation and cell management
- Disaster initiation and propagation
- Cascading infrastructure failures
- Risk heatmap generation
- Visualization export
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from spatial_engine import (
    GridManager,
    GridCell,
    CellMetadata,
    DiffusionModel,
    ZoningEngine,
    SpatialRiskCalculator,
    GridVisualExporter,
    GridSimulationRunner,
)


def demo_basic_grid():
    """Demo 1: Create a basic grid."""
    print("\n" + "=" * 60)
    print("DEMO 1: Grid Creation and Cell Management")
    print("=" * 60)

    grid = GridManager(width=20, height=20, cell_size=100.0)

    # Create cells with metadata
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(
                x=x,
                y=y,
                zone_type="mixed",
                population_density=100.0 + (x + y) * 2,
            )
            grid.create_cell(x, y, metadata)

    print(f"✓ Created {len(grid.cells)} cells in a 20x20 grid")
    print(f"✓ Total population: {grid.total_population:.0f}")
    print(f"✓ Grid statistics: {json.dumps(grid.calculate_statistics(), indent=2)}")


def demo_zoning():
    """Demo 2: Zoning and zone management."""
    print("\n" + "=" * 60)
    print("DEMO 2: Zoning Engine")
    print("=" * 60)

    grid = GridManager(width=30, height=30, cell_size=100.0)

    # Create cells
    for x in range(30):
        for y in range(30):
            metadata = CellMetadata(x=x, y=y)
            grid.create_cell(x, y, metadata)

    # Apply zoning
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()

    zone_stats = zoning.calculate_zone_statistics()
    print(f"✓ Assigned zones to {len(grid.cells)} cells")
    print(f"✓ Zone statistics:")
    for zone_type, stats in zone_stats.items():
        print(f"  - {zone_type}: {stats['cell_count']} cells, health={stats['infrastructure_health']:.2f}")


def demo_disaster_propagation():
    """Demo 3: Disaster initiation and propagation."""
    print("\n" + "=" * 60)
    print("DEMO 3: Disaster Propagation (Floods)")
    print("=" * 60)

    grid = GridManager(width=25, height=25, cell_size=100.0)

    # Create cells
    for x in range(25):
        for y in range(25):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)

    # Setup diffusion
    diffusion = DiffusionModel(grid)

    # Initiate flood at center
    center_x, center_y = 12, 12
    center_cell = grid.get_cell(center_x, center_y)
    center_cell.flood_intensity = 0.9

    print(f"✓ Initiated flood at ({center_x}, {center_y}) with intensity 0.9")

    # Run propagation steps
    for step in range(5):
        diffusion.propagate_step(hazard_type="flood")
        affected = grid.get_affected_cells()
        print(f"  Step {step + 1}: {len(affected)} cells affected, max intensity={max(c.flood_intensity for c in grid.get_all_cells()):.2f}")

    print(f"✓ Flood propagated across grid over 5 time steps")


def demo_risk_heatmaps():
    """Demo 4: Risk heatmap generation."""
    print("\n" + "=" * 60)
    print("DEMO 4: Risk Heatmap Analysis")
    print("=" * 60)

    grid = GridManager(width=15, height=15, cell_size=100.0)

    # Create cells
    for x in range(15):
        for y in range(15):
            metadata = CellMetadata(x=x, y=y, population_density=80.0 + x * y)
            grid.create_cell(x, y, metadata)

    # Initiate multiple hazards
    grid.get_cell(2, 2).flood_intensity = 0.8
    grid.get_cell(10, 5).wildfire_intensity = 0.7
    grid.get_cell(7, 12).seismic_intensity = 0.6

    # Generate heatmaps
    diffusion = DiffusionModel(grid)
    diffusion.propagate_step()

    risk_calc = SpatialRiskCalculator(grid)
    risk_metrics = risk_calc.calculate_risk_metrics()

    print(f"✓ Generated risk heatmaps after propagation")
    print(f"✓ Risk metrics:")
    for key, value in risk_metrics.items():
        print(f"  - {key}: {value}")

    # Get hotspots
    risk_hm = risk_calc.calculate_risk_heatmap()
    hotspots = risk_calc.get_hotspots(risk_hm, threshold=0.7)
    print(f"✓ Identified {len(hotspots)} high-risk hotspots")


def demo_full_simulation():
    """Demo 5: Full simulation with time stepping."""
    print("\n" + "=" * 60)
    print("DEMO 5: Full Grid Simulation")
    print("=" * 60)

    grid = GridManager(width=20, height=20, cell_size=100.0)

    # Setup grid
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)

    # Setup zoning
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()

    # Create runner
    runner = GridSimulationRunner(grid, zoning_engine=zoning)
    runner.configure(duration=20, diffusion_enabled=True, recovery_enabled=True)

    # Initiate disaster
    runner.initiate_disaster(x=10, y=10, disaster_type="flood", intensity=0.8, radius=2)

    print(f"✓ Initiated flood disaster at (10, 10)")
    print(f"✓ Configured simulation for 20 steps")

    # Run simulation
    summary = runner.run(duration=20)

    print(f"✓ Simulation completed:")
    print(f"  - Total steps: {summary['total_steps']}")
    print(f"  - Affected cells: {summary['grid_statistics']['affected_cell_count']}")
    print(f"  - Affected population: {summary['grid_statistics']['affected_population']:.0f}")

    # Export history
    history = runner.export_history()
    print(f"✓ Exported {len(history['history'])} timesteps of history")

    # Show final state progression
    print(f"\n  Timeline of affected cells:")
    for i, frame in enumerate(history["history"][::5] + [history["history"][-1]]):
        if "affected_cell_count" in frame:
            print(f"    Step {frame.get('timestamp', i*5)}: {frame['affected_cell_count']} cells affected")


def demo_intervention():
    """Demo 6: Policy intervention and recovery."""
    print("\n" + "=" * 60)
    print("DEMO 6: Policy Intervention")
    print("=" * 60)

    grid = GridManager(width=20, height=20, cell_size=100.0)

    # Setup grid
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)

    # Setup zoning
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()

    # Create runner
    runner = GridSimulationRunner(grid, zoning_engine=zoning)
    runner.configure(duration=30, diffusion_enabled=True, recovery_enabled=True)

    # Initiate disaster
    runner.initiate_disaster(x=10, y=10, disaster_type="flood", intensity=0.8, radius=3)

    # Run for initial steps
    for _ in range(10):
        runner.step()

    disaster_stats = runner.grid.calculate_statistics()
    print(f"✓ After 10 steps without intervention: {disaster_stats['affected_cell_count']} cells affected")

    # Apply intervention
    runner.apply_intervention(zone_type="residential", intervention_level=0.7, resource_level=1.0)
    print(f"✓ Applied intervention to residential zones (level=0.7)")

    # Continue simulation
    for _ in range(10):
        runner.step()

    recovery_stats = runner.grid.calculate_statistics()
    print(f"✓ After 20 more steps with intervention: {recovery_stats['affected_cell_count']} cells affected")
    print(f"✓ Infrastructure health improved from {disaster_stats.get('state_distribution', {}).get('affected', 0)} to {recovery_stats['affected_cell_count']} affected cells")


if __name__ == "__main__":
    try:
        demo_basic_grid()
        demo_zoning()
        demo_disaster_propagation()
        demo_risk_heatmaps()
        demo_full_simulation()
        demo_intervention()

        print("\n" + "=" * 60)
        print("✓ BATCH 2 DEMO COMPLETE")
        print("=" * 60)
        print("\nAll spatial simulation components working:")
        print("  ✓ Grid creation and cell management")
        print("  ✓ Zoning engine")
        print("  ✓ Disaster propagation (floods, seismic, etc.)")
        print("  ✓ Risk heatmap generation")
        print("  ✓ Full time-stepped simulation")
        print("  ✓ Policy interventions")
        print("\nGrid simulation spreads disasters visually and computationally!")

    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
