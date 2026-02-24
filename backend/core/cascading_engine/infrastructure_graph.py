"""
Infrastructure Graph — Network topology for cascading failure simulation.

Represents critical infrastructure (power, water, transport, healthcare, comms) as a directed 
graph with dependency relationships, capacity constraints, and failure propagation.

Node Types:
- power_plant: Generates electricity
- substation: Distributes power
- water_treatment: Produces potable water
- water_pump: Distributes water locally
- hospital: Healthcare delivery
- transport_hub: Transit center
- data_center: Communications/IT
- backup_generator: Emergency power
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx


class InfrastructureNodeType(Enum):
    """Enumeration of infrastructure component types."""
    POWER_PLANT = "power_plant"
    SUBSTATION = "substation"
    WATER_TREATMENT = "water_treatment"
    WATER_PUMP = "water_pump"
    HOSPITAL = "hospital"
    TRANSPORT_HUB = "transport_hub"
    DATA_CENTER = "data_center"
    BACKUP_GENERATOR = "backup_generator"


@dataclass
class InfrastructureNode:
    """
    Represents a single infrastructure component.
    
    Attributes:
        node_id: Unique identifier
        node_type: Category (power, water, etc.)
        location: (x, y) coordinates on grid
        capacity: Operational level (0.0 = failed, 1.0 = full)
        criticality: Importance to system (0-1, higher = more critical)
        repair_time_ticks: How many ticks to fully repair
        metadata: Additional attributes (capacity_mw, population_served, etc.)
    """
    node_id: str
    node_type: InfrastructureNodeType
    location: Tuple[float, float]
    capacity: float = 1.0  # Current operational level
    criticality: float = 0.5
    repair_time_ticks: int = 20
    metadata: Dict = field(default_factory=dict)
    
    # Internal state
    operational: bool = True
    damage_accumulated: float = 0.0
    repair_progress: float = 0.0  # 0-1, cumulative recovery
    
    def degrade(self, damage_amount: float) -> None:
        """Apply damage to this node."""
        self.damage_accumulated = min(1.0, self.damage_accumulated + damage_amount)
        self.capacity = max(0.0, 1.0 - self.damage_accumulated)
        if self.capacity == 0.0:
            self.operational = False
    
    def repair(self, repair_amount: float) -> None:
        """Apply repair to this node."""
        self.repair_progress = min(1.0, self.repair_progress + repair_amount)
        self.damage_accumulated = max(0.0, 1.0 - self.repair_progress)
        self.capacity = self.repair_progress
        if self.capacity >= 0.95:
            self.operational = True
    
    def reset_repairs(self) -> None:
        """Reset repair progress (disaster hits again)."""
        self.repair_progress = 0.0
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "location": self.location,
            "capacity": round(self.capacity, 3),
            "operational": self.operational,
            "criticality": self.criticality,
            "damage": round(self.damage_accumulated, 3),
        }


@dataclass
class InfrastructureEdge:
    """
    Represents a dependency relationship between nodes.
    
    Attributes:
        source: Provider node
        target: Dependent node
        weight: Importance of this dependency (0-1)
        edge_type: Nature of dependency (power, water, logical, etc.)
    """
    source: str
    target: str
    weight: float = 1.0
    edge_type: str = "dependency"
    
    def to_dict(self) -> Dict:
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "type": self.edge_type,
        }


class InfrastructureGraph:
    """
    Directed graph representing critical infrastructure network.
    
    Supports:
    - Node creation and dependency linking
    - Failure propagation queries
    - Emergency backup routing
    - Resilience analysis
    """
    
    def __init__(self):
        self._nodes: Dict[str, InfrastructureNode] = {}
        self._edges: Dict[Tuple[str, str], InfrastructureEdge] = {}
        self.graph = nx.DiGraph()  # Networkx backend for graph algorithms
    
    @property
    def nodes(self) -> Dict[str, InfrastructureNode]:
        """Get all nodes"""
        return self._nodes
    
    # ================================================================ #
    # Node Management
    # ================================================================ #
    
    def add_node(
        self,
        node_id: str,
        node_type: InfrastructureNodeType,
        location: Tuple[float, float],
        capacity: float = 1.0,
        criticality: float = 0.5,
        repair_time: int = 20,
        metadata: Optional[Dict] = None,
    ) -> InfrastructureNode:
        """Add a new infrastructure node to the graph."""
        node = InfrastructureNode(
            node_id=node_id,
            node_type=node_type,
            location=location,
            capacity=capacity,
            criticality=criticality,
            repair_time_ticks=repair_time,
            metadata=metadata or {},
        )
        self._nodes[node_id] = node
        self.graph.add_node(node_id)
        return node
    
    def get_node(self, node_id: str) -> Optional[InfrastructureNode]:
        """Retrieve a node by ID."""
        return self._nodes.get(node_id)
    
    def get_all_nodes(self) -> List[InfrastructureNode]:
        """Get all nodes."""
        return list(self._nodes.values())
    
    # ================================================================ #
    # Edge Management (Dependencies)
    # ================================================================ #
    
    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        weight: float = 1.0,
        edge_type: str = "dependency",
    ) -> InfrastructureEdge:
        """
        Add a dependency edge: source provides to target.
        
        Args:
            source_id: Provider node
            target_id: Dependent node
            weight: Impact magnitude if source fails (0-1)
            edge_type: Type of dependency (power, water, etc.)
        
        Returns:
            The created edge
        """
        edge = InfrastructureEdge(source_id, target_id, weight, edge_type)
        self._edges[(source_id, target_id)] = edge
        self.graph.add_edge(source_id, target_id, weight=weight, type=edge_type)
        return edge
    
    def get_dependencies(self, node_id: str) -> List[str]:
        """Get all nodes that this node depends on (incoming edges)."""
        return list(self.graph.predecessors(node_id))
    
    def get_dependents(self, node_id: str) -> List[str]:
        """Get all nodes that depend on this node (outgoing edges)."""
        return list(self.graph.successors(node_id))
    
    def get_edge(self, source_id: str, target_id: str) -> Optional[InfrastructureEdge]:
        """Get edge between two nodes."""
        return self._edges.get((source_id, target_id))
    
    # ================================================================ #
    # Graph Analysis
    # ================================================================ #
    
    def find_connected_component(self, start_node_id: str) -> Set[str]:
        """Get all nodes reachable from a given node (BFS)."""
        visited = set()
        queue = [start_node_id]
        while queue:
            node_id = queue.pop(0)
            if node_id in visited:
                continue
            visited.add(node_id)
            queue.extend(self.get_dependents(node_id))
        return visited
    
    def find_critical_path(self) -> List[str]:
        """Identify nodes with highest centrality (most dependencies)."""
        try:
            centrality = nx.degree_centrality(self.graph)
            return sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        except:
            return []
    
    def has_alternative_path(self, source_id: str, target_id: str) -> bool:
        """Check if there's a path from source to target."""
        try:
            return nx.has_path(self.graph, source_id, target_id)
        except:
            return False
    
    def get_path_length(self, source_id: str, target_id: str) -> int:
        """Get shortest path distance."""
        try:
            return nx.shortest_path_length(self.graph, source_id, target_id)
        except:
            return -1
    
    # ================================================================ #
    # Status & Reporting
    # ================================================================ #
    
    def get_failed_nodes(self) -> List[InfrastructureNode]:
        """Get all nodes with capacity <= 0."""
        return [n for n in self._nodes.values() if n.capacity <= 0.0]
    
    def get_degraded_nodes(self) -> List[InfrastructureNode]:
        """Get all nodes with 0 < capacity < 1."""
        return [n for n in self._nodes.values() if 0.0 < n.capacity < 1.0]
    
    def get_operational_nodes(self) -> List[InfrastructureNode]:
        """Get all nodes with capacity >= 0.95."""
        return [n for n in self._nodes.values() if n.capacity >= 0.95]
    
    def system_health(self) -> float:
        """Average capacity across all nodes (0-1)."""
        if not self._nodes:
            return 0.0
        return sum(n.capacity for n in self._nodes.values()) / len(self._nodes)
    
    def export_to_dict(self) -> Dict:
        """Serialize entire graph to dictionary."""
        return {
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
            "total_nodes": len(self._nodes),
            "failed_count": len(self.get_failed_nodes()),
            "system_health": round(self.system_health(), 3),
        }
