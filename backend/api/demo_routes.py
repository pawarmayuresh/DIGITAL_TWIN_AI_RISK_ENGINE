"""Demo visualization routes — expose Batch 2 & 3 simulations via API."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

router = APIRouter()

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from core.spatial_engine import (
    GridManager,
    CellMetadata,
    ZoningEngine,
)
from core.disaster_engine import (
    DisasterEvent,
    DisasterType,
    DisasterManager,
    SpatialImpactCalculator,
    DisasterConfigLoader,
)


@router.get("/scenarios")
async def get_available_scenarios():
    """Get list of available demo scenarios."""
    scenarios = [
        {
            "id": "spatial-grid",
            "name": "Spatial Grid Simulation",
            "description": "Basic grid creation with 400 cells",
            "batch": 2,
        },
        {
            "id": "flood",
            "name": "Single Flood Disaster",
            "description": "Flood propagation on 20x20 grid",
            "batch": 3,
        },
        {
            "id": "earthquake-cascade",
            "name": "Earthquake with Cascade",
            "description": "Earthquake triggering secondary disasters",
            "batch": 3,
        },
        {
            "id": "pandemic",
            "name": "Pandemic Wave",
            "description": "Infection spread across population",
            "batch": 3,
        },
        {
            "id": "multi-disaster",
            "name": "Multi-Disaster Scenario",
            "description": "Simultaneous earthquake, flood, fire, pandemic",
            "batch": 3,
        },
        {
            "id": "cyber-cascade",
            "name": "Cyber Attack Cascade",
            "description": "Network attack with cascading infrastructure failure",
            "batch": 3,
        },
        {
            "id": "cascade-demo",
            "name": "Cascading Failure Engine",
            "description": "Infrastructure collapse simulation (Batch 4)",
            "batch": 4,
        },
    ]
    return {"scenarios": scenarios}


@router.get("/run/{scenario_id}")
async def run_demo_scenario(scenario_id: str):
    """Run a specific demo scenario and return results."""
    
    try:
        if scenario_id == "flood":
            return await _run_flood_demo()
        elif scenario_id == "earthquake-cascade":
            return await _run_earthquake_demo()
        elif scenario_id == "pandemic":
            return await _run_pandemic_demo()
        elif scenario_id == "multi-disaster":
            return await _run_multi_disaster_demo()
        elif scenario_id == "cyber-cascade":
            return await _run_cyber_demo()
        elif scenario_id == "cascade-demo":
            return await _run_cascade_demo()
        else:
            raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _run_flood_demo():
    """Run single flood event demo."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    # Create cells
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    # Add zones
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    # Create disaster
    dm = DisasterManager()
    flood = DisasterEvent(
        event_id="flood-1",
        disaster_type=DisasterType.FLOOD,
        severity=0.7,
        epicenter=(10, 10),
        radius_km=5.0,
        onset_time=0,
    )
    dm.add_disaster(dm._create_disaster(flood))
    
    # Run simulation
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(15):
        dm.propagate_all(grid, None)
        spatial_calc.apply_impacts(grid)
    
    # Collect results
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    
    return {
        "scenario": "flood",
        "total_cells_affected": final_report["total_cells_affected"],
        "population_affected": int(final_report["population_affected"]),
        "infrastructure_failures": final_report["infrastructure_failures"],
        "critical_zones": len(final_report["critical_zones"]),
        "infrastructure_status": infra_status,
    }


async def _run_earthquake_demo():
    """Run earthquake with cascade demo."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    dm = DisasterManager()
    earthquake = DisasterEvent(
        event_id="earthquake-1",
        disaster_type=DisasterType.EARTHQUAKE,
        severity=0.8,
        epicenter=(10, 10),
        radius_km=6.0,
        onset_time=0,
    )
    dm.add_disaster(dm._create_disaster(earthquake))
    
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(20):
        dm.propagate_all(grid, None)
        for disaster in list(dm.active_disasters.values()):
            dm.trigger_cascades(grid, disaster)
        spatial_calc.apply_impacts(grid)
    
    final_report = spatial_calc.apply_impacts(grid)
    final_summary = dm.get_summary()
    
    return {
        "scenario": "earthquake_cascade",
        "total_cells_affected": final_report["total_cells_affected"],
        "population_affected": int(final_report["population_affected"]),
        "active_disasters": dm.get_active_disaster_count(),
        "disaster_types_triggered": final_summary["by_type"],
        "critical_zones": len(final_report["critical_zones"]),
    }


async def _run_pandemic_demo():
    """Run pandemic spread demo."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
            # High density in urban areas
            if (x > 8 and x < 12) or (y > 8 and y < 12):
                grid.get_cell(x, y).metadata.population_density = 300.0
    
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    dm = DisasterManager()
    pandemic = DisasterEvent(
        event_id="pandemic-1",
        disaster_type=DisasterType.PANDEMIC,
        severity=0.6,
        epicenter=(10, 10),
        radius_km=8.0,
        onset_time=0,
    )
    dm.add_disaster(dm._create_disaster(pandemic))
    
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(25):
        dm.propagate_all(grid, None)
        spatial_calc.apply_impacts(grid)
    
    final_report = spatial_calc.apply_impacts(grid)
    vuln = spatial_calc.get_population_vulnerability(grid)
    
    return {
        "scenario": "pandemic",
        "total_affected_cells": final_report["total_cells_affected"],
        "population_affected": int(final_report["population_affected"]),
        "total_population": int(vuln["total_population"]),
        "at_risk_population": int(vuln["at_risk_population"]),
        "vulnerability_index": vuln["vulnerability_index"],
    }


async def _run_multi_disaster_demo():
    """Run multi-disaster scenario."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    dm = DisasterManager()
    
    # Load multi-disaster scenario
    scenario = DisasterConfigLoader.get_preset_scenario("multi_disaster")
    events = DisasterConfigLoader.load_scenario(scenario)
    
    for event in events:
        disaster = dm._create_disaster(event)
        if disaster:
            dm.add_disaster(disaster)
    
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(30):
        for event in events:
            if event.onset_time == tick:
                disaster = dm._create_disaster(event)
                if disaster:
                    dm.add_disaster(disaster)
        
        dm.propagate_all(grid, None)
        for disaster in list(dm.active_disasters.values()):
            dm.trigger_cascades(grid, disaster)
        spatial_calc.apply_impacts(grid)
    
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    vuln = spatial_calc.get_population_vulnerability(grid)
    
    return {
        "scenario": "multi_disaster",
        "affected_cells": final_report["total_cells_affected"],
        "population_at_risk": int(final_report["population_affected"]),
        "critical_zones": len(final_report["critical_zones"]),
        "infrastructure_status": {k: f"{v*100:.1f}%" for k, v in infra_status.items()},
        "vulnerability_index": f"{vuln['vulnerability_index']:.3f}",
    }


async def _run_cyber_demo():
    """Run cyber attack cascade demo."""
    grid = GridManager(width=15, height=15, cell_size=1.0)
    
    for x in range(15):
        for y in range(15):
            metadata = CellMetadata(x=x, y=y, population_density=120.0)
            grid.create_cell(x, y, metadata)
    
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    dm = DisasterManager()
    cyber = DisasterEvent(
        event_id="cyber-1",
        disaster_type=DisasterType.CYBER_ATTACK,
        severity=0.75,
        epicenter=(7, 7),
        radius_km=4.0,
        onset_time=0,
    )
    dm.add_disaster(dm._create_disaster(cyber))
    
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(20):
        dm.propagate_all(grid, None)
        spatial_calc.apply_impacts(grid)
    
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    
    return {
        "scenario": "cyber_cascade",
        "compromised_cells": final_report["total_cells_affected"],
        "infrastructure_failures": final_report["infrastructure_failures"],
        "infrastructure_health": {k: f"{v*100:.1f}%" for k, v in infra_status.items()},
    }


async def _run_cascade_demo():
    """Run cascading failure demo."""
    grid = GridManager(width=20, height=20, cell_size=1.0)
    
    for x in range(20):
        for y in range(20):
            metadata = CellMetadata(x=x, y=y, population_density=100.0)
            grid.create_cell(x, y, metadata)
    
    zoning = ZoningEngine(grid)
    zoning.assign_grid_zones_geographic()
    
    dm = DisasterManager()
    
    # Load multi-disaster scenario
    scenario = DisasterConfigLoader.get_preset_scenario("multi_disaster")
    events = DisasterConfigLoader.load_scenario(scenario)
    
    for event in events:
        disaster = dm._create_disaster(event)
        if disaster:
            dm.add_disaster(disaster)
    
    spatial_calc = SpatialImpactCalculator(dm)
    for tick in range(30):
        for event in events:
            if event.onset_time == tick:
                disaster = dm._create_disaster(event)
                if disaster:
                    dm.add_disaster(disaster)
        
        dm.propagate_all(grid, None)
        for disaster in list(dm.active_disasters.values()):
            dm.trigger_cascades(grid, disaster)
        spatial_calc.apply_impacts(grid)
    
    final_report = spatial_calc.apply_impacts(grid)
    infra_status = spatial_calc.get_infrastructure_status(grid)
    vuln = spatial_calc.get_population_vulnerability(grid)
    
    return {
        "scenario": "cascade_demo",
        "affected_cells": final_report["total_cells_affected"],
        "population_at_risk": int(final_report["population_affected"]),
        "critical_zones": len(final_report["critical_zones"]),
        "infrastructure_status": {k: f"{v*100:.1f}%" for k, v in infra_status.items()},
        "vulnerability_index": f"{vuln['vulnerability_index']:.3f}",
    }
