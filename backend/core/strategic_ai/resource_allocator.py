"""
Resource Allocator - Optimal resource distribution for disaster response
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AllocationStrategy(Enum):
    """Resource allocation strategies"""
    PROPORTIONAL = "proportional"  # Proportional to need
    PRIORITY_BASED = "priority_based"  # Based on priority scores
    EQUAL = "equal"  # Equal distribution
    GREEDY = "greedy"  # Maximize immediate impact
    OPTIMAL = "optimal"  # Optimize overall outcome


@dataclass
class Resource:
    """Represents a resource"""
    resource_id: str
    name: str
    resource_type: str
    quantity: float
    unit: str
    cost_per_unit: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "quantity": self.quantity,
            "unit": self.unit,
            "cost_per_unit": self.cost_per_unit
        }


class ResourceAllocator:
    """
    Allocates resources optimally across disaster response needs.
    Supports multiple allocation strategies.
    """
    
    def __init__(self):
        self.available_resources: Dict[str, Resource] = {}
        self.allocations: List[Dict] = []
        
        # Initialize default resources
        self._initialize_default_resources()
    
    def _initialize_default_resources(self) -> None:
        """Initialize standard disaster response resources"""
        self.register_resource(Resource(
            resource_id="medical_supplies",
            name="Medical Supplies",
            resource_type="medical",
            quantity=10000,
            unit="units",
            cost_per_unit=50.0
        ))
        
        self.register_resource(Resource(
            resource_id="food_rations",
            name="Food Rations",
            resource_type="food",
            quantity=50000,
            unit="meals",
            cost_per_unit=5.0
        ))
        
        self.register_resource(Resource(
            resource_id="water_bottles",
            name="Water Bottles",
            resource_type="water",
            quantity=100000,
            unit="liters",
            cost_per_unit=1.0
        ))
        
        self.register_resource(Resource(
            resource_id="shelter_kits",
            name="Emergency Shelter Kits",
            resource_type="shelter",
            quantity=5000,
            unit="kits",
            cost_per_unit=200.0
        ))
        
        self.register_resource(Resource(
            resource_id="repair_crews",
            name="Repair Crews",
            resource_type="labor",
            quantity=100,
            unit="crews",
            cost_per_unit=5000.0
        ))
    
    def register_resource(self, resource: Resource) -> None:
        """Register a new resource"""
        self.available_resources[resource.resource_id] = resource
    
    def allocate_resources(
        self,
        demands: Dict[str, Dict],
        strategy: AllocationStrategy = AllocationStrategy.PROPORTIONAL
    ) -> Dict:
        """
        Allocate resources based on demands and strategy.
        
        Args:
            demands: Dict mapping location/need to resource requirements
                    Format: {location: {resource_id: {quantity, priority}}}
            strategy: Allocation strategy to use
        
        Returns:
            Allocation plan
        """
        if strategy == AllocationStrategy.PROPORTIONAL:
            return self._allocate_proportional(demands)
        elif strategy == AllocationStrategy.PRIORITY_BASED:
            return self._allocate_priority(demands)
        elif strategy == AllocationStrategy.EQUAL:
            return self._allocate_equal(demands)
        elif strategy == AllocationStrategy.GREEDY:
            return self._allocate_greedy(demands)
        else:
            return self._allocate_optimal(demands)
    
    def _allocate_proportional(self, demands: Dict[str, Dict]) -> Dict:
        """Allocate proportionally to demand"""
        allocations = {}
        
        for resource_id, resource in self.available_resources.items():
            # Calculate total demand for this resource
            total_demand = sum(
                location_demands.get(resource_id, {}).get("quantity", 0)
                for location_demands in demands.values()
            )
            
            if total_demand == 0:
                continue
            
            # Allocate proportionally
            for location, location_demands in demands.items():
                if resource_id in location_demands:
                    demand = location_demands[resource_id]["quantity"]
                    proportion = demand / total_demand
                    allocated = min(resource.quantity * proportion, demand)
                    
                    if location not in allocations:
                        allocations[location] = {}
                    
                    allocations[location][resource_id] = {
                        "allocated": allocated,
                        "requested": demand,
                        "fulfillment_rate": allocated / demand if demand > 0 else 1.0
                    }
        
        return {
            "strategy": "proportional",
            "allocations": allocations,
            "total_locations": len(allocations)
        }
    
    def _allocate_priority(self, demands: Dict[str, Dict]) -> Dict:
        """Allocate based on priority scores"""
        allocations = {}
        
        # Sort locations by priority
        sorted_locations = sorted(
            demands.items(),
            key=lambda x: x[1].get("priority", 0),
            reverse=True
        )
        
        # Track remaining resources
        remaining = {
            rid: res.quantity
            for rid, res in self.available_resources.items()
        }
        
        # Allocate in priority order
        for location, location_demands in sorted_locations:
            allocations[location] = {}
            
            for resource_id, demand_info in location_demands.items():
                if resource_id == "priority":
                    continue
                
                demand = demand_info.get("quantity", 0)
                available = remaining.get(resource_id, 0)
                allocated = min(demand, available)
                
                allocations[location][resource_id] = {
                    "allocated": allocated,
                    "requested": demand,
                    "fulfillment_rate": allocated / demand if demand > 0 else 1.0
                }
                
                remaining[resource_id] = available - allocated
        
        return {
            "strategy": "priority_based",
            "allocations": allocations,
            "remaining_resources": remaining
        }
    
    def _allocate_equal(self, demands: Dict[str, Dict]) -> Dict:
        """Allocate equally across all locations"""
        allocations = {}
        num_locations = len(demands)
        
        if num_locations == 0:
            return {"strategy": "equal", "allocations": {}}
        
        for resource_id, resource in self.available_resources.items():
            per_location = resource.quantity / num_locations
            
            for location in demands:
                if location not in allocations:
                    allocations[location] = {}
                
                allocations[location][resource_id] = {
                    "allocated": per_location,
                    "equal_share": True
                }
        
        return {
            "strategy": "equal",
            "allocations": allocations
        }
    
    def _allocate_greedy(self, demands: Dict[str, Dict]) -> Dict:
        """Greedy allocation to maximize immediate impact"""
        # Similar to priority but considers impact per resource unit
        return self._allocate_priority(demands)
    
    def _allocate_optimal(self, demands: Dict[str, Dict]) -> Dict:
        """Optimal allocation (simplified linear programming)"""
        # For now, use priority-based as approximation
        # In production, would use actual LP solver
        return self._allocate_priority(demands)
    
    def calculate_resource_gap(self, demands: Dict[str, Dict]) -> Dict:
        """Calculate gap between demand and available resources"""
        gaps = {}
        
        for resource_id, resource in self.available_resources.items():
            total_demand = sum(
                location_demands.get(resource_id, {}).get("quantity", 0)
                for location_demands in demands.values()
            )
            
            gap = total_demand - resource.quantity
            
            gaps[resource_id] = {
                "resource_name": resource.name,
                "available": resource.quantity,
                "demanded": total_demand,
                "gap": max(0, gap),
                "surplus": max(0, -gap),
                "fulfillment_rate": min(1.0, resource.quantity / total_demand) if total_demand > 0 else 1.0
            }
        
        return gaps
    
    def get_available_resources(self) -> List[Dict]:
        """Get all available resources"""
        return [res.to_dict() for res in self.available_resources.values()]
