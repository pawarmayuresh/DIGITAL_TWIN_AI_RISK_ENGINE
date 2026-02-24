"""
Dynamic Bayesian Network - BATCH 5
Adds temporal modeling and prediction capability
P(State_t | State_t-1, Evidence_t)
"""
from typing import Dict, List, Optional
from backend.core.infrastructure.probabilistic_node import ProbabilisticNode, NodeState
from backend.core.infrastructure.bayesian_network import InfrastructureBayesianNetwork
import random


class TemporalTransitionModel:
    """Models state transitions over time"""
    
    def __init__(self):
        # Transition probabilities: P(State_t | State_t-1)
        self.transitions = {
            NodeState.HEALTHY: {
                NodeState.HEALTHY: 0.90,
                NodeState.DEGRADED: 0.08,
                NodeState.FAILED: 0.02
            },
            NodeState.DEGRADED: {
                NodeState.HEALTHY: 0.15,
                NodeState.DEGRADED: 0.60,
                NodeState.FAILED: 0.25
            },
            NodeState.FAILED: {
                NodeState.HEALTHY: 0.05,
                NodeState.DEGRADED: 0.15,
                NodeState.FAILED: 0.80
            }
        }
    
    def get_transition_probability(self, from_state: NodeState, to_state: NodeState) -> float:
        """Get P(to_state | from_state)"""
        return self.transitions[from_state][to_state]
    
    def predict_next_state_distribution(self, current_probs: Dict[NodeState, float]) -> Dict[NodeState, float]:
        """Predict probability distribution at next timestep"""
        next_probs = {state: 0.0 for state in NodeState}
        
        for current_state, current_prob in current_probs.items():
            for next_state in NodeState:
                transition_prob = self.get_transition_probability(current_state, next_state)
                next_probs[next_state] += current_prob * transition_prob
        
        return next_probs


class DynamicBayesianNetwork:
    """Extends Bayesian Network with temporal modeling"""
    
    def __init__(self, network: InfrastructureBayesianNetwork):
        self.network = network
        self.transition_model = TemporalTransitionModel()
        self.prediction_horizon = 5  # Predict 5 steps ahead
        
    def predict_node_future(self, node_id: str, steps: int = 5) -> List[Dict]:
        """Predict future state distribution for a node"""
        node = self.network.get_node_by_id(node_id)
        if not node:
            return []
        
        predictions = []
        current_probs = node.probabilities.copy()
        
        for step in range(1, steps + 1):
            # Predict next distribution
            next_probs = self.transition_model.predict_next_state_distribution(current_probs)
            
            predictions.append({
                "timestep": self.network.timestep + step,
                "step_ahead": step,
                "probabilities": {
                    "healthy": next_probs[NodeState.HEALTHY],
                    "degraded": next_probs[NodeState.DEGRADED],
                    "failed": next_probs[NodeState.FAILED]
                },
                "predicted_health_score": next_probs[NodeState.HEALTHY] * 100,
                "predicted_risk_score": next_probs[NodeState.FAILED] * 100,
                "most_likely_state": max(next_probs.items(), key=lambda x: x[1])[0].value
            })
            
            current_probs = next_probs
        
        return predictions
    
    def predict_network_future(self, steps: int = 5) -> Dict:
        """Predict future state of entire network"""
        network_predictions = {}
        
        for node_id in self.network.nodes.keys():
            network_predictions[node_id] = self.predict_node_future(node_id, steps)
        
        # Calculate aggregate predictions
        aggregate_predictions = []
        for step in range(steps):
            step_data = {
                "timestep": self.network.timestep + step + 1,
                "step_ahead": step + 1,
                "avg_health": 0.0,
                "avg_risk": 0.0,
                "nodes_at_risk": 0,
                "nodes_likely_to_fail": []
            }
            
            for node_id, predictions in network_predictions.items():
                if step < len(predictions):
                    pred = predictions[step]
                    step_data["avg_health"] += pred["predicted_health_score"]
                    step_data["avg_risk"] += pred["predicted_risk_score"]
                    
                    if pred["predicted_risk_score"] > 50:
                        step_data["nodes_at_risk"] += 1
                        step_data["nodes_likely_to_fail"].append({
                            "node_id": node_id,
                            "risk_score": pred["predicted_risk_score"]
                        })
            
            num_nodes = len(self.network.nodes)
            if num_nodes > 0:
                step_data["avg_health"] /= num_nodes
                step_data["avg_risk"] /= num_nodes
            
            aggregate_predictions.append(step_data)
        
        return {
            "current_timestep": self.network.timestep,
            "prediction_horizon": steps,
            "node_predictions": network_predictions,
            "aggregate_predictions": aggregate_predictions,
            "warnings": self._generate_warnings(aggregate_predictions)
        }
    
    def _generate_warnings(self, predictions: List[Dict]) -> List[str]:
        """Generate warnings based on predictions"""
        warnings = []
        
        for pred in predictions:
            if pred["avg_risk"] > 60:
                warnings.append(
                    f"⚠️ CRITICAL: Network risk predicted to reach {pred['avg_risk']:.1f}% "
                    f"in {pred['step_ahead']} timesteps"
                )
            elif pred["avg_risk"] > 40:
                warnings.append(
                    f"⚠️ WARNING: Network risk predicted to reach {pred['avg_risk']:.1f}% "
                    f"in {pred['step_ahead']} timesteps"
                )
            
            if pred["nodes_at_risk"] > len(self.network.nodes) * 0.3:
                warnings.append(
                    f"⚠️ {pred['nodes_at_risk']} nodes predicted to be at high risk "
                    f"in {pred['step_ahead']} timesteps"
                )
        
        return warnings
    
    def detect_collapse_risk(self, threshold: float = 0.7) -> Dict:
        """Detect if network is heading towards collapse"""
        predictions = self.predict_network_future(steps=self.prediction_horizon)
        
        collapse_detected = False
        collapse_timestep = None
        
        for pred in predictions["aggregate_predictions"]:
            if pred["avg_risk"] > threshold * 100:
                collapse_detected = True
                collapse_timestep = pred["timestep"]
                break
        
        return {
            "collapse_risk_detected": collapse_detected,
            "collapse_timestep": collapse_timestep,
            "steps_until_collapse": collapse_timestep - self.network.timestep if collapse_timestep else None,
            "current_risk": predictions["aggregate_predictions"][0]["avg_risk"] if predictions["aggregate_predictions"] else 0,
            "peak_predicted_risk": max(p["avg_risk"] for p in predictions["aggregate_predictions"]) if predictions["aggregate_predictions"] else 0,
            "recommendations": self._generate_recommendations(collapse_detected, predictions)
        }
    
    def _generate_recommendations(self, collapse_detected: bool, predictions: Dict) -> List[str]:
        """Generate recommendations based on predictions"""
        recommendations = []
        
        if collapse_detected:
            recommendations.append("🚨 IMMEDIATE ACTION REQUIRED: Network collapse predicted")
            recommendations.append("Prioritize critical infrastructure maintenance")
            recommendations.append("Activate emergency response protocols")
        
        # Identify most vulnerable nodes
        first_step = predictions["aggregate_predictions"][0] if predictions["aggregate_predictions"] else {}
        at_risk_nodes = first_step.get("nodes_likely_to_fail", [])
        
        if at_risk_nodes:
            top_risk = sorted(at_risk_nodes, key=lambda x: x["risk_score"], reverse=True)[:3]
            recommendations.append(
                f"Focus on: {', '.join(n['node_id'] for n in top_risk)}"
            )
        
        return recommendations
