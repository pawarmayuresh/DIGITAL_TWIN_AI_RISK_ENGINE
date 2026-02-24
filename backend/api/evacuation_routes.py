"""
Evacuation System API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from backend.evacuation_system.grid_engine import MumbaiGridEngine
from backend.evacuation_system.pathfinder import EvacuationPathfinder
from backend.evacuation_system.human_agent_sim import EvacuationSimulator
from backend.evacuation_system.car_evacuation_manager import CarEvacuationManager
from backend.core.explainable_ai.decision_logger import decision_logger

router = APIRouter(prefix="/api/evacuation", tags=["evacuation"])

# Global instances (in production, use proper state management)
grid_engine = None
pathfinder = None
simulator = None
car_manager = None

def initialize_system():
    """Initialize evacuation system"""
    global grid_engine, pathfinder, simulator, car_manager
    if not grid_engine:
        grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
        pathfinder = EvacuationPathfinder(grid_engine)
        simulator = EvacuationSimulator(grid_engine, pathfinder)
        car_manager = CarEvacuationManager(grid_engine)

@router.get("/grid")
async def get_grid_data(ward_id: str = None, risk_multiplier: float = 1.0):
    """Get Mumbai grid data with safety levels, optionally focused on a ward"""
    initialize_system()
    
    # Import real-time data
    import pandas as pd
    import os
    
    try:
        # Load real-time sensor data for reference only
        base_path = "data/mumbai/realtime"
        water_sensors = pd.read_csv(f"{base_path}/water_level_sensors.csv")
        rain_sensors = pd.read_csv(f"{base_path}/rain_sensors.csv")
        
        # Log risk assessments for dangerous zones only (don't modify grid)
        for grid in grid_engine.grids.values():
            if grid.safety_level.value == "DANGEROUS":
                # Log risk assessment for dangerous zones
                features = {
                    "water_level": grid.water_level,
                    "rainfall": grid.rainfall,
                    "population_density": grid.population_density,
                    "risk_score": grid.risk_score
                }
                
                contributions = {
                    "water_level": grid.water_level * 0.40,
                    "rainfall": (grid.rainfall / 100) * 0.35,
                    "population_density": (grid.population_density / 1000) * 0.15,
                    "infrastructure": 0.10 if grid.infrastructure_status != "operational" else 0.0
                }
                
                decision_logger.log_risk_decision(
                    ward_id=grid.id,
                    risk_score=grid.risk_score,
                    features=features,
                    action="EVACUATION_REQUIRED",
                    confidence=0.85 if grid.risk_score > 0.7 else 0.70,
                    feature_contributions=contributions
                )
    
    except Exception as e:
        print(f"Warning: Could not load real-time data: {e}")
        # Use simulated data if files not found
        pass
    
    # Don't adjust by ward - use natural grid distribution
    # This ensures a good mix of safe, medium, and dangerous zones
    
    return grid_engine.to_dict()

@router.get("/safe-zones")
async def get_safe_zones():
    """Get all safe zones"""
    initialize_system()
    safe_zones = grid_engine.get_safe_zones()
    return {
        "count": len(safe_zones),
        "zones": [
            {
                "id": z.id,
                "name": z.name,
                "row": z.row,
                "col": z.col,
                "latitude": z.latitude,
                "longitude": z.longitude,
                "is_evacuation_point": z.is_evacuation_point
            }
            for z in safe_zones
        ]
    }

@router.get("/dangerous-zones")
async def get_dangerous_zones():
    """Get all dangerous zones"""
    initialize_system()
    dangerous_zones = grid_engine.get_dangerous_zones()
    return {
        "count": len(dangerous_zones),
        "zones": [
            {
                "id": z.id,
                "name": z.name,
                "row": z.row,
                "col": z.col,
                "risk_score": z.risk_score,
                "water_level": z.water_level,
                "population_density": z.population_density
            }
            for z in dangerous_zones
        ]
    }


@router.post("/find-path")
async def find_evacuation_path(start_grid_id: str, goal_grid_id: str):
    """Find optimal evacuation path between two grids"""
    initialize_system()
    
    start_grid = grid_engine.get_grid(start_grid_id)
    goal_grid = grid_engine.get_grid(goal_grid_id)
    
    if not start_grid or not goal_grid:
        raise HTTPException(status_code=404, detail="Grid not found")
    
    result = pathfinder.find_path(start_grid, goal_grid)
    
    # Log evacuation path decision
    if result.get("success"):
        decision_logger.log_evacuation_decision(
            grid_id=start_grid_id,
            path_selected=result.get("path_ids", []),
            path_cost=result.get("total_cost", 0),
            alternatives_considered=result.get("nodes_explored", 0),
            reason=f"Optimal path from {start_grid.name} to {goal_grid.name} with risk score {result.get('average_risk', 0):.2f}"
        )
    
    return result

@router.post("/initialize-simulation")
async def initialize_simulation(agents_per_zone: int = 3):
    """Initialize evacuation simulation with agents"""
    try:
        initialize_system()
        
        # Reset simulator
        global simulator
        simulator = EvacuationSimulator(grid_engine, pathfinder)
        
        # Create agents in dangerous zones
        agents = simulator.create_agents_in_dangerous_zones(agents_per_zone)
        
        print(f"✅ Created {len(agents)} human agents")
        
        # Assign evacuation paths
        simulator.assign_evacuation_paths()
        
        print(f"✅ Assigned evacuation paths")
        
        # Log agent decisions for each agent
        for agent in agents:
            if agent.path and len(agent.path) > 0:
                # Extract features from agent's current grid
                current_grid = agent.current_grid
                features = {
                    "risk_score": current_grid.risk_score,
                    "water_level": current_grid.water_level,
                    "rainfall": current_grid.rainfall,
                    "population_density": current_grid.population_density,
                    "agent_age_group": agent.age_group,
                    "agent_speed": agent.speed
                }
                
                # Calculate feature contributions (simplified)
                contributions = {
                    "risk_score": current_grid.risk_score * 0.4,
                    "water_level": current_grid.water_level * 0.3,
                    "rainfall": (current_grid.rainfall / 100) * 0.2,
                    "population_density": (current_grid.population_density / 1000) * 0.1
                }
                
                decision_logger.log_agent_decision(
                    agent_id=agent.id,
                    decision_type="evacuation_path_selection",
                    context={
                        "current_grid": current_grid.id,
                        "destination_grid": agent.destination_grid.id if agent.destination_grid else None,
                        "path_length": len(agent.path),
                        "features": features
                    },
                    action_taken=f"Selected path to {agent.destination_grid.name if agent.destination_grid else 'unknown'}",
                    reasoning=f"Agent in {agent.age_group} group evacuating from high-risk zone {current_grid.name}"
                )
        
        return {
            "success": True,
            "agents_created": len(agents),
            "stats": simulator.evacuation_stats,
            "agents": [agent.to_dict() for agent in agents]
        }
    except Exception as e:
        print(f"❌ Error in initialize_simulation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to initialize simulation: {str(e)}")

@router.post("/simulation-step")
async def run_simulation_step():
    """Run one step of evacuation simulation"""
    try:
        if not simulator:
            raise HTTPException(status_code=400, detail="Simulation not initialized")
        
        result = simulator.simulate_step()
        return result
    except Exception as e:
        print(f"❌ Error in simulation_step: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Simulation step failed: {str(e)}")

@router.get("/simulation-paths")
async def get_simulation_paths():
    """Get all evacuation paths for visualization"""
    if not simulator:
        # Return empty paths instead of error to avoid CORS issues
        return {
            "paths": [],
            "stats": {
                "total_agents": 0,
                "evacuating": 0,
                "safe": 0,
                "stuck": 0,
                "average_health": 100
            }
        }
    
    paths = simulator.get_all_paths()
    return {
        "paths": paths,
        "stats": simulator.evacuation_stats
    }

@router.get("/simulation-status")
async def get_simulation_status():
    """Get current simulation status"""
    if not simulator:
        return {"initialized": False}
    
    return {
        "initialized": True,
        "step": simulator.simulation_step,
        "stats": simulator.evacuation_stats,
        "is_complete": simulator.is_complete(),
        "agents": [agent.to_dict() for agent in simulator.agents.values()]
    }

@router.post("/reset-simulation")
async def reset_simulation():
    """Reset the simulation"""
    global simulator
    if simulator:
        simulator = EvacuationSimulator(grid_engine, pathfinder)
    return {"success": True, "message": "Simulation reset"}

@router.post("/reset-all")
async def reset_all_systems():
    """Reset entire evacuation system including grid"""
    global grid_engine, pathfinder, simulator, car_manager
    
    # Force recreation of all systems
    grid_engine = MumbaiGridEngine(grid_rows=20, grid_cols=20)
    pathfinder = EvacuationPathfinder(grid_engine)
    simulator = EvacuationSimulator(grid_engine, pathfinder)
    car_manager = CarEvacuationManager(grid_engine)
    
    return {
        "success": True,
        "message": "All systems reset with fresh grid",
        "grid_stats": {
            "total": len(grid_engine.grids),
            "safe": len(grid_engine.get_safe_zones()),
            "dangerous": len(grid_engine.get_dangerous_zones())
        }
    }

@router.post("/update-realtime")
async def update_realtime_conditions():
    """Simulate real-time changes in grid conditions"""
    initialize_system()
    grid_engine.simulate_realtime_changes()
    return {
        "success": True,
        "message": "Grid conditions updated",
        "grid_data": grid_engine.to_dict()
    }

@router.get("/grid-stats")
async def get_grid_statistics():
    """Get statistics about current grid state"""
    initialize_system()
    
    safe_count = len(grid_engine.get_safe_zones())
    dangerous_count = len(grid_engine.get_dangerous_zones())
    total = len(grid_engine.grids)
    medium_count = total - safe_count - dangerous_count
    
    avg_risk = sum(g.risk_score for g in grid_engine.grids.values()) / total
    avg_water = sum(g.water_level for g in grid_engine.grids.values()) / total
    avg_rainfall = sum(g.rainfall for g in grid_engine.grids.values()) / total
    
    return {
        "total_grids": total,
        "safe_zones": safe_count,
        "medium_risk_zones": medium_count,
        "dangerous_zones": dangerous_count,
        "average_risk_score": round(avg_risk, 3),
        "average_water_level": round(avg_water, 2),
        "average_rainfall": round(avg_rainfall, 2),
        "evacuation_points": len(grid_engine.get_evacuation_points())
    }


# ==================== CAR EVACUATION ENDPOINTS ====================

@router.post("/car/add")
async def add_car(car_id: str, name: str, start_grid: str = "A1", capacity: int = 50):
    """Add a new evacuation car"""
    initialize_system()
    
    car = car_manager.add_car(car_id, name, start_grid, capacity)
    return {
        "success": True,
        "car": car.to_dict()
    }

@router.post("/car/assign-mission")
async def assign_car_mission(car_id: str, danger_grid_id: str):
    """Assign evacuation mission to a car"""
    initialize_system()
    
    result = car_manager.assign_mission(car_id, danger_grid_id)
    
    # Log car mission decision
    if result and result.get("success"):
        danger_grid = grid_engine.get_grid(danger_grid_id)
        safe_grid = grid_engine.get_grid(result.get("safe_grid"))
        
        if danger_grid and safe_grid:
            features = {
                "danger_risk_score": danger_grid.risk_score,
                "danger_population": danger_grid.population_density,
                "danger_water_level": danger_grid.water_level,
                "safe_risk_score": safe_grid.risk_score,
                "path_length": len(result.get("path_to_danger", {}).get("path_ids", []))
            }
            
            contributions = {
                "danger_risk_score": danger_grid.risk_score * 0.35,
                "danger_population": (danger_grid.population_density / 1000) * 0.30,
                "danger_water_level": danger_grid.water_level * 0.20,
                "path_length": (len(result.get("path_to_danger", {}).get("path_ids", [])) / 20) * 0.15
            }
            
            decision_logger.log_agent_decision(
                agent_id=car_id,
                decision_type="car_mission_assignment",
                context={
                    "danger_grid": danger_grid_id,
                    "safe_grid": result.get("safe_grid"),
                    "features": features
                },
                action_taken=f"Assigned mission from {danger_grid.name} to {safe_grid.name}",
                reasoning=f"Car evacuation mission to rescue {danger_grid.population_density} people from high-risk zone"
            )
    
    return result

@router.post("/car/simulate-step")
async def car_simulation_step():
    """Run one step of car evacuation simulation"""
    try:
        if not car_manager:
            raise HTTPException(status_code=400, detail="Car system not initialized")
        
        result = car_manager.simulate_step()
        return result
    except Exception as e:
        print(f"❌ Error in car_simulation_step: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Car simulation step failed: {str(e)}")

@router.get("/car/status")
async def get_car_status():
    """Get current car evacuation status"""
    if not car_manager:
        return {"initialized": False}
    
    return {
        "initialized": True,
        **car_manager.get_status()
    }

@router.post("/car/reset")
async def reset_car_system():
    """Reset car evacuation system"""
    global car_manager
    initialize_system()
    
    # Clear all cars and recreate manager
    car_manager.cars.clear()
    car_manager.simulation_step = 0
    car_manager.total_evacuated = 0
    car_manager.active_missions = 0
    
    print("🔄 Car system reset - all cars cleared")
    
    return {"success": True, "message": "Car system reset"}

@router.post("/car/auto-assign")
async def auto_assign_cars():
    """Automatically assign cars to all danger zones"""
    initialize_system()
    
    # Get all dangerous zones
    dangerous_zones = grid_engine.get_dangerous_zones()
    print(f"🚨 Found {len(dangerous_zones)} dangerous zones")
    
    if len(dangerous_zones) == 0:
        print("⚠️ WARNING: No dangerous zones found! Grid may not be initialized properly.")
        # Force create some dangerous zones for testing
        for grid_id in ['A3', 'A9', 'B5', 'C7', 'D10']:
            grid = grid_engine.get_grid(grid_id)
            if grid:
                grid.safety_level = grid_engine.grids[grid_id].safety_level.__class__.DANGEROUS
                grid.risk_score = 0.8
                grid.population_density = max(grid.population_density, 1000)
                print(f"  🔧 Forced {grid_id} to be dangerous with population {grid.population_density}")
        
        dangerous_zones = grid_engine.get_dangerous_zones()
        print(f"🚨 After forcing: {len(dangerous_zones)} dangerous zones")
    
    for zone in dangerous_zones[:5]:  # Print first 5
        print(f"  - {zone.id} ({zone.name}): Population {zone.population_density}, Risk {zone.risk_score:.2f}")
    
    # Create cars if needed
    if len(car_manager.cars) == 0:
        safe_zones = grid_engine.get_safe_zones()
        print(f"✅ Found {len(safe_zones)} safe zones")
        
        if safe_zones:
            start_grid = safe_zones[0].id
            for i in range(min(5, max(len(dangerous_zones), 5))):  # Always create 5 cars
                car_manager.add_car(f"CAR-{i+1}", f"Rescue Vehicle {i+1}", start_grid, capacity=50)
                print(f"🚗 Added car CAR-{i+1} at {start_grid}")
        else:
            print("❌ ERROR: No safe zones found!")
            return {
                "success": False,
                "message": "No safe zones available",
                "dangerous_zones_found": len(dangerous_zones),
                "safe_zones_found": 0,
                "cars": [],
                "missions_assigned": 0
            }
    
    # Assign missions
    assignments = []
    car_list = list(car_manager.cars.values())
    print(f"🚗 Assigning missions to {len(car_list)} cars")
    
    for i, danger_zone in enumerate(dangerous_zones[:len(car_list)]):
        if danger_zone.population_density > 0:
            car = car_list[i % len(car_list)]
            print(f"  Trying to assign {car.id} to {danger_zone.id} (pop: {danger_zone.population_density})")
            
            if car.state.value == "IDLE":
                result = car_manager.assign_mission(car.id, danger_zone.id)
                if result and result.get("success"):
                    assignments.append(result)
                    print(f"  ✅ Mission assigned: {car.id} → {danger_zone.id}")
                else:
                    print(f"  ❌ Failed to assign mission: {result}")
            else:
                print(f"  ⏸️ Car {car.id} is busy ({car.state.value})")
    
    print(f"📊 Total missions assigned: {len(assignments)}")
    
    return {
        "success": True,
        "missions_assigned": len(assignments),
        "assignments": assignments,
        "cars": [car.to_dict() for car in car_manager.cars.values()],
        "dangerous_zones_found": len(dangerous_zones),
        "safe_zones_found": len(grid_engine.get_safe_zones())
    }
