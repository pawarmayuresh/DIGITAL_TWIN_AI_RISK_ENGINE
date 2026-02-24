"""
Cascading Failure Engine — Cascading Failure Engine
Propagates infrastructure failures through the dependency graph.
Implements threshold-based collapse, recovery, and stability scoring.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
import networkx as nx
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class FailureEvent:
    """Records a single failure occurrence during cascade."""
    node_id: str
    tick: int
    trigger: str           # "disaster", "overload", "cascade"
    capacity_before: float
    capacity_after: float


class CascadingFailureEngine:
    """
    Core cascade propagation engine.

    Algorithm:
    1. Mark initially failed nodes (from disaster impacts).
    2. Identify dependent nodes whose required inputs drop below threshold.
    3. Propagate failures iteratively until no new failures occur (fixpoint).
    4. Record cascade depth and affected node set.
    
    Key Parameters:
    - DEFAULT_FAILURE_THRESHOLD: Capacity below which node is considered failed
    - PROPAGATION_ATTENUATION: Damage reduction per hop in the dependency chain
    """

    DEFAULT_FAILURE_THRESHOLD = 0.3    # capacity below this → node fails
    PROPAGATION_ATTENUATION = 0.7      # each hop attenuates impact by this factor

    def __init__(self, infra_graph, threshold: float = DEFAULT_FAILURE_THRESHOLD):
        self.infra_graph = infra_graph
        self.threshold = threshold
        self.failure_log: List[FailureEvent] = []
        self._current_tick: int = 0
        self.cascade_history: List[Dict] = []

    # ------------------------------------------------------------------ #
    # Main entry point
    # ------------------------------------------------------------------ #
    
    def propagate_failures(
        self, initial_failures: Dict[str, float], tick: int
    ) -> Dict[str, any]:
        """
        Propagate failures through infrastructure network.
        
        Args:
            initial_failures: {node_id: damage_amount (0–1)}
            tick: current simulation tick

        Returns:
            {
                "failed": [...node_ids...],
                "degraded": [...node_ids...],
                "cascade_depth": int,
                "total_failed": int,
                "cascade_events": int,
            }
        """
        self._current_tick = tick
        failed: Set[str] = set()
        degraded: Set[str] = set()
        cascade_event_count = 0

        # Apply initial damages
        for node_id, damage in initial_failures.items():
            node = self.infra_graph._nodes.get(node_id)
            if node:
                cap_before = node.capacity
                node.degrade(damage)
                self.failure_log.append(
                    FailureEvent(node_id, tick, "disaster", cap_before, node.capacity)
                )
                if node.capacity <= self.threshold:
                    failed.add(node_id)
                else:
                    degraded.add(node_id)

        # Iterative cascade propagation
        cascade_depth = 0
        new_failures = set(failed)
        while new_failures:
            next_wave = self._propagate_wave(new_failures, failed, tick)
            failed |= next_wave
            cascade_event_count += len(next_wave)
            new_failures = next_wave
            cascade_depth += 1
            if cascade_depth > 50:      # safety cap
                break

        # Record history
        result = {
            "failed": list(failed),
            "degraded": list(degraded),
            "cascade_depth": cascade_depth,
            "total_failed": len(failed),
            "cascade_events": cascade_event_count,
        }
        self.cascade_history.append(result)
        
        return result

    def _propagate_wave(
        self, newly_failed: Set[str], all_failed: Set[str], tick: int
    ) -> Set[str]:
        """For each newly failed node, degrade its dependents."""
        next_wave: Set[str] = set()
        for failed_id in newly_failed:
            dependents = self.infra_graph.get_dependents(failed_id)
            for dep_id in dependents:
                if dep_id in all_failed:
                    continue
                node = self.infra_graph._nodes.get(dep_id)
                if not node:
                    continue
                
                edge_data = self.infra_graph.graph.get_edge_data(failed_id, dep_id)
                edge_weight = edge_data.get("weight", 1.0) if edge_data else 1.0
                impact = edge_weight * self.PROPAGATION_ATTENUATION
                
                cap_before = node.capacity
                node.degrade(impact)
                self.failure_log.append(
                    FailureEvent(dep_id, tick, "cascade", cap_before, node.capacity)
                )
                if node.capacity <= self.threshold:
                    next_wave.add(dep_id)
        return next_wave

    # ------------------------------------------------------------------ #
    # Stability & recovery
    # ------------------------------------------------------------------ #
    
    def stability_index(self) -> float:
        """
        System-wide stability = mean capacity of all operational nodes.
        0 = total collapse, 1 = fully operational.
        """
        nodes = list(self.infra_graph._nodes.values())
        if not nodes:
            return 0.0
        return sum(n.capacity for n in nodes) / len(nodes)
    
    def weighted_stability_index(self) -> float:
        """
        Stability weighted by criticality.
        More critical nodes have higher weight.
        """
        nodes = list(self.infra_graph._nodes.values())
        if not nodes:
            return 0.0
        total_weight = sum(n.criticality for n in nodes)
        if total_weight == 0:
            return 0.0
        weighted_sum = sum(n.capacity * n.criticality for n in nodes)
        return weighted_sum / total_weight
    
    def failure_rate(self) -> float:
        """Fraction of nodes that have failed."""
        nodes = list(self.infra_graph._nodes.values())
        if not nodes:
            return 0.0
        failed = sum(1 for n in nodes if n.capacity <= self.threshold)
        return failed / len(nodes)

    def cascade_summary(self) -> Dict:
        """Comprehensive summary of cascade state."""
        total_nodes = len(self.infra_graph._nodes)
        failed = self.infra_graph.get_failed_nodes()
        degraded = self.infra_graph.get_degraded_nodes()
        return {
            "total_nodes": total_nodes,
            "failed_nodes": len(failed),
            "degraded_nodes": len(degraded),
            "operational_nodes": total_nodes - len(failed) - len(degraded),
            "failure_rate": round(self.failure_rate(), 3),
            "stability_index": round(self.stability_index(), 3),
            "weighted_stability": round(self.weighted_stability_index(), 3),
            "events_logged": len(self.failure_log),
            "cascade_history_length": len(self.cascade_history),
        }

    # ------------------------------------------------------------------ #
    # Export and analysis
    # ------------------------------------------------------------------ #
    
    def export_failure_log(self, limit: Optional[int] = None) -> List[Dict]:
        """Export failure events as dictionaries."""
        log = self.failure_log[:limit] if limit else self.failure_log
        return [
            {
                "node_id": fe.node_id,
                "tick": fe.tick,
                "trigger": fe.trigger,
                "capacity_before": round(fe.capacity_before, 3),
                "capacity_after": round(fe.capacity_after, 3),
            }
            for fe in log
        ]
