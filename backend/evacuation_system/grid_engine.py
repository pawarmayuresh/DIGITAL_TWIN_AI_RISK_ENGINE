"""
Grid Engine - Mumbai City Grid Management
Divides Mumbai into named grid zones with risk assessment
Uses real-time data from Mumbai sensors
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random

class SafetyLevel(Enum):
    SAFE = "SAFE"
    MEDIUM_RISK = "MEDIUM_RISK"
    DANGEROUS = "DANGEROUS"

@dataclass
class GridZone:
    """Represents a single grid zone in Mumbai"""
    id: str  # e.g., "A1", "B2"
    name: str  # e.g., "Colaba-North", "Bandra-West"
    row: int
    col: int
    latitude: float
    longitude: float
    risk_score: float  # 0.0 to 1.0
    population_density: int
    water_level: float  # meters
    rainfall: float  # mm/hour
    infrastructure_status: str  # "operational", "damaged", "blocked"
    safety_level: SafetyLevel
    is_evacuation_point: bool = False
    ward_id: str = ""  # Link to actual Mumbai ward
    
    def get_color(self) -> str:
        """Get color code for visualization"""
        if self.safety_level == SafetyLevel.SAFE:
            return "#10b981"  # Green
        elif self.safety_level == SafetyLevel.MEDIUM_RISK:
            return "#f59e0b"  # Yellow/Orange
        else:
            return "#ef4444"  # Red
    
    def is_passable(self) -> bool:
        """Check if grid can be traversed"""
        return (self.safety_level != SafetyLevel.DANGEROUS and 
                self.infrastructure_status != "blocked" and
                self.water_level < 1.5)
    
    def update_from_realtime_data(self, water_level: float, rainfall: float):
        """Update grid based on real-time sensor data"""
        self.water_level = water_level
        self.rainfall = rainfall
        
        # Recalculate risk score
        water_risk = min(1.0, water_level / 2.0)  # 2m = 100% risk
        rain_risk = min(1.0, rainfall / 100.0)  # 100mm/hr = 100% risk
        self.risk_score = (water_risk * 0.6 + rain_risk * 0.4)
        
        # Update safety level
        if self.risk_score < 0.4 and self.water_level < 0.5:
            self.safety_level = SafetyLevel.SAFE
        elif self.risk_score < 0.7:
            self.safety_level = SafetyLevel.MEDIUM_RISK
        else:
            self.safety_level = SafetyLevel.DANGEROUS
        
        # Update infrastructure status based on conditions
        if self.risk_score > 0.8:
            if random.random() < 0.3:
                self.infrastructure_status = "damaged"
            elif random.random() < 0.1:
                self.infrastructure_status = "blocked"

class MumbaiGridEngine:
    """Manages Mumbai city grid system with real-time updates"""
    
    def __init__(self, grid_rows: int = 20, grid_cols: int = 20):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.grids: Dict[str, GridZone] = {}
        self.grid_matrix = np.empty((grid_rows, grid_cols), dtype=object)
        
        # Mumbai bounds (approximate)
        self.lat_min, self.lat_max = 18.90, 19.27
        self.lon_min, self.lon_max = 72.77, 72.98
        
        self._initialize_grids()
    
    def _initialize_grids(self):
        """Initialize Mumbai grid zones with realistic data"""
        # Ward names for different areas
        ward_names = {
            (0, 0): "Colaba", (0, 1): "Fort", (0, 2): "Kalbadevi",
            (1, 0): "Girgaon", (1, 1): "Tardeo", (1, 2): "Byculla",
            (2, 0): "Worli", (2, 1): "Parel", (2, 2): "Sewri",
            (3, 0): "Mahim", (3, 1): "Dadar", (3, 2): "Matunga",
            (4, 0): "Bandra-W", (4, 1): "Bandra-E", (4, 2): "Kurla-W",
            (5, 0): "Khar", (5, 1): "Santacruz", (5, 2): "Kurla-E",
            (6, 0): "Juhu", (6, 1): "Vile Parle", (6, 2): "Ghatkopar-W",
            (7, 0): "Andheri-W", (7, 1): "Andheri-E", (7, 2): "Ghatkopar-E",
            (8, 0): "Versova", (8, 1): "Powai", (8, 2): "Vikhroli",
            (9, 0): "Goregaon-W", (9, 1): "Goregaon-E", (9, 2): "Bhandup",
            (10, 0): "Malad-W", (10, 1): "Malad-E", (10, 2): "Mulund-W",
            (11, 0): "Kandivali-W", (11, 1): "Kandivali-E", (11, 2): "Mulund-E",
            (12, 0): "Borivali-W", (12, 1): "Borivali-E", (12, 2): "Thane-W",
        }
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                grid_id = f"{chr(65 + row)}{col + 1}"  # A1, A2, B1, etc.
                
                # Get ward name or generate generic
                ward_key = (row // 2, col // 2)
                ward_name = ward_names.get(ward_key, f"Zone-{grid_id}")
                
                # Calculate lat/lon
                lat = self.lat_min + (row / self.grid_rows) * (self.lat_max - self.lat_min)
                lon = self.lon_min + (col / self.grid_cols) * (self.lon_max - self.lon_min)
                
                # Generate realistic risk data with better balance
                # Coastal areas (low row numbers) have higher flood risk
                coastal_risk = 0.6 if row < 3 else 0.25
                # Low-lying areas near Mithi River (middle columns)
                river_risk = 0.55 if 8 <= col <= 12 else 0.20
                base_risk = (coastal_risk + river_risk) / 2
                
                # Add controlled randomness for variety
                risk_score = min(1.0, max(0.1, base_risk + np.random.uniform(-0.1, 0.35)))
                
                # Population density (higher in central areas)
                pop_density = int(5000 + np.random.randint(-2000, 3000))
                if 3 <= row <= 8 and 3 <= col <= 8:  # Central Mumbai
                    pop_density += 3000
                
                # Water level and rainfall based on risk
                water_level = risk_score * np.random.uniform(0.3, 1.5)
                rainfall = risk_score * np.random.uniform(10, 80)
                
                # Infrastructure status
                infra_status = "operational"
                if risk_score > 0.75:
                    infra_status = np.random.choice(["operational", "damaged", "blocked"], 
                                                   p=[0.6, 0.3, 0.1])
                
                # Determine safety level with balanced thresholds
                if risk_score < 0.30 and water_level < 0.5:
                    safety = SafetyLevel.SAFE
                elif risk_score < 0.65:
                    safety = SafetyLevel.MEDIUM_RISK
                else:
                    safety = SafetyLevel.DANGEROUS
                
                # Ensure dangerous zones have significant population for evacuation
                if safety == SafetyLevel.DANGEROUS:
                    pop_density = max(pop_density, 800)  # Minimum 800 people in danger zones
                
                # Mark some safe zones as evacuation points
                is_evac_point = (safety == SafetyLevel.SAFE and 
                               np.random.random() < 0.15)
                
                grid = GridZone(
                    id=grid_id,
                    name=ward_name,
                    row=row,
                    col=col,
                    latitude=lat,
                    longitude=lon,
                    risk_score=risk_score,
                    population_density=pop_density,
                    water_level=water_level,
                    rainfall=rainfall,
                    infrastructure_status=infra_status,
                    safety_level=safety,
                    is_evacuation_point=is_evac_point
                )
                
                self.grids[grid_id] = grid
                self.grid_matrix[row, col] = grid
    
    def get_grid(self, grid_id: str) -> Optional[GridZone]:
        """Get grid by ID"""
        return self.grids.get(grid_id)
    
    def get_grid_by_position(self, row: int, col: int) -> Optional[GridZone]:
        """Get grid by row/col position"""
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            return self.grid_matrix[row, col]
        return None
    
    def get_neighbors(self, grid: GridZone) -> List[GridZone]:
        """Get neighboring grids (4-directional)"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            new_row, new_col = grid.row + dr, grid.col + dc
            neighbor = self.get_grid_by_position(new_row, new_col)
            if neighbor and neighbor.is_passable():
                neighbors.append(neighbor)
        
        return neighbors
    
    def get_all_neighbors(self, grid: GridZone) -> List[GridZone]:
        """Get ALL neighboring grids (4-directional) including dangerous ones"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            new_row, new_col = grid.row + dr, grid.col + dc
            neighbor = self.get_grid_by_position(new_row, new_col)
            if neighbor:
                neighbors.append(neighbor)
        
        return neighbors
    
    def get_safe_zones(self) -> List[GridZone]:
        """Get all safe grid zones"""
        return [g for g in self.grids.values() if g.safety_level == SafetyLevel.SAFE]
    
    def get_evacuation_points(self) -> List[GridZone]:
        """Get designated evacuation points"""
        return [g for g in self.grids.values() if g.is_evacuation_point]
    
    def get_dangerous_zones(self) -> List[GridZone]:
        """Get all dangerous grid zones"""
        return [g for g in self.grids.values() if g.safety_level == SafetyLevel.DANGEROUS]
    
    def update_grid_conditions(self, grid_id: str, **kwargs):
        """Update grid conditions dynamically"""
        grid = self.get_grid(grid_id)
        if grid:
            for key, value in kwargs.items():
                if hasattr(grid, key):
                    setattr(grid, key, value)
            
            # Recalculate safety level
            if grid.risk_score < 0.4 and grid.water_level < 0.5:
                grid.safety_level = SafetyLevel.SAFE
            elif grid.risk_score < 0.7:
                grid.safety_level = SafetyLevel.MEDIUM_RISK
            else:
                grid.safety_level = SafetyLevel.DANGEROUS
    
    def simulate_realtime_changes(self):
        """Simulate real-time changes in grid conditions"""
        import random
        
        for grid in self.grids.values():
            # Simulate water level changes
            water_change = random.uniform(-0.1, 0.15)
            grid.water_level = max(0, min(3.0, grid.water_level + water_change))
            
            # Simulate rainfall changes
            rain_change = random.uniform(-5, 10)
            grid.rainfall = max(0, min(150, grid.rainfall + rain_change))
            
            # Update risk based on new conditions
            grid.update_from_realtime_data(grid.water_level, grid.rainfall)
            
            # Randomly fix some infrastructure
            if grid.infrastructure_status == "damaged" and random.random() < 0.1:
                grid.infrastructure_status = "operational"
    
    def apply_ward_data(self, ward_data: Dict):
        """Apply real Mumbai ward data to grids"""
        # Map ward data to grids
        for grid in self.grids.values():
            if grid.ward_id in ward_data:
                data = ward_data[grid.ward_id]
                grid.water_level = data.get('water_level', grid.water_level)
                grid.rainfall = data.get('rainfall', grid.rainfall)
                grid.risk_score = data.get('risk_score', grid.risk_score)
                grid.update_from_realtime_data(grid.water_level, grid.rainfall)
    
    def to_dict(self) -> Dict:
        """Export grid data for API"""
        return {
            "grid_rows": self.grid_rows,
            "grid_cols": self.grid_cols,
            "grids": [
                {
                    "id": g.id,
                    "name": g.name,
                    "row": g.row,
                    "col": g.col,
                    "latitude": g.latitude,
                    "longitude": g.longitude,
                    "risk_score": g.risk_score,
                    "population_density": g.population_density,
                    "water_level": g.water_level,
                    "rainfall": g.rainfall,
                    "infrastructure_status": g.infrastructure_status,
                    "safety_level": g.safety_level.value,
                    "color": g.get_color(),
                    "is_evacuation_point": g.is_evacuation_point,
                    "is_passable": g.is_passable()
                }
                for g in self.grids.values()
            ]
        }
