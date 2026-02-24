"""
Bayesian Network for Infrastructure - BATCH 2 & 3
Implements CPTs and real-time evidence integration
"""
from typing import Dict, List, Optional
from backend.core.infrastructure.probabilistic_node import ProbabilisticNode, NodeState
import math


class ConditionalProbabilityTable:
    """CPT for modeling P(Child | Parents)"""
    
    def __init__(self):
        # Simplified CPT: P(Failed | parent_states)
        # Format: {(parent1_state, parent2_state, ...): p_failed}
        self.table: Dict[tuple, float] = {}
        
    def add_entry(self, parent_states: tuple, p_failed: float):
        """Add CPT entry"""
        self.table[parent_states] = p_failed
    
    def get_failure_probability(self, parent_states: tuple) -> float:
        """Get failure probability given parent states"""
        return self.table.get(parent_states, 0.02)  # Default low probability


class InfrastructureBayesianNetwork:
    """Bayesian Network for infrastructure dependencies"""
    
    def __init__(self):
        self.nodes: Dict[str, ProbabilisticNode] = {}
        self.cpts: Dict[str, ConditionalProbabilityTable] = {}
        self.evidence: Dict[str, float] = {}
        self.timestep = 0
        
    def add_node(self, node: ProbabilisticNode):
        """Add node to network"""
        self.nodes[node.node_id] = node
        
    def add_dependency(self, parent_id: str, child_id: str, weight: float):
        """Add dependency between nodes"""
        if parent_id in self.nodes and child_id in self.nodes:
            parent = self.nodes[parent_id]
            child = self.nodes[child_id]
            parent.add_child(child, weight)
            child.add_parent(parent, weight)
    
    def initialize_cpt(self, node_id: str):
        """Initialize CPT for a node with simplified rules"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        cpt = ConditionalProbabilityTable()
        
        # Simplified CPT based on number of parents
        if len(node.parents) == 0:
            # No parents - use prior
            pass
        elif len(node.parents) == 1:
            # Single parent
            cpt.add_entry((NodeState.HEALTHY,), 0.02)
            cpt.add_entry((NodeState.DEGRADED,), 0.15)
            cpt.add_entry((NodeState.FAILED,), 0.60)
        elif len(node.parents) == 2:
            # Two parents (e.g., Power + Water)
            cpt.add_entry((NodeState.HEALTHY, NodeState.HEALTHY), 0.02)
            cpt.add_entry((NodeState.FAILED, NodeState.HEALTHY), 0.40)
            cpt.add_entry((NodeState.HEALTHY, NodeState.FAILED), 0.35)
            cpt.add_entry((NodeState.FAILED, NodeState.FAILED), 0.75)
            cpt.add_entry((NodeState.DEGRADED, NodeState.HEALTHY), 0.15)
            cpt.add_entry((NodeState.HEALTHY, NodeState.DEGRADED), 0.15)
            cpt.add_entry((NodeState.DEGRADED, NodeState.DEGRADED), 0.30)
            cpt.add_entry((NodeState.DEGRADED, NodeState.FAILED), 0.50)
            cpt.add_entry((NodeState.FAILED, NodeState.DEGRADED), 0.50)
        
        self.cpts[node_id] = cpt
    
    def set_evidence(self, evidence: Dict[str, float]):
        """Set evidence variables (rain, flood, cyber attack, etc.)"""
        self.evidence = evidence
    
    def apply_evidence_to_nodes(self):
        """Apply evidence to modify node probabilities - BATCH 3"""
        rain_intensity = self.evidence.get('RainIntensity', 0.0)
        flood_level = self.evidence.get('FloodLevel', 0.0)
        cyber_attack = self.evidence.get('CyberAttack', 0.0)
        power_stress = self.evidence.get('PowerStress', 0.0)
        water_stress = self.evidence.get('WaterStress', 0.0)
        
        for node in self.nodes.values():
            # Reset to baseline first
            if node.node_type == "Utility":
                if "Power" in node.node_id:
                    # Power affected by rain and cyber attacks
                    failure_increase = rain_intensity * 0.15 + cyber_attack * 0.25 + power_stress * 0.20
                    node.update_probability(NodeState.FAILED, failure_increase)
                    node.update_probability(NodeState.HEALTHY, -failure_increase * 0.7)
                    
                elif "Water" in node.node_id:
                    # Water affected by flood
                    failure_increase = flood_level * 0.20 + water_stress * 0.15
                    node.update_probability(NodeState.FAILED, failure_increase)
                    node.update_probability(NodeState.HEALTHY, -failure_increase * 0.7)
            
            elif node.node_type == "IT":
                # Data centers affected by power and cyber attacks
                failure_increase = cyber_attack * 0.30 + power_stress * 0.10
                node.update_probability(NodeState.FAILED, failure_increase)
                node.update_probability(NodeState.HEALTHY, -failure_increase * 0.7)
            
            elif node.node_type == "Healthcare":
                # Hospitals affected by flood and power
                failure_increase = flood_level * 0.10 + power_stress * 0.15
                node.update_probability(NodeState.FAILED, failure_increase)
                node.update_probability(NodeState.HEALTHY, -failure_increase * 0.7)
            
            elif node.node_type == "Emergency":
                # Emergency services affected by overall stress
                failure_increase = (rain_intensity + flood_level) * 0.08
                node.update_probability(NodeState.FAILED, failure_increase)
                node.update_probability(NodeState.HEALTHY, -failure_increase * 0.7)
    
    def propagate_beliefs(self):
        """Bayesian inference - propagate probabilities through network"""
        # Simplified belief propagation
        # In full implementation, use message passing or variable elimination
        
        for node in self.nodes.values():
            if len(node.parents) == 0:
                continue  # Root nodes already updated by evidence
            
            # Calculate influence from parents
            total_failure_influence = 0.0
            total_weight = 0.0
            
            for parent, weight in node.parents:
                parent_failure_prob = parent.probabilities[NodeState.FAILED]
                parent_degraded_prob = parent.probabilities[NodeState.DEGRADED]
                
                # Weighted influence
                influence = (parent_failure_prob * 0.8 + parent_degraded_prob * 0.3) * weight
                total_failure_influence += influence
                total_weight += weight
            
            if total_weight > 0:
                avg_influence = total_failure_influence / total_weight
                
                # Update child probabilities based on parent influence
                node.update_probability(NodeState.FAILED, avg_influence * 0.5)
                node.update_probability(NodeState.DEGRADED, avg_influence * 0.3)
                node.update_probability(NodeState.HEALTHY, -avg_influence * 0.8)
    
    def update_network(self, evidence: Optional[Dict[str, float]] = None):
        """Full network update - BATCH 3 real-time integration"""
        self.timestep += 1
        
        if evidence:
            self.set_evidence(evidence)
        
        # Step 1: Apply evidence to root nodes
        self.apply_evidence_to_nodes()
        
        # Step 2: Propagate beliefs through network
        self.propagate_beliefs()
        
        # Step 3: Update state history
        for node in self.nodes.values():
            current_state = node.get_most_likely_state()
            node.state_history.append(current_state)
            node.previous_state = current_state
    
    def get_network_state(self) -> Dict:
        """Get current state of entire network"""
        return {
            "timestep": self.timestep,
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "evidence": self.evidence,
            "total_nodes": len(self.nodes),
            "total_dependencies": sum(len(n.parents) for n in self.nodes.values()),
            "average_health": sum(n.get_health_score() for n in self.nodes.values()) / len(self.nodes) if self.nodes else 0,
            "average_risk": sum(n.get_risk_score() for n in self.nodes.values()) / len(self.nodes) if self.nodes else 0,
            "critical_nodes": [n.node_id for n in self.nodes.values() if n.get_risk_score() > 50]
        }
    
    def get_node_by_id(self, node_id: str) -> Optional[ProbabilisticNode]:
        """Get node by ID"""
        return self.nodes.get(node_id)
    
    def get_nodes_by_type(self, node_type: str) -> List[ProbabilisticNode]:
        """Get all nodes of a specific type"""
        return [n for n in self.nodes.values() if n.node_type == node_type]
    
    def get_nodes_by_ward(self, ward: str) -> List[ProbabilisticNode]:
        """Get all nodes in a specific ward"""
        return [n for n in self.nodes.values() if n.ward == ward]
