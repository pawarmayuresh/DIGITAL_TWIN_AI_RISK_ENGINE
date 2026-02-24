"""
Recovery Model — Temporal repair and restoration of infrastructure.

Implements:
- Repair prioritization (critical nodes first)
- Resource allocation curves (recovery speed dependent on available resources)
- Repair timeline modeling (how long different component types take)
- Recovery acceleration strategies (backup systems, parallel repairs)
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RepairPriority(Enum):
    """Repair priority levels."""
    CRITICAL = 1     # Must repair immediately (hospitals, power plants)
    HIGH = 2         # Essential services (water treatment, transport)
    MEDIUM = 3       # Important (backup systems, communications)
    LOW = 4          # Nice to have (secondary networks)


@dataclass
class RepairAllocation:
    """Tracks repair resource allocation."""
    total_repair_capacity: float  # Fraction of infrastructure that can be repaired per tick
    available_resources: float    # Current available repair workforce/materials (0-1)
    repair_speed: float           # Base repair rate (0-1 capacity recovery per tick)


class RecoveryModel:
    """
    Models infrastructure recovery and repair prioritization.
    
    Key Features:
    - Priority-based repair queuing
    - Resource-constrained recovery (not everything can be fixed at once)
    - Temporal modeling (different repair times for different components)
    - Recovery acceleration (backup systems, parallel teams)
    """
    
    # Default repair times (in ticks) by infrastructure type
    DEFAULT_REPAIR_TIMES = {
        "power_plant": 40,
        "substation": 20,
        "water_treatment": 30,
        "water_pump": 15,
        "hospital": 50,
        "transport_hub": 25,
        "data_center": 35,
        "backup_generator": 10,
    }
    
    # Default criticality of each type (used for repair prioritization)
    DEFAULT_CRITICALITIES = {
        "power_plant": 1.0,
        "substation": 0.95,
        "water_treatment": 0.9,
        "water_pump": 0.8,
        "hospital": 0.95,
        "transport_hub": 0.7,
        "data_center": 0.85,
        "backup_generator": 0.6,
    }
    
    def __init__(
        self,
        infra_graph,
        repair_capacity_per_tick: float = 0.05,  # 5% of infrastructure per tick
        available_resources: float = 1.0,  # Start fully resourced
    ):
        self.infra_graph = infra_graph
        self.repair_allocation = RepairAllocation(
            total_repair_capacity=repair_capacity_per_tick,
            available_resources=available_resources,
            repair_speed=0.02,  # 2% recovery per tick
        )
        self.repair_queue: List[str] = []
        self.repair_history: List[Dict] = []
        self._current_tick: int = 0
    
    # ================================================================ #
    # Priority calculation
    # ================================================================ #
    
    def calculate_repair_priority(self, node_id: str) -> float:
        """
        Score for repair priority (higher = should repair first).
        
        Factors:
        - Node criticality
        - Damage severity
        - Number of dependent nodes
        """
        node = self.infra_graph._nodes.get(node_id)
        if not node:
            return 0.0
        
        # Criticality of the node type
        crit_score = node.criticality
        
        # Damage severity (how bad the damage)
        damage_score = node.damage_accumulated
        
        # Dependency importance (how many others depend on this)
        dependents = self.infra_graph.get_dependents(node_id)
        dependency_score = len(dependents) * 0.1
        
        # Combined priority
        return (crit_score * 0.5) + (damage_score * 0.3) + dependency_score
    
    def rebuild_repair_queue(self) -> List[str]:
        """Rebuild repair queue based on current priorities."""
        # Only repair failed/degraded nodes
        candidates = []
        for node in self.infra_graph._nodes.values():
            if node.capacity < 0.95 and node.damage_accumulated > 0:
                candidates.append((node.node_id, self.calculate_repair_priority(node.node_id)))
        
        # Sort by priority (highest first)
        sorted_queue = sorted(candidates, key=lambda x: x[1], reverse=True)
        self.repair_queue = [node_id for node_id, _ in sorted_queue]
        return self.repair_queue
    
    # ================================================================ #
    # Recovery execution
    # ================================================================ #
    
    def apply_repairs(self, tick: int) -> Dict[str, any]:
        """
        Apply repairs to infrastructure in priority order.
        
        Returns:
            {
                "nodes_repaired": int,
                "total_capacity_restored": float,
                "repairs_applied": [{node_id, repair_amount}, ...]
            }
        """
        self._current_tick = tick
        
        # Rebuild queue based on current state
        self.rebuild_repair_queue()
        
        repairs_applied = []
        total_capacity_restored = 0.0
        available_repair_budget = (
            self.repair_allocation.total_repair_capacity * 
            self.repair_allocation.available_resources
        )
        
        for node_id in self.repair_queue:
            if available_repair_budget <= 0:
                break
            
            node = self.infra_graph._nodes.get(node_id)
            if not node or node.capacity >= 0.95:
                continue
            
            # Calculate repair amount for this node
            remaining_damage = node.damage_accumulated
            repair_amount = min(
                self.repair_allocation.repair_speed * self.repair_allocation.available_resources,
                remaining_damage,
                available_repair_budget
            )
            
            # Apply repair
            node.repair(repair_amount)
            available_repair_budget -= repair_amount
            total_capacity_restored += repair_amount
            
            repairs_applied.append({
                "node_id": node_id,
                "repair_amount": round(repair_amount, 3),
                "new_capacity": round(node.capacity, 3),
            })
        
        result = {
            "nodes_repaired": len(repairs_applied),
            "total_capacity_restored": round(total_capacity_restored, 3),
            "repairs_applied": repairs_applied,
            "queue_length": len(self.repair_queue),
        }
        
        self.repair_history.append(result)
        return result
    
    def set_resource_availability(self, availability: float, tick: int) -> None:
        """
        Update available repair resources (0-1).
        
        0.0 = no repairs possible
        1.0 = full repair capacity available
        """
        self.repair_allocation.available_resources = max(0.0, min(1.0, availability))
    
    def accelerate_recovery(self, speed_multiplier: float = 1.5) -> None:
        """
        Temporarily boost recovery speed (e.g., emergency response, military aide).
        """
        self.repair_allocation.repair_speed *= speed_multiplier
    
    def activate_backup_systems(self, node_id: str) -> float:
        """
        Deploy backup system for a critical node.
        Returns immediate capacity restoration.
        """
        node = self.infra_graph._nodes.get(node_id)
        if not node:
            return 0.0
        
        # Backup provides 30-50% immediate restoration
        restoration = min(0.5, node.damage_accumulated * 0.3)
        node.repair(restoration)
        
        return restoration
    
    # ================================================================ #
    # Recovery analysis
    # ================================================================ #
    
    def estimated_recovery_time(self, node_id: str) -> int:
        """Estimate ticks until a node is fully repaired."""
        node = self.infra_graph._nodes.get(node_id)
        if not node or node.capacity >= 0.95:
            return 0
        
        remaining_damage = node.damage_accumulated
        if self.repair_allocation.repair_speed <= 0:
            return float('inf')
        
        available_repair_rate = (
            self.repair_allocation.repair_speed * 
            self.repair_allocation.available_resources
        )
        if available_repair_rate <= 0:
            return float('inf')
        
        return int(remaining_damage / available_repair_rate)
    
    def system_recovery_trajectory(self) -> Dict:
        """Model expected recovery over next N ticks."""
        trajectory = {
            "current_health": round(self.infra_graph.system_health(), 3),
            "current_failed": len(self.infra_graph.get_failed_nodes()),
            "damaged_queue_length": len(self.repair_queue),
            "available_resources": round(self.repair_allocation.available_resources, 3),
            "repair_speed": round(self.repair_allocation.repair_speed, 3),
        }
        return trajectory
    
    def recovery_summary(self) -> Dict:
        """Comprehensive recovery state summary."""
        return {
            "total_repairs": len(self.repair_history),
            "total_capacity_restored": round(
                sum(r.get("total_capacity_restored", 0) for r in self.repair_history), 3
            ),
            "nodes_in_queue": len(self.repair_queue),
            "available_resources": round(self.repair_allocation.available_resources, 3),
            "repair_speed": round(self.repair_allocation.repair_speed, 3),
            "system_health": round(self.infra_graph.system_health(), 3),
        }
