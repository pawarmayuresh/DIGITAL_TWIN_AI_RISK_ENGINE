"""
Stability Calculator — Infrastructure system resilience metrics.

Provides comprehensive stability analysis:
- Single points of failure identification
- Redundancy assessment
- Cascade vulnerability scoring
- Network resilience metrics
- Critical path analysis
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
import networkx as nx


class StabilityCalculator:
    """
    Analyzes infrastructure network resilience and vulnerability.
    
    Metrics:
    - System stability index (0-1)
    - Cascade vulnerability (how quickly failures propagate)
    - Redundancy score (alternative paths available)
    - Critical node importance
    """
    
    def __init__(self, infra_graph, cascade_engine=None):
        self.infra_graph = infra_graph
        self.cascade_engine = cascade_engine
        self._stability_cache: Optional[float] = None
        self._last_update_tick: int = -1
    
    # ================================================================ #
    # Overall stability
    # ================================================================ #
    
    def system_stability_index(self, use_criticality: bool = True) -> float:
        """
        Calculate overall system stability (0-1).
        
        Considers:
        - Average node capacity
        - Critical nodes weighted heavier
        - Dependency network integrity
        
        Args:
            use_criticality: Weight by node importance
        
        Returns:
            0.0 = complete system failure
            1.0 = fully operational
        """
        nodes = self.infra_graph.get_all_nodes()
        if not nodes:
            return 0.0
        
        if use_criticality:
            total_weight = sum(n.criticality for n in nodes)
            if total_weight == 0:
                return 0.0
            weighted_capacity = sum(n.capacity * n.criticality for n in nodes)
            return weighted_capacity / total_weight
        else:
            return sum(n.capacity for n in nodes) / len(nodes)
    
    def cascade_vulnerability_index(self) -> float:
        """
        Score for how vulnerable the system is to cascading failures (0-1).
        
        High score = high vulnerability to propagation
        
        Factors:
        - Network density (more connections = more contagion paths)
        - Average node degradation
        - Dependency criticality
        """
        nodes = self.infra_graph.get_all_nodes()
        if not nodes:
            return 0.0
        
        # Average degradation
        avg_degradation = 1.0 - sum(n.capacity for n in nodes) / len(nodes)
        
        # Network connectivity (more edges = more cascade paths)
        try:
            graph = self.infra_graph.graph
            edge_count = graph.number_of_edges()
            node_count = graph.number_of_nodes()
            max_edges = node_count * (node_count - 1)  # Fully connected
            connectivity = edge_count / max(max_edges, 1)
        except:
            connectivity = 0.0
        
        # Weighted criticality of degraded nodes
        degraded = self.infra_graph.get_degraded_nodes()
        degraded_criticality = sum(n.criticality for n in degraded)
        max_criticality = sum(n.criticality for n in nodes)
        crit_factor = degraded_criticality / max(max_criticality, 1)
        
        # Combined vulnerability
        vulnerability = (avg_degradation * 0.4) + (connectivity * 0.3) + (crit_factor * 0.3)
        return min(1.0, vulnerability)
    
    # ================================================================ #
    # Redundancy & alternatives
    # ================================================================ #
    
    def redundancy_score(self) -> float:
        """
        How redundant is the network? (0-1)
        
        High score = many alternative paths if components fail
        """
        nodes = self.infra_graph.get_all_nodes()
        if len(nodes) < 2:
            return 0.0
        
        total_alternatives = 0
        for node in nodes:
            dependents = self.infra_graph.get_dependents(node.node_id)
            for dep_id in dependents:
                # Check if there's an alternative path (other providers)
                dep_dependencies = self.infra_graph.get_dependencies(dep_id)
                if len(dep_dependencies) > 1:
                    total_alternatives += 1
        
        max_possible = len(nodes) * 5  # Rough estimate of expected alternatives
        return min(1.0, total_alternatives / max(max_possible, 1))
    
    def critical_single_points_of_failure(self) -> List[Tuple[str, float]]:
        """
        Identify nodes whose failure would cascade to many others.
        
        Returns:
            [(node_id, cascade_impact_score), ...]
        """
        critical_nodes = []
        
        for node in self.infra_graph.get_all_nodes():
            # Score based on:
            # 1. Number of dependents
            # 2. Criticality of dependents
            # 3. Lack of alternatives
            
            dependents = self.infra_graph.get_dependents(node.node_id)
            if not dependents:
                continue
            
            dependent_criticality = sum(
                self.infra_graph._nodes[dep_id].criticality 
                for dep_id in dependents
                if dep_id in self.infra_graph._nodes
            )
            
            # Check redundancy (do dependents have alternatives?)
            redundancy_factor = 0.0
            for dep_id in dependents:
                alt_providers = len(self.infra_graph.get_dependencies(dep_id))
                if alt_providers == 1:  # No alternatives
                    redundancy_factor += 1.0
            redundancy_factor /= max(len(dependents), 1)
            
            cascade_score = (dependent_criticality * 0.5) + (redundancy_factor * 0.5)
            
            if cascade_score > 0.1:  # Only report significant ones
                critical_nodes.append((node.node_id, round(cascade_score, 3)))
        
        return sorted(critical_nodes, key=lambda x: x[1], reverse=True)
    
    # ================================================================ #
    # Dependency analysis
    # ================================================================ #
    
    def network_depth(self) -> int:
        """
        Maximum cascade depth in the network.
        How many hops from source to furthest dependent?
        """
        try:
            graph = self.infra_graph.graph
            if graph.number_of_nodes() == 0:
                return 0
            
            # Find longest path
            max_depth = 0
            for source in graph.nodes():
                for target in graph.nodes():
                    if source == target:
                        continue
                    try:
                        length = nx.shortest_path_length(graph, source, target)
                        max_depth = max(max_depth, length)
                    except:
                        pass
            return max_depth
        except:
            return 0
    
    def avg_path_length(self) -> float:
        """Average path length in the dependency graph."""
        try:
            graph = self.infra_graph.graph
            if graph.number_of_nodes() < 2:
                return 0.0
            lengths = []
            for source in graph.nodes():
                for target in graph.nodes():
                    if source == target:
                        continue
                    try:
                        length = nx.shortest_path_length(graph, source, target)
                        lengths.append(length)
                    except:
                        pass
            if lengths:
                return sum(lengths) / len(lengths)
            return 0.0
        except:
            return 0.0
    
    # ================================================================ #
    # Comprehensive reporting
    # ================================================================ #
    
    def vulnerability_report(self) -> Dict:
        """Complete vulnerability and resilience assessment."""
        critical_nodes = self.critical_single_points_of_failure()
        
        return {
            "system_stability": round(self.system_stability_index(), 3),
            "cascade_vulnerability": round(self.cascade_vulnerability_index(), 3),
            "redundancy_score": round(self.redundancy_score(), 3),
            "network_depth": self.network_depth(),
            "avg_path_length": round(self.avg_path_length(), 3),
            "critical_points": critical_nodes[:5],
            "operational_nodes": len(self.infra_graph.get_operational_nodes()),
            "degraded_nodes": len(self.infra_graph.get_degraded_nodes()),
            "failed_nodes": len(self.infra_graph.get_failed_nodes()),
        }
    
    def resilience_summary(self) -> str:
        """Human-readable resilience assessment."""
        stability = self.system_stability_index()
        vulnerability = self.cascade_vulnerability_index()
        redundancy = self.redundancy_score()
        
        if stability > 0.9:
            status = "🟢 HEALTHY"
        elif stability > 0.7:
            status = "🟡 DEGRADED"
        elif stability > 0.4:
            status = "🔴 CRITICAL"
        else:
            status = "⚫ COLLAPSED"
        
        vuln_desc = "Very Vulnerable" if vulnerability > 0.7 else "Somewhat Vulnerable" if vulnerability > 0.4 else "Resilient"
        redund_desc = "Highly Redundant" if redundancy > 0.6 else "Moderately Redundant" if redundancy > 0.3 else "Limited Redundancy"
        
        return f"{status} | Stability: {stability:.1%} | Cascade Risk: {vuln_desc} | Redundancy: {redund_desc}"
    
    def resilience_score(self) -> float:
        """
        Overall resilience metric (0-1).
        Combines stability, redundancy, and cascade resistance.
        """
        stability = self.system_stability_index()
        redundancy = self.redundancy_score()
        vulnerability = 1.0 - self.cascade_vulnerability_index()
        
        # Weighted combination
        return (stability * 0.5) + (redundancy * 0.25) + (vulnerability * 0.25)
