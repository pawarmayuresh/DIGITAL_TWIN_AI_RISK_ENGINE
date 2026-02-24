"""
Digital Twin API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
from pathlib import Path

router = APIRouter()

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from core.digital_twin import TwinManager
from core.spatial_engine import GridManager, CellMetadata
from core.cascading_engine import InfrastructureGraph, InfrastructureNode, InfrastructureNodeType
from core.disaster_engine import DisasterManager

# Global twin manager instance (in production, use proper state management)
twin_manager = TwinManager()


class TwinInitConfig(BaseModel):
    """Configuration for initializing a digital twin"""
    city_id: str
    city_name: str
    total_population: int
    total_area_km2: float
    gdp: float
    grid_width: int = 20
    grid_height: int = 20


@router.post("/initialize")
async def initialize_twin(config: TwinInitConfig):
    """Initialize a new digital twin"""
    try:
        # Create grid
        grid = GridManager(width=config.grid_width, height=config.grid_height, cell_size=1.0)
        
        # Create cells
        for x in range(config.grid_width):
            for y in range(config.grid_height):
                metadata = CellMetadata(x=x, y=y, population_density=100.0)
                grid.create_cell(x, y, metadata)
        
        # Create infrastructure graph
        infra_graph = InfrastructureGraph()
        
        # Add some infrastructure nodes
        for i in range(5):
            infra_graph.add_node(
                node_id=f"power_node_{i+1}",
                node_type=InfrastructureNodeType.POWER_PLANT,
                location=(i * 4, 10),
                capacity=1000.0
            )
        
        for i in range(3):
            infra_graph.add_node(
                node_id=f"water_node_{i+1}",
                node_type=InfrastructureNodeType.WATER_TREATMENT,
                location=(i * 6, 5),
                capacity=500.0
            )
        
        # Create disaster manager
        disaster_mgr = DisasterManager()
        
        # Initialize twin
        result = twin_manager.initialize_twin(
            city_id=config.city_id,
            city_name=config.city_name,
            total_population=config.total_population,
            total_area_km2=config.total_area_km2,
            gdp=config.gdp,
            grid_manager=grid,
            infrastructure_graph=infra_graph,
            disaster_manager=disaster_mgr
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_twin_status():
    """Get current twin status"""
    try:
        status = twin_manager.get_twin_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/population")
async def get_population_status():
    """Get population metrics"""
    try:
        if not twin_manager.population_model:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        return twin_manager.population_model.get_status_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economy")
async def get_economic_status():
    """Get economic metrics"""
    try:
        if not twin_manager.economic_model:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        return twin_manager.economic_model.get_economic_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assets")
async def get_critical_assets():
    """Get critical asset status"""
    try:
        if not twin_manager.asset_registry:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        return {
            "summary": twin_manager.asset_registry.get_operational_summary(),
            "assets": twin_manager.asset_registry.export_assets()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulate")
async def run_simulation(steps: int = 10):
    """Run simulation for N steps"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        results = []
        for step in range(steps):
            status = twin_manager.run_simulation_step()
            results.append(status)
        
        return {
            "steps_completed": steps,
            "final_status": results[-1] if results else {},
            "all_steps": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/baseline/compare")
async def compare_to_baseline():
    """Compare current state to baseline"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        comparison = twin_manager.compare_to_baseline()
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/impact-report")
async def get_impact_report():
    """Get comprehensive impact report"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        report = twin_manager.generate_impact_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resilience")
async def get_resilience_metrics():
    """Get resilience metrics"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        metrics = twin_manager.get_resilience_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_twin():
    """Reset twin to baseline state"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        twin_manager.reset_to_baseline()
        return {"status": "reset", "message": "Twin reset to baseline state"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export")
async def export_twin_state():
    """Export complete twin state"""
    try:
        if not twin_manager.is_initialized:
            raise HTTPException(status_code=404, detail="Twin not initialized")
        
        state = twin_manager.export_twin_state()
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
