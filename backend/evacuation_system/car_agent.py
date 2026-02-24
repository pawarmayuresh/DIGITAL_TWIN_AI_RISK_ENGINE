"""
Car Agent - Vehicle-based evacuation with state machine
Moves on grid, picks up people from danger zones, drops at safe zones
"""
from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

class CarState(Enum):
    IDLE = "IDLE"
    MOVING_TO_DANGER = "MOVING_TO_DANGER"
    LOADING = "LOADING"
    MOVING_TO_SAFE = "MOVING_TO_SAFE"
    UNLOADING = "UNLOADING"

@dataclass
class CarAgent:
    """Represents an evacuation vehicle"""
    id: str
    name: str
    capacity: int = 50  # Max people per trip
    current_grid_id: str = "A1"  # Starting position
    state: CarState = CarState.IDLE
    passengers: int = 0
    total_evacuated: int = 0
    trips_completed: int = 0
    
    # Current mission
    target_danger_grid: Optional[str] = None
    target_safe_grid: Optional[str] = None
    current_path: List[str] = field(default_factory=list)
    path_index: int = 0
    
    # Statistics
    total_distance_traveled: int = 0
    total_risk_encountered: float = 0.0
    
    def get_position(self) -> Dict:
        """Get current position info"""
        return {
            "grid_id": self.current_grid_id,
            "state": self.state.value,
            "passengers": self.passengers,
            "capacity": self.capacity,
            "total_evacuated": self.total_evacuated,
            "trips": self.trips_completed
        }
    
    def can_pickup(self) -> bool:
        """Check if car can pick up more people"""
        return self.passengers < self.capacity
    
    def pickup_people(self, count: int) -> int:
        """Pick up people, return actual count picked up"""
        available_space = self.capacity - self.passengers
        actual_pickup = min(count, available_space)
        self.passengers += actual_pickup
        return actual_pickup
    
    def dropoff_people(self) -> int:
        """Drop off all passengers"""
        count = self.passengers
        self.total_evacuated += count
        self.passengers = 0
        self.trips_completed += 1
        return count
    
    def move_to_next_grid(self, grid_id: str, risk_score: float):
        """Move car to next grid in path"""
        self.current_grid_id = grid_id
        self.path_index += 1
        self.total_distance_traveled += 1
        self.total_risk_encountered += risk_score
    
    def set_mission(self, danger_grid: str, safe_grid: str, path_to_danger: List[str], path_to_safe: List[str]):
        """Set new evacuation mission"""
        self.target_danger_grid = danger_grid
        self.target_safe_grid = safe_grid
        self.current_path = path_to_danger
        self.path_index = 0
        self.state = CarState.MOVING_TO_DANGER
    
    def reached_destination(self) -> bool:
        """Check if car reached current destination"""
        if not self.current_path or len(self.current_path) == 0:
            return True
        # Car has reached destination if it's at the last grid in the path
        return self.current_grid_id == self.current_path[-1]
    
    def to_dict(self) -> Dict:
        """Export car data"""
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "current_grid_id": self.current_grid_id,
            "state": self.state.value,
            "passengers": self.passengers,
            "total_evacuated": self.total_evacuated,
            "trips_completed": self.trips_completed,
            "target_danger_grid": self.target_danger_grid,
            "target_safe_grid": self.target_safe_grid,
            "total_distance": self.total_distance_traveled,
            "total_risk": round(self.total_risk_encountered, 2),
            "progress": (self.path_index / len(self.current_path) * 100) if self.current_path else 0
        }
