"""
Causal Graph Generator - Builds causal graphs showing decision relationships.
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class CausalRelationType(Enum):
    """Types of causal relationships."""
    DIRECT_CAUSE = "direct_cause"
    INDIRECT_CAUSE = "indirect_cause"
    CORRELATION = "correlation"
    INHIBITION = "inhibition"
    AMPLIFICATION = "amplification"


@dataclass
class CausalNode:
    """Node in a causal graph."""
    node_id: str
    label: str
    node_type: str  # 'input', 'intermediate', 'output'
    value: Any
    importance: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CausalEdge:
    """Edge in a causal graph."""
    source_id: str
    target_id: str
    relation_type: CausalRelationType
    strength: float  # 0.0 to 1.0
    explanation: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class CausalGraphGenerator:
    """Generates causal graphs for AI decisions."""
    
    def __init__(self):
        self.graphs: Dict[str, Dict[str, Any]] = {}
    
    def build_graph(
        self,
        decision_id: str,
        inputs: Dict[str, Any],
        intermediates: Dict[str, Any],
        outputs: Dict[str, Any],
        trace_steps: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """Build a causal graph from decision data."""
        
        nodes = []
        edges = []
        
        # Create input nodes
        for key, value in inputs.items():
            node = CausalNode(
                node_id=f"input_{key}",
                label=key,
                node_type='input',
                value=value,
                importance=self._calculate_importance(key, value, outputs)
            )
            nodes.append(node)
        
        # Create intermediate nodes
        for key, value in intermediates.items():
            node = CausalNode(
                node_id=f"intermediate_{key}",
                label=key,
                node_type='intermediate',
                value=value,
                importance=self._calculate_importance(key, value, outputs)
            )
            nodes.append(node)
        
        # Create output nodes
        for key, value in outputs.items():
            node = CausalNode(
                node_id=f"output_{key}",
                label=key,
                node_type='output',
                value=value,
                importance=1.0  # Outputs are always important
            )
            nodes.append(node)
        
        # Build edges from trace steps
        if trace_steps:
            edges.extend(self._build_edges_from_trace(trace_steps, nodes))
        else:
            edges.extend(self._infer_edges(inputs, intermediates, outputs))
        
        graph = {
            'decision_id': decision_id,
            'nodes': [self._node_to_dict(n) for n in nodes],
            'edges': [self._edge_to_dict(e) for e in edges],
            'metadata': {
                'num_inputs': len(inputs),
                'num_intermediates': len(intermediates),
                'num_outputs': len(outputs)
            }
        }
        
        self.graphs[decision_id] = graph
        return graph
    
    def _calculate_importance(
        self,
        key: str,
        value: Any,
        outputs: Dict[str, Any]
    ) -> float:
        """Calculate importance of a node."""
        # Simple heuristic: higher values = more important
        if isinstance(value, (int, float)):
            # Normalize to 0-1 range
            return min(abs(value) / 100.0, 1.0)
        elif isinstance(value, bool):
            return 1.0 if value else 0.3
        elif isinstance(value, str):
            # Check if mentioned in outputs
            for output_val in outputs.values():
                if isinstance(output_val, str) and key in output_val:
                    return 0.8
            return 0.5
        else:
            return 0.5
    
    def _build_edges_from_trace(
        self,
        trace_steps: List[Any],
        nodes: List[CausalNode]
    ) -> List[CausalEdge]:
        """Build edges from decision trace steps."""
        edges = []
        
        for i, step in enumerate(trace_steps):
            # Extract inputs and outputs from step
            step_inputs = step.inputs if hasattr(step, 'inputs') else {}
            step_outputs = step.outputs if hasattr(step, 'outputs') else {}
            
            # Create edges from inputs to outputs
            for input_key in step_inputs.keys():
                for output_key in step_outputs.keys():
                    source_node = self._find_node(nodes, input_key)
                    target_node = self._find_node(nodes, output_key)
                    
                    if source_node and target_node:
                        edge = CausalEdge(
                            source_id=source_node.node_id,
                            target_id=target_node.node_id,
                            relation_type=CausalRelationType.DIRECT_CAUSE,
                            strength=step.confidence if hasattr(step, 'confidence') else 0.8,
                            explanation=step.reasoning if hasattr(step, 'reasoning') else "Direct causal relationship"
                        )
                        edges.append(edge)
        
        return edges
    
    def _infer_edges(
        self,
        inputs: Dict[str, Any],
        intermediates: Dict[str, Any],
        outputs: Dict[str, Any]
    ) -> List[CausalEdge]:
        """Infer edges when trace is not available."""
        edges = []
        
        # Connect inputs to intermediates
        for input_key in inputs.keys():
            for inter_key in intermediates.keys():
                if self._are_related(input_key, inter_key):
                    edge = CausalEdge(
                        source_id=f"input_{input_key}",
                        target_id=f"intermediate_{inter_key}",
                        relation_type=CausalRelationType.DIRECT_CAUSE,
                        strength=0.7,
                        explanation=f"{input_key} influences {inter_key}"
                    )
                    edges.append(edge)
        
        # Connect intermediates to outputs
        for inter_key in intermediates.keys():
            for output_key in outputs.keys():
                if self._are_related(inter_key, output_key):
                    edge = CausalEdge(
                        source_id=f"intermediate_{inter_key}",
                        target_id=f"output_{output_key}",
                        relation_type=CausalRelationType.DIRECT_CAUSE,
                        strength=0.8,
                        explanation=f"{inter_key} determines {output_key}"
                    )
                    edges.append(edge)
        
        # Connect inputs directly to outputs if no intermediates
        if not intermediates:
            for input_key in inputs.keys():
                for output_key in outputs.keys():
                    edge = CausalEdge(
                        source_id=f"input_{input_key}",
                        target_id=f"output_{output_key}",
                        relation_type=CausalRelationType.DIRECT_CAUSE,
                        strength=0.9,
                        explanation=f"{input_key} directly affects {output_key}"
                    )
                    edges.append(edge)
        
        return edges
    
    def _find_node(self, nodes: List[CausalNode], key: str) -> Optional[CausalNode]:
        """Find a node by key."""
        for node in nodes:
            if key in node.node_id or key in node.label:
                return node
        return None
    
    def _are_related(self, key1: str, key2: str) -> bool:
        """Check if two keys are semantically related."""
        # Simple heuristic: check for common words
        words1 = set(key1.lower().split('_'))
        words2 = set(key2.lower().split('_'))
        return len(words1 & words2) > 0
    
    def _node_to_dict(self, node: CausalNode) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            'node_id': node.node_id,
            'label': node.label,
            'node_type': node.node_type,
            'value': str(node.value),
            'importance': node.importance,
            'metadata': node.metadata
        }
    
    def _edge_to_dict(self, edge: CausalEdge) -> Dict[str, Any]:
        """Convert edge to dictionary."""
        return {
            'source_id': edge.source_id,
            'target_id': edge.target_id,
            'relation_type': edge.relation_type.value,
            'strength': edge.strength,
            'explanation': edge.explanation,
            'metadata': edge.metadata
        }
    
    def get_graph(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Get a causal graph by decision ID."""
        return self.graphs.get(decision_id)
    
    def get_critical_path(self, decision_id: str) -> List[str]:
        """Get the critical path (most important nodes) in a graph."""
        graph = self.graphs.get(decision_id)
        if not graph:
            return []
        
        # Sort nodes by importance
        nodes = sorted(graph['nodes'], key=lambda n: n['importance'], reverse=True)
        
        # Return top 5 most important nodes
        return [n['label'] for n in nodes[:5]]
    
    def explain_relationship(
        self,
        decision_id: str,
        source_label: str,
        target_label: str
    ) -> Optional[str]:
        """Explain the relationship between two nodes."""
        graph = self.graphs.get(decision_id)
        if not graph:
            return None
        
        # Find edge
        for edge in graph['edges']:
            source_node = next((n for n in graph['nodes'] if n['node_id'] == edge['source_id']), None)
            target_node = next((n for n in graph['nodes'] if n['node_id'] == edge['target_id']), None)
            
            if source_node and target_node:
                if source_node['label'] == source_label and target_node['label'] == target_label:
                    return edge['explanation']
        
        return None
