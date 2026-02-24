#!/usr/bin/env python3
"""
Batch 9 Validation Script - Explainable AI
Validates all explainability components are working correctly.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from core.explainable_ai import (
    DecisionTracer,
    DecisionType,
    CausalGraphGenerator,
    SHAPExplainer,
    CounterfactualAnalyzer,
    ConfidenceEstimator,
    TransparencyReportBuilder,
    AuditLogInterpreter,
    ExplanationIntegrator
)


def validate_decision_tracer():
    """Validate decision tracer functionality."""
    print("✓ Testing Decision Tracer...")
    
    tracer = DecisionTracer()
    
    # Test trace creation
    trace_id = tracer.start_trace(DecisionType.EVACUATION, {'disaster': 'earthquake'})
    assert trace_id is not None, "Failed to start trace"
    
    # Test step logging
    tracer.log_step(
        trace_id,
        component='test',
        action='test_action',
        inputs={'test': 1},
        outputs={'result': 2},
        reasoning='Test reasoning',
        confidence=0.9
    )
    
    # Test trace completion
    trace = tracer.end_trace(trace_id, {'final': 'decision'})
    assert len(trace.steps) == 1, "Failed to log step"
    assert trace.total_confidence > 0, "Invalid confidence"
    
    print("  ✓ Decision tracer validated")
    return True


def validate_causal_graph():
    """Validate causal graph generator."""
    print("✓ Testing Causal Graph Generator...")
    
    generator = CausalGraphGenerator()
    
    # Test graph building
    graph = generator.build_graph(
        'test_decision',
        inputs={'input1': 1, 'input2': 2},
        intermediates={'inter1': 3},
        outputs={'output1': 4}
    )
    
    assert 'nodes' in graph, "Missing nodes"
    assert 'edges' in graph, "Missing edges"
    assert len(graph['nodes']) > 0, "No nodes created"
    
    # Test critical path
    critical_path = generator.get_critical_path('test_decision')
    assert isinstance(critical_path, list), "Invalid critical path"
    
    print("  ✓ Causal graph generator validated")
    return True


def validate_shap_explainer():
    """Validate SHAP explainer."""
    print("✓ Testing SHAP Explainer...")
    
    explainer = SHAPExplainer()
    
    # Set baseline
    explainer.set_baseline({'feature1': 0, 'feature2': 0})
    
    # Define test model
    def model_fn(inputs):
        return {'output': inputs.get('feature1', 0) * 2}
    
    # Test explanation
    explanation = explainer.explain_prediction(
        model_fn,
        {'feature1': 5, 'feature2': 3}
    )
    
    assert 'shap_values' in explanation, "Missing SHAP values"
    assert 'top_features' in explanation, "Missing top features"
    
    print("  ✓ SHAP explainer validated")
    return True


def validate_counterfactual_analyzer():
    """Validate counterfactual analyzer."""
    print("✓ Testing Counterfactual Analyzer...")
    
    analyzer = CounterfactualAnalyzer()
    
    # Define test model
    def model_fn(inputs):
        val = inputs.get('value', 0)
        return {'result': 'high' if val > 5 else 'low'}
    
    # Test counterfactual generation
    counterfactual = analyzer.generate_counterfactual(
        model_fn,
        {'value': 7},
        {'result': 'high'}
    )
    
    assert 'success' in counterfactual, "Missing success field"
    
    print("  ✓ Counterfactual analyzer validated")
    return True


def validate_confidence_estimator():
    """Validate confidence estimator."""
    print("✓ Testing Confidence Estimator...")
    
    estimator = ConfidenceEstimator()
    
    # Test confidence estimation
    confidence = estimator.estimate_confidence(
        decision_data={
            'disaster_severity': 7.5,
            'infrastructure_health': 75,
            'casualties': 50
        }
    )
    
    assert 'overall_confidence' in confidence, "Missing overall confidence"
    assert 'confidence_level' in confidence, "Missing confidence level"
    assert 0 <= confidence['overall_confidence'] <= 1, "Invalid confidence value"
    
    # Test suggestions
    suggestions = estimator.suggest_improvements(confidence)
    assert isinstance(suggestions, list), "Invalid suggestions"
    
    print("  ✓ Confidence estimator validated")
    return True


def validate_transparency_report():
    """Validate transparency report builder."""
    print("✓ Testing Transparency Report Builder...")
    
    builder = TransparencyReportBuilder()
    
    # Create mock data
    from core.explainable_ai.decision_tracer import DecisionTrace, DecisionStep
    
    trace = DecisionTrace(
        trace_id='test_trace',
        decision_type='test',
        timestamp='2026-02-18T14:00:00',
        context={},
        steps=[],
        final_decision={},
        total_confidence=0.8,
        execution_time_ms=100.0
    )
    
    # Test report building
    report = builder.build_report(
        trace,
        {'nodes': [], 'edges': []},
        {'top_features': [], 'feature_contributions': {}},
        {'success': False},
        {'overall_confidence': 0.8, 'confidence_level': 'high', 'confidence_factors': {}, 'explanation': ''}
    )
    
    assert 'report_id' in report, "Missing report ID"
    assert 'decision_summary' in report, "Missing decision summary"
    assert 'recommendations' in report, "Missing recommendations"
    
    print("  ✓ Transparency report builder validated")
    return True


def validate_audit_log_interpreter():
    """Validate audit log interpreter."""
    print("✓ Testing Audit Log Interpreter...")
    
    interpreter = AuditLogInterpreter()
    
    # Test logging
    interpreter.log_decision(
        'test_decision',
        'test_type',
        'test_user',
        {'input': 1},
        {'output': 2},
        0.85,
        'Test explanation'
    )
    
    assert len(interpreter.audit_logs) == 1, "Failed to log decision"
    
    # Test interpretation
    interpretation = interpreter.interpret_logs()
    assert 'decision_statistics' in interpretation, "Missing statistics"
    assert 'compliance_status' in interpretation, "Missing compliance status"
    
    print("  ✓ Audit log interpreter validated")
    return True


def validate_explanation_integrator():
    """Validate explanation integrator."""
    print("✓ Testing Explanation Integrator...")
    
    integrator = ExplanationIntegrator()
    
    # Define test model
    def model_fn(inputs):
        return {'output': inputs.get('value', 0) * 2}
    
    # Test integrated explanation
    explanation = integrator.explain_decision(
        'test_integrated',
        DecisionType.RISK_ASSESSMENT,
        {'test': 'context'},
        model_fn,
        {'value': 5},
        {'output': 10}
    )
    
    assert 'decision_id' in explanation, "Missing decision ID"
    assert 'trace' in explanation, "Missing trace"
    assert 'confidence' in explanation, "Missing confidence"
    assert 'summary' in explanation, "Missing summary"
    
    # Test statistics
    stats = integrator.get_statistics()
    assert isinstance(stats, dict), "Invalid statistics"
    
    print("  ✓ Explanation integrator validated")
    return True


def run_all_validations():
    """Run all validation tests."""
    print("\n" + "="*60)
    print("BATCH 9 VALIDATION - EXPLAINABLE AI")
    print("="*60 + "\n")
    
    tests = [
        ("Decision Tracer", validate_decision_tracer),
        ("Causal Graph", validate_causal_graph),
        ("SHAP Explainer", validate_shap_explainer),
        ("Counterfactual Analyzer", validate_counterfactual_analyzer),
        ("Confidence Estimator", validate_confidence_estimator),
        ("Transparency Report", validate_transparency_report),
        ("Audit Log Interpreter", validate_audit_log_interpreter),
        ("Explanation Integrator", validate_explanation_integrator)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ {test_name} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"VALIDATION COMPLETE: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_validations()
    sys.exit(0 if success else 1)
