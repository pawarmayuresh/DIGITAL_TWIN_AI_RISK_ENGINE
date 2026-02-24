"""
Explanation Integrator - Integrates all explainability components.
"""

from typing import Dict, Any, Optional, Callable
from .decision_tracer import DecisionTracer, DecisionType
from .causal_graph import CausalGraphGenerator
from .shap_explainer import SHAPExplainer
from .counterfactual_analyzer import CounterfactualAnalyzer
from .confidence_estimator import ConfidenceEstimator
from .transparency_report import TransparencyReportBuilder
from .audit_log_interpreter import AuditLogInterpreter


class ExplanationIntegrator:
    """Integrates all explainability components into a unified interface."""
    
    def __init__(self):
        self.tracer = DecisionTracer()
        self.causal_generator = CausalGraphGenerator()
        self.shap_explainer = SHAPExplainer()
        self.counterfactual_analyzer = CounterfactualAnalyzer()
        self.confidence_estimator = ConfidenceEstimator()
        self.report_builder = TransparencyReportBuilder()
        self.audit_interpreter = AuditLogInterpreter()
    
    def explain_decision(
        self,
        decision_id: str,
        decision_type: DecisionType,
        context: Dict[str, Any],
        model_fn: Callable,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate complete explanation for a decision."""
        
        # Start tracing
        trace_id = self.tracer.start_trace(decision_type, context)
        
        # Log decision step
        self.tracer.log_step(
            trace_id,
            component='decision_engine',
            action='make_decision',
            inputs=inputs,
            outputs=outputs,
            reasoning='Primary decision based on input analysis',
            confidence=0.85
        )
        
        # End trace
        trace = self.tracer.end_trace(trace_id, outputs)
        
        # Build causal graph
        causal_graph = self.causal_generator.build_graph(
            decision_id,
            inputs=inputs,
            intermediates={},
            outputs=outputs,
            trace_steps=trace.steps
        )
        
        # Generate SHAP explanation
        shap_explanation = self.shap_explainer.explain_prediction(
            model_fn,
            inputs
        )
        
        # Generate counterfactual
        counterfactual = self.counterfactual_analyzer.generate_counterfactual(
            model_fn,
            inputs,
            outputs
        )
        
        # Estimate confidence
        confidence = self.confidence_estimator.estimate_confidence(
            inputs,
            trace_steps=trace.steps
        )
        
        # Build transparency report
        report = self.report_builder.build_report(
            trace,
            causal_graph,
            shap_explanation,
            counterfactual,
            confidence
        )
        
        # Log for audit
        self.audit_interpreter.log_decision(
            decision_id,
            decision_type.value,
            user_id,
            inputs,
            outputs,
            confidence['overall_confidence'],
            shap_explanation.get('top_features', [])
        )
        
        return {
            'decision_id': decision_id,
            'trace': trace.to_dict(),
            'causal_graph': causal_graph,
            'shap_explanation': shap_explanation,
            'counterfactual': counterfactual,
            'confidence': confidence,
            'transparency_report': report,
            'summary': self._generate_summary(trace, confidence, shap_explanation)
        }
    
    def _generate_summary(
        self,
        trace: Any,
        confidence: Dict[str, Any],
        shap_explanation: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary."""
        decision_type = trace.decision_type
        conf_level = confidence['confidence_level']
        top_features = shap_explanation.get('top_features', [])[:3]
        
        summary = f"Decision type: {decision_type}. "
        summary += f"Confidence: {conf_level}. "
        
        if top_features:
            summary += f"Key factors: {', '.join(top_features)}. "
        
        summary += confidence.get('explanation', '')
        
        return summary
    
    def get_explanation(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Get explanation for a previously explained decision."""
        # Get trace
        trace = self.tracer.get_trace(decision_id)
        if not trace:
            return None
        
        # Get causal graph
        causal_graph = self.causal_generator.get_graph(decision_id)
        
        # Get audit trail
        audit_trail = self.audit_interpreter.get_decision_audit_trail(decision_id)
        
        return {
            'decision_id': decision_id,
            'trace': trace.to_dict() if trace else None,
            'causal_graph': causal_graph,
            'audit_trail': audit_trail
        }
    
    def explain_why(
        self,
        decision_id: str,
        question: str
    ) -> str:
        """Answer specific 'why' questions about a decision."""
        explanation = self.get_explanation(decision_id)
        if not explanation:
            return "Decision not found."
        
        question_lower = question.lower()
        
        if 'confidence' in question_lower:
            # Get confidence info from audit trail
            if explanation['audit_trail']:
                conf = explanation['audit_trail'][0].get('confidence', 0)
                return f"The confidence for this decision was {conf:.2f}."
        
        elif 'important' in question_lower or 'factor' in question_lower:
            # Get important factors from causal graph
            if explanation['causal_graph']:
                critical_path = self.causal_generator.get_critical_path(decision_id)
                return f"The most important factors were: {', '.join(critical_path)}"
        
        elif 'how' in question_lower:
            # Explain process
            trace = explanation['trace']
            if trace:
                num_steps = len(trace.get('steps', []))
                return f"The decision was made in {num_steps} steps, analyzing inputs and generating outputs."
        
        else:
            return "I can explain confidence levels, important factors, or the decision process. Please ask a more specific question."
    
    def compare_decisions(
        self,
        decision_id1: str,
        decision_id2: str
    ) -> Dict[str, Any]:
        """Compare two decisions."""
        exp1 = self.get_explanation(decision_id1)
        exp2 = self.get_explanation(decision_id2)
        
        if not exp1 or not exp2:
            return {'error': 'One or both decisions not found'}
        
        # Compare traces
        trace1 = exp1['trace']
        trace2 = exp2['trace']
        
        comparison = {
            'decision_ids': [decision_id1, decision_id2],
            'execution_time_diff': abs(
                trace1.get('execution_time_ms', 0) - trace2.get('execution_time_ms', 0)
            ),
            'confidence_diff': abs(
                exp1['audit_trail'][0].get('confidence', 0) - exp2['audit_trail'][0].get('confidence', 0)
            ) if exp1['audit_trail'] and exp2['audit_trail'] else 0,
            'summary': f"Decision {decision_id1} and {decision_id2} differ in execution time and confidence levels."
        }
        
        return comparison
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics across all explainability components."""
        return {
            'tracer': self.tracer.get_statistics(),
            'audit_logs': len(self.audit_interpreter.audit_logs),
            'causal_graphs': len(self.causal_generator.graphs),
            'shap_explanations': len(self.shap_explainer.explanations),
            'counterfactuals': len(self.counterfactual_analyzer.counterfactuals),
            'confidence_history': len(self.confidence_estimator.confidence_history),
            'transparency_reports': len(self.report_builder.reports)
        }
