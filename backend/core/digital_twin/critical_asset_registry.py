"""
Critical Asset Registry - Track hospitals, schools, utilities, emergency services
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


class AssetType(Enum):
    """Critical asset types"""
    HOSPITAL = "hospital"
    SCHOOL = "school"
    FIRE_STATION = "fire_station"
    POLICE_STATION = "police_station"
    WATER_TREATMENT = "water_treatment"
    POWER_PLANT = "power_plant"
    SHELTER = "shelter"
    FOOD_DISTRIBUTION = "food_distribution"
    EMERGENCY_CENTER = "emergency_center"


@dataclass
class CriticalAsset:
    """Represents a critical infrastructure asset"""
    asset_id: str
    asset_type: AssetType
    name: str
    location: Tuple[int, int]  # Grid coordinates (x, y)
    capacity: int  # Capacity (beds, students, etc.)
    operational_status: float = 1.0  # 0.0 to 1.0
    dependencies: List[str] = None  # Infrastructure node IDs
    service_radius_km: float = 5.0
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
    
    def is_operational(self) -> bool:
        """Check if asset is operational (>50% status)"""
        return self.operational_status > 0.5
    
    def degrade(self, amount: float) -> None:
        """Degrade asset operational status"""
        self.operational_status = max(0.0, self.operational_status - amount)
    
    def repair(self, amount: float) -> None:
        """Repair asset operational status"""
        self.operational_status = min(1.0, self.operational_status + amount)
    
    def to_dict(self) -> Dict:
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type.value,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity,
            "operational_status": self.operational_status,
            "is_operational": self.is_operational(),
            "dependencies": self.dependencies,
            "service_radius_km": self.service_radius_km
        }


class CriticalAssetRegistry:
    """
    Registry for managing critical infrastructure assets.
    Tracks hospitals, schools, emergency services, and utilities.
    """
    
    def __init__(self):
        self.assets: Dict[str, CriticalAsset] = {}
        self._assets_by_type: Dict[AssetType, List[str]] = {
            asset_type: [] for asset_type in AssetType
        }
    
    def register_asset(self, asset: CriticalAsset) -> None:
        """Register a new critical asset"""
        self.assets[asset.asset_id] = asset
        
        # Index by type
        if asset.asset_type not in self._assets_by_type:
            self._assets_by_type[asset.asset_type] = []
        self._assets_by_type[asset.asset_type].append(asset.asset_id)
    
    def get_asset(self, asset_id: str) -> Optional[CriticalAsset]:
        """Get asset by ID"""
        return self.assets.get(asset_id)
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[CriticalAsset]:
        """Get all assets of a specific type"""
        asset_ids = self._assets_by_type.get(asset_type, [])
        return [self.assets[aid] for aid in asset_ids if aid in self.assets]
    
    def get_assets_in_radius(
        self,
        location: Tuple[int, int],
        radius_km: float
    ) -> List[CriticalAsset]:
        """Get all assets within radius of location"""
        assets_in_radius = []
        
        for asset in self.assets.values():
            distance = self._calculate_distance(location, asset.location)
            if distance <= radius_km:
                assets_in_radius.append(asset)
        
        return assets_in_radius
    
    def _calculate_distance(
        self,
        loc1: Tuple[int, int],
        loc2: Tuple[int, int]
    ) -> float:
        """Calculate Euclidean distance between two locations"""
        dx = loc2[0] - loc1[0]
        dy = loc2[1] - loc1[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def update_asset_status(self, infrastructure_graph) -> None:
        """Update asset operational status based on infrastructure dependencies"""
        if not infrastructure_graph:
            return
        
        for asset in self.assets.values():
            if not asset.dependencies:
                continue
            
            # Calculate average health of dependencies
            total_health = 0.0
            valid_deps = 0
            
            for dep_id in asset.dependencies:
                if dep_id in infrastructure_graph.nodes:
                    node = infrastructure_graph.nodes[dep_id]
                    total_health += node.capacity
                    valid_deps += 1
            
            if valid_deps > 0:
                avg_health = total_health / valid_deps
                # Asset status follows infrastructure health
                asset.operational_status = avg_health
    
    def calculate_service_coverage(self, grid_manager) -> Dict:
        """Calculate service coverage across the grid"""
        if not grid_manager:
            return {}
        
        coverage_by_type = {}
        
        for asset_type in AssetType:
            assets = self.get_assets_by_type(asset_type)
            if not assets:
                coverage_by_type[asset_type.value] = {
                    "total_assets": 0,
                    "operational_assets": 0,
                    "coverage_percentage": 0.0
                }
                continue
            
            operational_assets = [a for a in assets if a.is_operational()]
            
            # Calculate coverage (simplified: based on service radius)
            total_cells = len(grid_manager.cells)
            covered_cells = set()
            
            for asset in operational_assets:
                # Find cells within service radius
                for cell in grid_manager.cells.values():
                    cell_loc = (cell.metadata.x, cell.metadata.y)
                    distance = self._calculate_distance(asset.location, cell_loc)
                    if distance <= asset.service_radius_km:
                        covered_cells.add((cell.metadata.x, cell.metadata.y))
            
            coverage_pct = len(covered_cells) / total_cells if total_cells > 0 else 0.0
            
            coverage_by_type[asset_type.value] = {
                "total_assets": len(assets),
                "operational_assets": len(operational_assets),
                "coverage_percentage": coverage_pct * 100,
                "total_capacity": sum(a.capacity for a in assets),
                "operational_capacity": sum(a.capacity for a in operational_assets)
            }
        
        return coverage_by_type
    
    def get_operational_summary(self) -> Dict:
        """Get summary of operational status"""
        summary = {
            "total_assets": len(self.assets),
            "operational_assets": sum(1 for a in self.assets.values() if a.is_operational()),
            "by_type": {}
        }
        
        for asset_type in AssetType:
            assets = self.get_assets_by_type(asset_type)
            operational = [a for a in assets if a.is_operational()]
            
            summary["by_type"][asset_type.value] = {
                "total": len(assets),
                "operational": len(operational),
                "operational_percentage": (
                    len(operational) / len(assets) * 100 if assets else 0.0
                )
            }
        
        return summary
    
    def get_critical_failures(self) -> List[CriticalAsset]:
        """Get list of critical assets that have failed"""
        return [
            asset for asset in self.assets.values()
            if not asset.is_operational()
        ]
    
    def initialize_default_assets(self, grid_width: int, grid_height: int) -> None:
        """Initialize default critical assets for a city"""
        # Hospitals
        for i in range(3):
            x = int(grid_width * (0.25 + i * 0.25))
            y = int(grid_height * 0.5)
            self.register_asset(CriticalAsset(
                asset_id=f"hospital_{i+1:03d}",
                asset_type=AssetType.HOSPITAL,
                name=f"Hospital #{i+1}",
                location=(x, y),
                capacity=500,
                dependencies=["power_node_1", "water_node_1"],
                service_radius_km=5.0
            ))
        
        # Fire Stations
        for i in range(4):
            x = int(grid_width * (0.2 + i * 0.2))
            y = int(grid_height * (0.3 if i % 2 == 0 else 0.7))
            self.register_asset(CriticalAsset(
                asset_id=f"fire_{i+1:03d}",
                asset_type=AssetType.FIRE_STATION,
                name=f"Fire Station #{i+1}",
                location=(x, y),
                capacity=20,
                dependencies=["power_node_1", "telecom_node_1"],
                service_radius_km=3.0
            ))
        
        # Schools
        for i in range(10):
            x = int(grid_width * ((i % 5) * 0.2 + 0.1))
            y = int(grid_height * (0.3 if i < 5 else 0.7))
            self.register_asset(CriticalAsset(
                asset_id=f"school_{i+1:03d}",
                asset_type=AssetType.SCHOOL,
                name=f"School #{i+1}",
                location=(x, y),
                capacity=1000,
                dependencies=["power_node_1"],
                service_radius_km=2.0
            ))
        
        # Emergency Shelters
        for i in range(5):
            x = int(grid_width * (0.1 + i * 0.2))
            y = int(grid_height * 0.5)
            self.register_asset(CriticalAsset(
                asset_id=f"shelter_{i+1:03d}",
                asset_type=AssetType.SHELTER,
                name=f"Emergency Shelter #{i+1}",
                location=(x, y),
                capacity=2000,
                dependencies=["power_node_1", "water_node_1"],
                service_radius_km=4.0
            ))
    
    def export_assets(self) -> List[Dict]:
        """Export all assets as list of dictionaries"""
        return [asset.to_dict() for asset in self.assets.values()]
