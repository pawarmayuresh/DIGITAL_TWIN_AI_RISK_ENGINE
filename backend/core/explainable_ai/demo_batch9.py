"""
Batch 9 Demo - Explainable AI
Demonstrates transparent and interpretable AI decisions.
"""

from .decision_tracer import DecisionTracer, DecisionType
from .causal_graph import CausalGraphGenerator
from .shap_explainer import SHAPExplainer
from .counterfactual_analyzer import CounterfactualAnalyzer
from .confidence_estimator import ConfidenceEstimator
from .transparency_report import TransparencyReportBuilder
from .audit_log_interpreter import AuditLogInterpreter
from .explanation_integrator import ExplanationIntegrator


def demo_decision_tracer():
    """Demo: Decision tracing."""
    print("\n=== Decision Tracer Demo ===")
    
    tracer = DecisionTracer()
    
    # Start trace
    trace_id = tracer.start_trace(
        DecisionType.EVACUATION,
        context={'disaster': 'earthquake', 'severity': 7.5}
    )
    print(f"Started trace: {trace_id}")
    
    # Log steps
    tracer.log_step(
        trace_id,
        component='risk_assessor',
        action='assess_risk',
        inputs={'severity': 7.5, 'population': 100000},
        outputs={'risk_level': 'high'},
        reasoning='High severity earthquake requires immediate action',
        confidence=0.9
    )
    
    tracer.log_step(
        trace_id,
        component='resource_allocator',
        action='allocate_resources',
        inputs={'risk_level': 'high'},
        outputs={'resources': 5000, 'zones': ['A', 'B']},
        reasoning='Allocate maximum resources to high-risk zones',
        confidence=0.85
    )
    
    # End trace
    trace = tracer.end_trace(
        trace_id,
        final_decision={'action': 'evacuate', 'zones': ['A', 'B'], 'resources': 5000}
    )
    
    print(f"Trace completed with {len(trace.steps)} steps")
    print(f"Total confidence: {trace.total_confidence:.2f}")
    print(f"Execution time: {trace.execution_time_ms:.2f} ms")
    
    # Get statistics
    stats = tracer.get_statistics()
    print(f"Tracer statistics: {stats}")
    
    return tracer


def demo_causal_graph():
    """Demo: Causal graph generation."""
    print("\n=== Causal Graph Demo ===")
    
    generator = CausalGraphGenerator()
    
    # Build graph
    graph = generator.build_graph(
        decision_id='decision_001',
        inputs={
            'disaster_severity': 7.5,
            'population': 100000,
            'infrastructure_health': 75
        },
        intermediates={
            'risk_level': 'high',
            'resource_needs': 5000
        },
        outputs={
            'action': 'evacuate',
            'zones': ['A', 'B']
        }
    )
    
    print(f"Graph created with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
    
    # Get critical path
    critical_path = generator.get_critical_path('decision_001')
    print(f"Critical path: {critical_path}")
    
    return generator


def demo_shap_explainer():
    """Demo: SHAP feature importance."""
    print("\n=== SHAP Explainer Demo ===")
    
    explainer = SHAPExplainer()
    
    # Set baseline
    explainer.set_baseline({
        'disaster_severity': 5.0,
        'population': 50000,
        'infrastructure_health': 100
    })
    
    # Define simple model
    def model_fn(inputs):
        severity = inputs.get('disaster_severity', 0)
        population = inputs.get('population', 0)
        infra = inputs.get('infrastructure_health', 100)
        
        # Simple risk score
        risk_score = (severity * 10) + (population / 10000) - (infra / 10)
        return {'risk_score': risk_score}
    
    # Explain prediction
    explanation = explainer.explain_prediction(
        model_fn,
        {
            'disaster_severity': 7.5,
            'population': 100000,
            'infrastructure_health': 75
        }
    )
    
    print(f"SHAP values: {explanation['shap_values']}")
    print(f"Top features: {explanation['top_features']}")
    
    # Get natural language explanation
    top_exp = explainer.get_top_features_explanation(explanation, top_n=3)
    print(f"Explanation: {top_exp}")
    
    return explainer


def demo_counterfactual():
    """Demo: Counterfactual analysis."""
    print("\n=== Counterfactual Analyzer Demo ===")
    
    analyzer = CounterfactualAnalyzer()
    
    # Define model
    def model_fn(inputs):
        severity = inputs.get('disaster_severity', 0)
        if severity > 7.0:
            return {'action': 'evacuate'}
        else:
            return {'action': 'monitor'}
    
    # Generate counterfactual
    original_input = {'disaster_severity': 7.5, 'population': 100000}
    original_output = model_fn(original_input)
    
    counterfactual = analyzer.generate_counterfactual(
        model_fn,
        original_input,
        original_output,
        features_to_change=['disaster_severity']
    )
    
    if counterfactual.get('success'):
        print(f"Counterfactual found with {counterfactual['num_changes']} changes")
        print(f"Changes: {counterfactual['changes']}")
        print(f"Explanation: {counterfactual['explanation']}")
    else:
        print("No counterfactual found")
    
    return analyzer


def demo_confidence_estimator():
    """Demo: Confidence estimation."""
    print("\n=== Confidence Estimator Demo ===")
    
    estimator = ConfidenceEstimator()
    
    # Estimate confidence
    confidence = estimator.estimate_confidence(
        decision_data={
            'disaster_severity': 7.5,
            'infrastructure_health': 75,
            'casualties': 50,
            'resources_available': 5000,
            'time_step': 5
        }
    )
    
    print(f"Overall confidence: {confidence['overall_confidence']:.2f}")
    print(f"Confidence level: {confidence['confidence_level']}")
    print(f"Explanation: {confidence['explanation']}")
    
    # Get suggestions
    suggestions = estimator.suggest_improvements(confidence)
    print(f"Suggestions: {suggestions}")
    
    return estimator


def demo_transparency_report():
    """Demo: Transparency report generation."""
    print("\n=== Transparency Report Demo ===")
    
    builder = TransparencyReportBuilder()
    
    # Create mock data
    from .decision_tracer import DecisionTrace, DecisionStep
    
    trace = DecisionTrace(
        trace_id='trace_001',
        decision_type='evacuation',
        timestamp='2026-02-18T14:00:00',
        context={'disaster': 'earthquake'},
        steps=[
            DecisionStep(
                step_id='step_1',
                timestamp='2026-02-18T14:00:01',
                component='risk_assessor',
                action='assess',
                inputs={},
                outputs={},
                reasoning='Assess risk',
                confidence=0.9
            )
        ],
        final_decision={'action': 'evacuate'},
        total_confidence=0.85,
        execution_time_ms=150.0
    )
    
    causal_graph = {'nodes': [], 'edges': [], 'metadata': {}}
    shap_explanation = {'top_features': ['disaster_severity', 'population'], 'feature_contributions': {}}
    counterfactual = {'success': True, 'num_changes': 1, 'changes': {}, 'explanation': 'Test'}
    confidence = {'overall_confidence': 0.85, 'confidence_level': 'high', 'confidence_factors': {}, 'explanation': 'Good'}
    
    # Build report
    report = builder.build_report(
        trace,
        causal_graph,
        shap_explanation,
        counterfactual,
        confidence
    )
    
    print(f"Report ID: {report['report_id']}")
    print(f"Recommendations: {report['recommendations']}")
    
    return builder


def demo_audit_log():
    """Demo: Audit log interpretation."""
    print("\n=== Audit Log Interpreter Demo ===")
    
    interpreter = AuditLogInterpreter()
    
    # Log some decisions
    for i in range(5):
        interpreter.log_decision(
            decision_id=f'decision_{i}',
            decision_type='evacuation',
            user_id='user_001',
            inputs={'severity': 7.0 + i * 0.5},
            outputs={'action': 'evacuate'},
            confidence=0.8 + i * 0.02,
            explanation=f'Decision {i} explanation'
        )
    
    # Interpret logs
    interpretation = interpreter.interpret_logs()
    
    print(f"Analyzed {interpretation['num_logs_analyzed']} logs")
    print(f"Decision statistics: {interpretation['decision_statistics']}")
    print(f"Compliance status: {interpretation['compliance_status']['status']}")
    
    # Generate audit report
    audit_report = interpreter.generate_audit_report(interpretation['interpretation_id'])
    print(f"Audit report: {audit_report['summary']}")
    
    return interpreter


def demo_explanation_integrator():
    """Demo: Integrated explanation system."""
    print("\n=== Explanation Integrator Demo ===")
    
    integrator = ExplanationIntegrator()
    
    # Define simple model
    def model_fn(inputs):
        severity = inputs.get('disaster_severity', 0)
        return {'risk_score': severity * 10}
    
    # Explain decision
    explanation = integrator.explain_decision(
        decision_id='integrated_001',
        decision_type=DecisionType.EVACUATION,
        context={'disaster': 'earthquake'},
        model_fn=model_fn,
        inputs={'disaster_severity': 7.5, 'population': 100000},
        outputs={'action': 'evacuate'},
        user_id='demo_user'
    )
    
    print(f"Decision ID: {explanation['decision_id']}")
    print(f"Summary: {explanation['summary']}")
    print(f"Confidence: {explanation['confidence']['confidence_level']}")
    
    # Ask why
    why_answer = integrator.explain_why('integrated_001', 'Why was this decision made?')
    print(f"Why answer: {why_answer}")
    
    # Get statistics
    stats = integrator.get_statistics()
    print(f"System statistics: {stats}")
    
    return integrator


def run_all_demos():
    """Run all Batch 9 demos."""
    print("\n" + "="*60)
    print("BATCH 9 - EXPLAINABLE AI DEMONSTRATIONS")
    print("="*60)
    
    # Run individual demos
    tracer = demo_decision_tracer()
    generator = demo_causal_graph()
    explainer = demo_shap_explainer()
    analyzer = demo_counterfactual()
    estimator = demo_confidence_estimator()
    builder = demo_transparency_report()
    interpreter = demo_audit_log()
    integrator = demo_explanation_integrator()
    
    print("\n" + "="*60)
    print("BATCH 9 COMPLETE - FULLY EXPLAINABLE AI DECISIONS")
    print("="*60)
    
    return {
        'tracer': tracer,
        'causal_generator': generator,
        'shap_explainer': explainer,
        'counterfactual_analyzer': analyzer,
        'confidence_estimator': estimator,
        'report_builder': builder,
        'audit_interpreter': interpreter,
        'integrator': integrator
    }


if __name__ == "__main__":
    run_all_demos()
