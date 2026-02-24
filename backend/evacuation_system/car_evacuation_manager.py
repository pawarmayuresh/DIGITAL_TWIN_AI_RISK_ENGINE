"""
Car Evacuation Manager - Orchestrates car-based evacuation
Manages multiple cars, assigns missions, handles state transitions
"""
from typing import List, Dict, Optional
from .car_agent import CarAgent, CarState
from .car_pathfinder import CarPathfinder
from .grid_engine import MumbaiGridEngine

class CarEvacuationManager:
    """Manages car-based evacuation simulation"""
    
    def __init__(self, grid_engine: MumbaiGridEngine):
        self.grid_engine = grid_engine
        self.pathfinder = CarPathfinder(grid_engine, penalty_weight=10.0)
        self.cars: Dict[str, CarAgent] = {}
        self.simulation_step = 0
        self.total_evacuated = 0
        self.active_missions = 0
    
    def add_car(self, car_id: str, name: str, start_grid: str, capacity: int = 50) -> CarAgent:
        """Add a new car to the fleet"""
        car = CarAgent(
            id=car_id,
            name=name,
            capacity=capacity,
            current_grid_id=start_grid
        )
        self.cars[car_id] = car
        return car
    
    def assign_mission(self, car_id: str, danger_grid_id: str) -> Optional[Dict]:
        """Assign evacuation mission to a car"""
        car = self.cars.get(car_id)
        if not car or car.state != CarState.IDLE:
            print(f"❌ Cannot assign mission: car {car_id} not found or not idle")
            return None
        
        danger_grid = self.grid_engine.get_grid(danger_grid_id)
        if not danger_grid or danger_grid.population_density == 0:
            print(f"❌ Cannot assign mission: danger grid {danger_grid_id} has no population")
            return None
        
        print(f"🔍 Finding path from {car.current_grid_id} to {danger_grid_id}")
        
        # Find path to danger zone (allow entering danger at goal)
        path_to_danger = self.pathfinder.find_path(
            car.current_grid_id,
            danger_grid_id,
            allow_danger_at_goal=True
        )
        
        if not path_to_danger or not path_to_danger["success"]:
            print(f"❌ No path to danger zone {danger_grid_id}")
            return {"success": False, "message": "No path to danger zone"}
        
        print(f"✅ Path to danger found: {len(path_to_danger['path_ids'])} steps")
        
        # Find nearest safe zone
        safe_grid = self._find_nearest_safe_zone(danger_grid_id)
        if not safe_grid:
            print(f"❌ No safe zone available")
            return {"success": False, "message": "No safe zone available"}
        
        print(f"🔍 Finding path from {danger_grid_id} to safe zone {safe_grid.id}")
        
        # Find path to safe zone (from danger zone)
        path_to_safe = self.pathfinder.find_path(
            danger_grid_id,
            safe_grid.id,
            allow_danger_at_goal=False
        )
        
        if not path_to_safe or not path_to_safe["success"]:
            print(f"❌ No path to safe zone {safe_grid.id}")
            return {"success": False, "message": "No path to safe zone"}
        
        print(f"✅ Path to safe found: {len(path_to_safe['path_ids'])} steps")
        
        # Assign mission
        car.set_mission(
            danger_grid_id,
            safe_grid.id,
            path_to_danger["path_ids"],
            path_to_safe["path_ids"]
        )
        
        self.active_missions += 1
        
        print(f"✅ Mission assigned to {car_id}: {danger_grid_id} → {safe_grid.id}")
        
        return {
            "success": True,
            "car_id": car_id,
            "danger_grid": danger_grid_id,
            "safe_grid": safe_grid.id,
            "path_to_danger": path_to_danger,
            "path_to_safe": path_to_safe
        }
    
    def simulate_step(self) -> Dict:
        """Simulate one time step"""
        self.simulation_step += 1
        movements = []
        state_changes = []
        
        for car in self.cars.values():
            if car.state == CarState.IDLE:
                continue
            
            elif car.state == CarState.MOVING_TO_DANGER:
                if car.reached_destination():
                    # Arrived at danger zone
                    car.state = CarState.LOADING
                    state_changes.append({
                        "car_id": car.id,
                        "new_state": "LOADING",
                        "grid_id": car.current_grid_id
                    })
                else:
                    # Move to next grid in path
                    if car.path_index < len(car.current_path):
                        next_grid_id = car.current_path[car.path_index]
                        next_grid = self.grid_engine.get_grid(next_grid_id)
                        
                        if next_grid:
                            prev_grid = car.current_grid_id
                            car.move_to_next_grid(next_grid_id, next_grid.risk_score)
                            movements.append({
                                "car_id": car.id,
                                "from": prev_grid,
                                "to": next_grid_id,
                                "state": "MOVING_TO_DANGER"
                            })
                    else:
                        # Path complete, start loading
                        car.state = CarState.LOADING
            
            elif car.state == CarState.LOADING:
                # Pick up people
                danger_grid = self.grid_engine.get_grid(car.target_danger_grid)
                if danger_grid and danger_grid.population_density > 0:
                    pickup_count = car.pickup_people(danger_grid.population_density)
                    danger_grid.population_density -= pickup_count
                    
                    state_changes.append({
                        "car_id": car.id,
                        "action": "PICKED_UP",
                        "count": pickup_count,
                        "grid_id": car.current_grid_id
                    })
                
                # Start moving to safe zone
                path_to_safe = self.pathfinder.find_path(
                    car.current_grid_id,
                    car.target_safe_grid,
                    allow_danger_at_goal=False
                )
                
                if path_to_safe and path_to_safe["success"]:
                    car.current_path = path_to_safe["path_ids"]
                    car.path_index = 0
                    car.state = CarState.MOVING_TO_SAFE
                else:
                    # No path, go idle
                    car.state = CarState.IDLE
                    self.active_missions -= 1
            
            elif car.state == CarState.MOVING_TO_SAFE:
                if car.reached_destination():
                    # Arrived at safe zone
                    car.state = CarState.UNLOADING
                    state_changes.append({
                        "car_id": car.id,
                        "new_state": "UNLOADING",
                        "grid_id": car.current_grid_id
                    })
                else:
                    # Move to next grid in path
                    if car.path_index < len(car.current_path):
                        next_grid_id = car.current_path[car.path_index]
                        next_grid = self.grid_engine.get_grid(next_grid_id)
                        
                        if next_grid:
                            prev_grid = car.current_grid_id
                            car.move_to_next_grid(next_grid_id, next_grid.risk_score)
                            movements.append({
                                "car_id": car.id,
                                "from": prev_grid,
                                "to": next_grid_id,
                                "state": "MOVING_TO_SAFE"
                            })
                    else:
                        # Path complete, start unloading
                        car.state = CarState.UNLOADING
            
            elif car.state == CarState.UNLOADING:
                # Drop off people
                dropoff_count = car.dropoff_people()
                self.total_evacuated += dropoff_count
                
                state_changes.append({
                    "car_id": car.id,
                    "action": "DROPPED_OFF",
                    "count": dropoff_count,
                    "grid_id": car.current_grid_id
                })
                
                # Check if danger zone still has people
                danger_grid = self.grid_engine.get_grid(car.target_danger_grid)
                if danger_grid and danger_grid.population_density > 0:
                    # Assign same mission again
                    self.assign_mission(car.id, car.target_danger_grid)
                else:
                    # Mission complete
                    car.state = CarState.IDLE
                    car.target_danger_grid = None
                    car.target_safe_grid = None
                    self.active_missions -= 1
        
        return {
            "step": self.simulation_step,
            "movements": movements,
            "state_changes": state_changes,
            "total_evacuated": self.total_evacuated,
            "active_missions": self.active_missions,
            "cars": [car.to_dict() for car in self.cars.values()]
        }
    
    def _find_nearest_safe_zone(self, from_grid_id: str) -> Optional:
        """Find nearest safe evacuation point"""
        from_grid = self.grid_engine.get_grid(from_grid_id)
        if not from_grid:
            return None
        
        safe_zones = self.grid_engine.get_safe_zones()
        if not safe_zones:
            return None
        
        min_distance = float('inf')
        nearest = None
        
        for safe_zone in safe_zones:
            distance = abs(safe_zone.row - from_grid.row) + abs(safe_zone.col - from_grid.col)
            if distance < min_distance:
                min_distance = distance
                nearest = safe_zone
        
        return nearest
    
    def get_status(self) -> Dict:
        """Get current simulation status"""
        return {
            "step": self.simulation_step,
            "total_cars": len(self.cars),
            "active_missions": self.active_missions,
            "total_evacuated": self.total_evacuated,
            "cars": [car.to_dict() for car in self.cars.values()]
        }
    
    def reset(self):
        """Reset simulation"""
        for car in self.cars.values():
            car.state = CarState.IDLE
            car.passengers = 0
            car.total_evacuated = 0
            car.trips_completed = 0
            car.total_distance_traveled = 0
            car.total_risk_encountered = 0.0
        
        self.simulation_step = 0
        self.total_evacuated = 0
        self.active_missions = 0
