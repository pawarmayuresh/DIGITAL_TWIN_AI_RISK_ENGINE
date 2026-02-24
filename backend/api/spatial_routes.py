"""
Spatial API Routes
Provides endpoints for spatial grid data and visualization
"""
from fastapi import APIRouter
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["spatial"])

# Import spatial modules
try:
    from backend.core.spatial_engine.grid_manager import GridManager
except ImportError:
    GridManager = None


class CellUpdate(BaseModel):
    disaster_intensity: Optional[float] = None
    population: Optional[int] = None
    infrastructure_health: Optional[float] = None


@router.get("/grid")
async def get_grid():
    """Get current grid state"""
    if not GridManager:
        # Return mock grid data
        grid = []
        for y in range(20):
            for x in range(20):
                grid.append({
                    "x": x,
                    "y": y,
                    "disaster_intensity": 0.0,
                    "population": 1000,
                    "infrastructure_health": 1.0
                })
        return {"grid": grid, "size": 20}
    
    manager = GridManager(size=20)
    grid_data = []
    for y in range(manager.size):
        for x in range(manager.size):
            cell = manager.get_cell(x, y)
            if cell:
                grid_data.append({
                    "x": x,
                    "y": y,
                    "disaster_intensity": cell.disaster_intensity,
                    "population": cell.population,
                    "infrastructure_health": cell.infrastructure_health
                })
    
    return {"grid": grid_data, "size": manager.size}


@router.get("/grid/{x}/{y}")
async def get_cell(x: int, y: int):
    """Get specific cell data"""
    if not GridManager:
        return {
            "x": x,
            "y": y,
            "disaster_intensity": 0.0,
            "population": 1000,
            "infrastructure_health": 1.0
        }
    
    manager = GridManager(size=20)
    cell = manager.get_cell(x, y)
    if not cell:
        return {"error": "Cell not found"}
    
    return {
        "x": x,
        "y": y,
        "disaster_intensity": cell.disaster_intensity,
        "population": cell.population,
        "infrastructure_health": cell.infrastructure_health
    }


@router.put("/grid/{x}/{y}")
async def update_cell(x: int, y: int, update: CellUpdate):
    """Update cell data"""
    if not GridManager:
        return {"success": True, "x": x, "y": y}
    
    manager = GridManager(size=20)
    cell = manager.get_cell(x, y)
    if not cell:
        return {"error": "Cell not found"}
    
    if update.disaster_intensity is not None:
        cell.disaster_intensity = update.disaster_intensity
    if update.population is not None:
        cell.population = update.population
    if update.infrastructure_health is not None:
        cell.infrastructure_health = update.infrastructure_health
    
    return {"success": True, "x": x, "y": y}
