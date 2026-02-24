"""
Disaster-Cascade Integration — Connect Batch 3 disasters to Batch 4 cascades.

Bridges spatial disaster impacts and infrastructure network failures:
- Converts disaster damage (grid cells) → infrastructure graph failures
- Propagates cascades → back to grid cells
- Models realistic infrastructure collapse within disaster context
- Enables feedback loops (cascade severity influences disaster outcomes)
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
import sys
from pathlib import Path

# Import disaster engine
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from disaster_engine import DisasterManager, DisasterType
from cascading_engine import (
    InfrastructureGraph,
    InfrastructureNodeType,
    CascadingFailureEngine,
    RecoveryModel,
    StabilityCalculator,
)
from spatial_engine import GridCell, GridManager


class DisasterCascadeIntegrator:
    """
    Orchestrates interaction between disaster simulation and infrastructure cascades.
    
    Workflow:
    1. Disaster occurs on spatial grid (Batch 3)
    2. Disaster impacts map to infrastructure nodes
    3. Cascading failure engine propagates through network (Batch 4)
    4. Failed infrastructure degrades grid cells further
    5. Stability metrics feedback to disaster evolution
    """
    
    def __init__(
        self,
        infra_graph: InfrastructureGraph,
        disaster_manager: DisasterManager,
        grid: GridManager,
    ):
        self.infra_graph = infra_graph
        self.disaster_manager = disaster_manager
        self.grid = grid
        
        # Cascade components
        self.cascade_engine = CascadingFailureEngine(infra_graph, threshold=0.3)
        self.recovery_model = RecoveryModel(infra_graph, repair_capacity_per_tick=0.08)
        self.stability_calc = StabilityCalculator(infra_graph, self.cascade_engine)
        
        # Integration state
        self.coupling_factor = 0.6  # How much cascade severity affects grid (0-1)
        self.integration_log: List[Dict] = []
    
    # ================================================================ #
    # Disaster → Infrastructure Mapping
    # ================================================================ #
    
    def map_disaster_damage_to_infrastructure(
        self,
        disaster_type: DisasterType,
        affected_cells: List[Tuple[int, int]],
        severity: float,
        tick: int,
    ) -> Dict[str, float]:
        """
        Convert spatial disaster damage to infrastructure node failures.
        
        Logic:
        - Count affected cells in each zone/region
        - Map regional damage to nearby infrastructure nodes
        - Scale damage by disaster type (earthquakes hit everything, fires hit power lines, etc.)
        
        Args:
            disaster_type: Type of disaster (flood, earthquake, etc.)
            affected_cells: List of (x, y) grid coordinates damaged
            severity: 0-1 disaster severity
            tick: Simulation tick
        
        Returns:
            {node_id: damage_amount, ...} ready for cascade engine
        """
        infrastructure_damage = {}
        
        # Disaster-specific vulnerability multipliers
        vulnerability_by_type = {
            DisasterType.EARTHQUAKE: {
                InfrastructureNodeType.SUBSTATION: 0.9,
                InfrastructureNodeType.WATER_TREATMENT: 0.8,
                InfrastructureNodeType.HOSPITAL: 0.7,
                InfrastructureNodeType.POWER_PLANT: 0.95,
                InfrastructureNodeType.TRANSPORT_HUB: 0.6,
            },
            DisasterType.FLOOD: {
                InfrastructureNodeType.POWER_PLANT: 0.3,
                InfrastructureNodeType.SUBSTATION: 0.4,
                InfrastructureNodeType.WATER_TREATMENT: 0.95,
                InfrastructureNodeType.WATER_PUMP: 0.9,
                InfrastructureNodeType.TRANSPORT_HUB: 0.8,
            },
            DisasterType.WILDFIRE: {
                InfrastructureNodeType.POWER_PLANT: 0.2,
                InfrastructureNodeType.SUBSTATION: 0.85,
                InfrastructureNodeType.TRANSPORT_HUB: 0.8,
                InfrastructureNodeType.DATA_CENTER: 0.6,
            },
            DisasterType.PANDEMIC: {
                InfrastructureNodeType.HOSPITAL: 0.3,
                InfrastructureNodeType.DATA_CENTER: 0.1,
                InfrastructureNodeType.TRANSPORT_HUB: 0.2,
            },
            DisasterType.CYBER_ATTACK: {
                InfrastructureNodeType.DATA_CENTER: 0.95,
                InfrastructureNodeType.SUBSTATION: 0.3,
                InfrastructureNodeType.HOSPITAL: 0.4,
                InfrastructureNodeType.TRANSPORT_HUB: 0.5,
            },
        }
        
        vulns = vulnerability_by_type.get(disaster_type, {})
        
        # Map each affected grid cell to nearby infrastructure
        for x, y in affected_cells:
            # Find nodes within proximity to this cell
            for node in self.infra_graph.get_all_nodes():
                node_x, node_y = node.location
                distance = ((x - node_x) ** 2 + (y - node_y) ** 2) ** 0.5
                
                # Damage attenuates with distance
                if distance < 5.0:  # Within 5 km
                    # Distance-based attenuation
                    distance_factor = max(0.0, 1.0 - (distance / 5.0))
                    
                    # Type-based vulnerability
                    vuln = vulns.get(node.node_type, 0.3)
                    
                    # Total damage
                    damage = severity * distance_factor * vuln
                    
                    if node.node_id in infrastructure_damage:
                        infrastructure_damage[node.node_id] = min(
                            1.0, 
                            infrastructure_damage[node.node_id] + damage
                        )
                    else:
                        infrastructure_damage[node.node_id] = damage
        
        return {k: v for k, v in infrastructure_damage.items() if v > 0.05}
    
    # ================================================================ #
    # Cascade → Grid Feedback
    # ================================================================ #
    
    def apply_cascade_impacts_to_grid(
        self,
        cascade_result: Dict,
        tick: int,
    ) -> Dict[str, any]:
        """
        Feed cascade failures back into spatial grid.
        
        Failed infrastructure degrades cells in its zone:
        - No water → cells lose healthcare, population stress
        - No power → cells lose critical services
        - Transport disrupted → goods distribution fails
        
        Returns:
            Impact summary
        """
        grid_impacts = {
            "cells_affected": 0,
            "population_stressed": 0,
            "infrastructure_degraded": 0,
        }
        
        failed_nodes = cascade_result.get("failed", [])
        degraded_nodes = cascade_result.get("degraded", [])
        
        # For each failed infrastructure node, degrade nearby grid cells
        for node_id in failed_nodes + degraded_nodes:
            node = self.infra_graph._nodes.get(node_id)
            if not node:
                continue
            
            node_x, node_y = node.location
            node_type = node.node_type
            
            # Determine impact radius and severity based on node type
            radius = 8.0 if node_type == InfrastructureNodeType.POWER_PLANT else 5.0
            severity_factor = 0.7 if node_id in failed_nodes else 0.4
            
            # Apply impact to cells in radius
            for cell in self.grid.get_all_cells():
                cell_x, cell_y = cell.metadata.x, cell.metadata.y
                distance = ((cell_x - node_x) ** 2 + (cell_y - node_y) ** 2) ** 0.5
                
                if distance < radius:
                    impact = severity_factor * (1.0 - distance / radius)
                    
                    # Degrade infrastructure health based on failed service
                    if node_type == InfrastructureNodeType.POWER_PLANT:
                        cell.power_grid_health = max(
                            0.0, cell.power_grid_health - impact * 0.3
                        )
                    elif node_type == InfrastructureNodeType.WATER_TREATMENT:
                        cell.water_network_health = max(
                            0.0, cell.water_network_health - impact * 0.3
                        )
                    elif node_type == InfrastructureNodeType.HOSPITAL:
                        cell.healthcare_capacity = max(
                            0.0, cell.healthcare_capacity - impact * 0.3
                        )
                    elif node_type == InfrastructureNodeType.TRANSPORT_HUB:
                        cell.transport_network_health = max(
                            0.0, cell.transport_network_health - impact * 0.2
                        )
                    
                    grid_impacts["cells_affected"] += 1
                    if hasattr(cell.metadata, "population_density"):
                        grid_impacts["population_stressed"] += int(
                            cell.metadata.population_density * impact
                        )
        
        return grid_impacts
    
    # ================================================================ #
    # Integrated simulation step
    # ================================================================ #
    
    def simulate_integrated_tick(
        self,
        tick: int,
        disaster_events: List[Tuple[DisasterType, List[Tuple[int, int]], float]] = None,
    ) -> Dict:
        """
        Execute single integrated simulation tick.
        
        Order:
        1. Apply disaster spatial impacts
        2. Map to infrastructure damage
        3. Propagate cascades
        4. Feed back to grid
        5. Apply recovery
        6. Calculate overall stability
        
        Args:
            tick: Current simulation tick
            disaster_events: [(type, affected_cells, severity), ...]
        
        Returns:
            Comprehensive simulation state
        """
        disaster_events = disaster_events or []
        
        # Step 1: Disasters damage infrastructure
        all_infrastructure_damage = {}
        for disaster_type, affected_cells, severity in disaster_events:
            damage = self.map_disaster_damage_to_infrastructure(
                disaster_type, affected_cells, severity, tick
            )
            for node_id, dmg in damage.items():
                all_infrastructure_damage[node_id] = max(
                    all_infrastructure_damage.get(node_id, 0), dmg
                )
        
        # Step 2: Propagate cascades
        cascade_result = {}
        if all_infrastructure_damage:
            cascade_result = self.cascade_engine.propagate_failures(
                all_infrastructure_damage, tick
            )
        
        # Step 3: Feed cascades back to grid
        grid_impacts = self.apply_cascade_impacts_to_grid(cascade_result, tick)
        
        # Step 4: Apply recovery
        recovery_result = self.recovery_model.apply_repairs(tick)
        
        # Step 5: Calculate stability
        cascade_summary = self.cascade_engine.cascade_summary()
        stability = self.stability_calc.system_stability_index()
        resilience = self.stability_calc.resilience_score()
        
        # Compile result
        result = {
            "tick": tick,
            "disasters_triggered": len(disaster_events),
            "infrastructure_damage_points": len(all_infrastructure_damage),
            "cascade": cascade_result,
            "grid_impacts": grid_impacts,
            "recovery": recovery_result,
            "system_health": {
                "stability": round(stability, 3),
                "resilience": round(resilience, 3),
                "failed_nodes": cascade_summary["failed_nodes"],
                "degraded_nodes": cascade_summary["degraded_nodes"],
            },
        }
        
        self.integration_log.append(result)
        return result
    
    def integration_summary(self) -> Dict:
        """Comprehensive summary of integrated simulation."""
        return {
            "total_ticks": len(self.integration_log),
            "total_infrastructure_impacts": len(self.cascade_engine.failure_log),
            "average_system_health": round(
                sum(
                    r["system_health"]["stability"] 
                    for r in self.integration_log
                ) / max(len(self.integration_log), 1),
                3
            ),
            "peak_cascade_depth": max(
                c.get("cascade_depth", 0) for c in self.cascade_engine.cascade_history
            ),
            "total_nodes_recovered": sum(
                r.get("nodes_repaired", 0) 
                for r in self.recovery_model.repair_history
            ),
            "grid_cells_impacted": sum(
                r["grid_impacts"]["cells_affected"]
                for r in self.integration_log
            ),
        }
