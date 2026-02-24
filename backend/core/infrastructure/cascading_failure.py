"""
Cascading Failure Engine - BATCH 4
Allows failures to propagate automatically through the network
"""
from typing import List, Dict, Set
from backend.core.infrastructure.probabilistic_node import ProbabilisticNode, NodeState
from backend.core.infrastructure.bayesian_network import InfrastructureBayesianNetwork


class CascadingFailureEngine:
    """Simulates cascading failures in infrastructure network"""
    
    def __init__(self, network: InfrastructureBayesianNetwork, failure_threshold: float = 0.6):
        self.network = network
        self.failure_threshold = failure_threshold
        self.cascade_history: List[Dict] = []
        self.current_cascade: List[str] = []
        
    def check_and_propagate_failures(self) -> Dict:
        """Check for failures and propagate stress to dependent nodes"""
        cascade_events = []
        affected_nodes: Set[str] = set()
        
        # Step 1: Identify nodes exceeding failure threshold
        critical_nodes = []
        for node in self.network.nodes.values():
            p_failed = node.probabilities[NodeState.FAILED]
            
            if p_failed > self.failure_threshold:
                critical_nodes.append(node)
                affected_nodes.add(node.node_id)
                
                cascade_events.append({
                    "node_id": node.node_id,
                    "type": "CRITICAL_FAILURE",
                    "failure_probability": p_failed,
                    "message": f"{node.node_id} has {p_failed*100:.1f}% failure probability"
                })
        
        # Step 2: Propagate stress to children
        for node in critical_nodes:
            stress_level = node.probabilities[NodeState.FAILED]
            
            for child, weight in node.children:
                # Calculate stress propagation
                stress_increase = stress_level * weight * 0.4  # 40% of parent stress
                
                # Increase child's failure probability
                old_p_failed = child.probabilities[NodeState.FAILED]
                child.update_probability(NodeState.FAILED, stress_increase)
                child.update_probability(NodeState.DEGRADED, stress_increase * 0.5)
                child.update_probability(NodeState.HEALTHY, -stress_increase * 1.5)
                
                new_p_failed = child.probabilities[NodeState.FAILED]
                
                if new_p_failed > old_p_failed + 0.05:  # Significant increase
                    affected_nodes.add(child.node_id)
                    cascade_events.append({
                        "node_id": child.node_id,
                        "type": "CASCADE_STRESS",
                        "source": node.node_id,
                        "stress_increase": stress_increase,
                        "old_failure_prob": old_p_failed,
                        "new_failure_prob": new_p_failed,
                        "message": f"{child.node_id} stress increased from {old_p_failed*100:.1f}% to {new_p_failed*100:.1f}% due to {node.node_id}"
                    })
        
        # Step 3: Check for chain reactions
        chain_reaction = self._detect_chain_reaction(affected_nodes)
        
        cascade_result = {
            "cascade_detected": len(cascade_events) > 0,
            "num_events": len(cascade_events),
            "events": cascade_events,
            "affected_nodes": list(affected_nodes),
            "chain_reaction": chain_reaction,
            "severity": self._calculate_cascade_severity(cascade_events)
        }
        
        self.cascade_history.append(cascade_result)
        self.current_cascade = list(affected_nodes)
        
        return cascade_result
    
    def _detect_chain_reaction(self, affected_nodes: Set[str]) -> bool:
        """Detect if cascade is spreading (chain reaction)"""
        if len(self.cascade_history) < 2:
            return False
        
        # Check if number of affected nodes is increasing
        prev_cascade = self.cascade_history[-1] if self.cascade_history else {"affected_nodes": []}
        prev_affected = set(prev_cascade.get("affected_nodes", []))
        
        return len(affected_nodes) > len(prev_affected)
    
    def _calculate_cascade_severity(self, events: List[Dict]) -> str:
        """Calculate severity of cascade"""
        if len(events) == 0:
            return "NONE"
        elif len(events) <= 2:
            return "LOW"
        elif len(events) <= 5:
            return "MEDIUM"
        elif len(events) <= 10:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def simulate_node_failure(self, node_id: str) -> Dict:
        """Manually trigger a node failure and observe cascade"""
        node = self.network.get_node_by_id(node_id)
        if not node:
            return {"success": False, "message": "Node not found"}
        
        # Force node to failed state
        node.set_probabilities(0.05, 0.15, 0.80)
        
        # Propagate the failure
        cascade_result = self.check_and_propagate_failures()
        
        return {
            "success": True,
            "triggered_node": node_id,
            "cascade": cascade_result
        }
    
    def get_cascade_path(self, start_node_id: str) -> List[str]:
        """Get potential cascade path from a node"""
        visited = set()
        path = []
        
        def dfs(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)
            path.append(node_id)
            
            node = self.network.get_node_by_id(node_id)
            if node:
                for child, weight in node.children:
                    if weight > 0.5:  # Only follow strong dependencies
                        dfs(child.node_id)
        
        dfs(start_node_id)
        return path
    
    def get_vulnerability_analysis(self) -> Dict:
        """Analyze network vulnerability to cascading failures"""
        vulnerability_scores = {}
        
        for node in self.network.nodes.values():
            # Calculate vulnerability based on:
            # 1. Number of dependencies
            # 2. Current failure probability
            # 3. Importance (number of children)
            
            num_parents = len(node.parents)
            num_children = len(node.children)
            p_failed = node.probabilities[NodeState.FAILED]
            
            # Vulnerability score
            dependency_factor = min(num_parents / 3.0, 1.0)  # Normalize
            importance_factor = min(num_children / 3.0, 1.0)
            
            vulnerability = (
                p_failed * 0.4 +
                dependency_factor * 0.3 +
                importance_factor * 0.3
            )
            
            vulnerability_scores[node.node_id] = {
                "score": vulnerability,
                "failure_prob": p_failed,
                "num_dependencies": num_parents,
                "num_dependents": num_children,
                "risk_level": "HIGH" if vulnerability > 0.6 else "MEDIUM" if vulnerability > 0.3 else "LOW"
            }
        
        # Sort by vulnerability
        sorted_nodes = sorted(
            vulnerability_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return {
            "most_vulnerable": sorted_nodes[:5],
            "vulnerability_scores": vulnerability_scores,
            "network_resilience": 1.0 - (sum(v["score"] for v in vulnerability_scores.values()) / len(vulnerability_scores))
        }
