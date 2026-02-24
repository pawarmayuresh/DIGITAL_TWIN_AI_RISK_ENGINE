"""
Explainability API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.core.explainable_ai.decision_logger import decision_logger
from backend.core.explainable_ai.shap_explainer import SHAPExplainer
from backend.evacuation_system.risk_model import risk_model

router = APIRouter(prefix="/api/explainability", tags=["explainability"])

# Global instances
_explanation_integrator = None
shap_explainer = SHAPExplainer()

# Set baseline for SHAP
shap_explainer.set_baseline({
    "water_level": 0.5,
    "rainfall": 10.0,
    "coastal_proximity": 0.0,
    "river_proximity": 0.0,
    "population_density": 500
})


class ExplainDecisionRequest(BaseModel):
    decision_id: str
    decision_type: str
    context: Dict[str, Any]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    user_id: Optional[str] = None


class WhyQuestionRequest(BaseModel):
    decision_id: str
    question: str


@router.get("/decisions/recent")
async def get_recent_decisions(limit: int = 50):
    """Get recent decisions"""
    decisions = decision_logger.get_recent_decisions(limit)
    stats = decision_logger.get_statistics()
    return {
        "decisions": decisions,
        "statistics": stats
    }


@router.get("/decisions/stats")
async def get_decision_statistics():
    """Get decision statistics"""
    return decision_logger.get_statistics()


@router.get("/decisions/ward/{ward_id}")
async def get_ward_decisions(ward_id: str):
    """Get decisions for specific ward"""
    decisions = decision_logger.get_decisions_by_ward(ward_id)
    return {"ward_id": ward_id, "decisions": decisions}


@router.post("/explain-risk")
async def explain_risk_prediction(features: Dict[str, Any]):
    """Explain risk prediction using SHAP values"""
    try:
        # Get risk prediction
        prediction = risk_model.predict(features)
        
        # Get SHAP explanation
        shap_explanation = shap_explainer.explain_prediction(
            model_fn=risk_model.predict,
            input_features=features
        )
        
        # Get detailed risk explanation
        risk_explanation = risk_model.explain_risk(features)
        
        # Get visualization data
        viz_data = shap_explainer.visualize_shap_values(shap_explanation)
        
        return {
            "status": "success",
            "prediction": prediction,
            "risk_explanation": risk_explanation,
            "shap_explanation": shap_explanation,
            "visualization": viz_data,
            "natural_language": shap_explainer.get_top_features_explanation(shap_explanation, top_n=3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/global-importance")
async def get_global_feature_importance():
    """Get global feature importance across all explanations"""
    try:
        # Get decisions from decision logger
        decisions = decision_logger.get_recent_decisions(limit=1000)
        
        if not decisions:
            return {
                "status": "success",
                "message": "No decisions available yet. Start evacuation simulation to generate data.",
                "feature_importance": {},
                "total_explanations": 0
            }
        
        # Aggregate feature contributions from all risk decisions
        feature_totals = {}
        feature_counts = {}
        
        for decision in decisions:
            if decision.get("decision_type") == "risk_assessment" and decision.get("feature_contributions"):
                for feature, value in decision["feature_contributions"].items():
                    if feature not in feature_totals:
                        feature_totals[feature] = 0
                        feature_counts[feature] = 0
                    feature_totals[feature] += abs(value)
                    feature_counts[feature] += 1
        
        if not feature_totals:
            return {
                "status": "success",
                "message": "No risk assessments with feature contributions yet",
                "feature_importance": {},
                "total_explanations": 0
            }
        
        # Calculate average importance and normalize to percentages
        total_importance = sum(feature_totals.values())
        feature_importance = {}
        
        if total_importance > 0:
            for feature in feature_totals:
                avg_contribution = feature_totals[feature] / feature_counts[feature]
                # Convert to percentage of total
                percentage = (feature_totals[feature] / total_importance) * 100
                feature_importance[feature] = percentage
        
        # Sort by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "status": "success",
            "feature_importance": dict(sorted_features),
            "total_explanations": len([d for d in decisions if d.get("decision_type") == "risk_assessment"]),
            "top_5_features": [f[0] for f in sorted_features[:5]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/counterfactual")
async def generate_counterfactual(features: Dict[str, Any], target_risk: float = 0.3):
    """Generate counterfactual: what changes would reduce risk below threshold"""
    try:
        from backend.core.explainable_ai.counterfactual_analyzer import CounterfactualAnalyzer
        
        analyzer = CounterfactualAnalyzer()
        
        # Filter out cache-busting and metadata parameters
        clean_features = {k: v for k, v in features.items() if not k.startswith('_')}
        
        # Get original prediction
        original_prediction = risk_model.predict(clean_features)
        original_risk = original_prediction["risk_score"]
        
        # Define target output
        target_output = {"risk_score": target_risk}
        
        # Generate counterfactual using clean features
        result = analyzer.generate_counterfactual(
            model_fn=risk_model.predict,
            original_input=clean_features,
            original_output=original_prediction,
            target_output=target_output,
            max_changes=3
        )
        
        if result.get("success"):
            # Add actionable recommendations
            changes = result["changes"]
            recommendations = []
            for feature, change_info in changes.items():
                if feature == "water_level":
                    recommendations.append(f"Improve drainage to reduce water level from {change_info['original']:.2f}m to {change_info['modified']:.2f}m")
                elif feature == "rainfall":
                    recommendations.append(f"If rainfall reduces from {change_info['original']:.1f}mm to {change_info['modified']:.1f}mm, risk decreases")
                elif feature == "population_density":
                    recommendations.append(f"Evacuate {int(change_info['original'] - change_info['modified'])} people to reduce risk")
            
            result["recommendations"] = recommendations
            result["risk_reduction"] = original_risk - result["counterfactual_output"]["risk_score"]
        
        return {
            "status": "success",
            "counterfactual": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decision-boundary")
async def explore_decision_boundary(features: Dict[str, Any], feature_name: str):
    """Explore how risk changes as a feature varies"""
    try:
        from backend.core.explainable_ai.counterfactual_analyzer import CounterfactualAnalyzer
        
        analyzer = CounterfactualAnalyzer()
        
        result = analyzer.explain_decision_boundary(
            model_fn=risk_model.predict,
            input_features=features,
            feature_name=feature_name,
            num_points=20
        )
        
        # Extract risk scores
        result["risk_scores"] = [r for r in result["outputs"]]
        
        return {
            "status": "success",
            "boundary_analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/causal-graph")
async def get_causal_graph():
    """Get causal graph for flood risk system"""
    try:
        # Return predefined causal structure for flood risk
        graph_data = {
            "nodes": [
                {"id": "rainfall", "label": "Rainfall", "type": "environmental", "importance": 0.8},
                {"id": "drainage", "label": "Drainage Capacity", "type": "infrastructure", "importance": 0.7},
                {"id": "water_level", "label": "Water Level", "type": "measured", "importance": 0.9},
                {"id": "flood_risk", "label": "Flood Risk", "type": "assessment", "importance": 1.0},
                {"id": "evacuation", "label": "Evacuation Decision", "type": "action", "importance": 1.0},
                {"id": "population", "label": "Population Density", "type": "demographic", "importance": 0.6},
                {"id": "casualties", "label": "Casualty Risk", "type": "impact", "importance": 0.8}
            ],
            "edges": [
                {"source": "rainfall", "target": "water_level", "type": "direct_cause", "strength": 0.7, "explanation": "Heavy rainfall increases water level"},
                {"source": "drainage", "target": "water_level", "type": "moderator", "strength": -0.5, "explanation": "Better drainage reduces water level"},
                {"source": "water_level", "target": "flood_risk", "type": "direct_cause", "strength": 0.8, "explanation": "Higher water level increases flood risk"},
                {"source": "flood_risk", "target": "evacuation", "type": "direct_cause", "strength": 0.9, "explanation": "High flood risk triggers evacuation"},
                {"source": "population", "target": "casualties", "type": "moderator", "strength": 0.6, "explanation": "Higher population increases potential casualties"},
                {"source": "flood_risk", "target": "casualties", "type": "direct_cause", "strength": 0.7, "explanation": "Flood risk directly impacts casualties"}
            ]
        }
        
        # Add intervention analysis
        interventions = {
            "improve_drainage": {
                "target": "drainage",
                "effect": "Reduces water_level by 30-50%, decreasing flood_risk",
                "cost": "High",
                "timeframe": "Long-term"
            },
            "early_warning": {
                "target": "evacuation",
                "effect": "Faster evacuation response, reduces casualties by 40%",
                "cost": "Medium",
                "timeframe": "Short-term"
            },
            "rainfall_management": {
                "target": "rainfall",
                "effect": "Cannot control, but can predict and prepare",
                "cost": "N/A",
                "timeframe": "N/A"
            }
        }
        
        return {
            "status": "success",
            "causal_graph": graph_data,
            "interventions": interventions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/causal-intervention")
async def analyze_causal_intervention(intervention: str, magnitude: float = 0.5):
    """Analyze effect of causal intervention"""
    try:
        # Simulate intervention effects
        interventions_map = {
            "improve_drainage": {
                "affected_feature": "water_level",
                "effect_multiplier": 1.0 - magnitude,  # Reduces water level
                "description": f"Improving drainage by {magnitude*100:.0f}% reduces water level"
            },
            "increase_capacity": {
                "affected_feature": "population_density",
                "effect_multiplier": 1.0 - magnitude,
                "description": f"Evacuating {magnitude*100:.0f}% of population"
            },
            "weather_control": {
                "affected_feature": "rainfall",
                "effect_multiplier": 1.0 - magnitude,
                "description": f"Reducing rainfall by {magnitude*100:.0f}%"
            }
        }
        
        if intervention not in interventions_map:
            raise HTTPException(status_code=400, detail="Unknown intervention")
        
        intervention_data = interventions_map[intervention]
        
        return {
            "status": "success",
            "intervention": intervention,
            "magnitude": magnitude,
            "effect": intervention_data,
            "recommendation": f"{intervention_data['description']} would reduce overall flood risk"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-path")
async def explain_evacuation_path(
    path: List[str],
    start_grid: str,
    end_grid: str
):
    """Explain why an evacuation path was selected"""
    try:
        from backend.core.explainable_ai.path_explainer import path_explainer
        
        # Mock path costs and avoided grids (in real system, get from pathfinder)
        path_costs = {grid_id: 0.3 + (i * 0.1) for i, grid_id in enumerate(path)}
        avoided_grids = [
            {"id": "X1", "risk_score": 0.85},
            {"id": "X2", "risk_score": 0.92}
        ]
        
        reason = f"Optimal path from {start_grid} to {end_grid} minimizing flood risk exposure"
        
        explanation = path_explainer.explain_path_selection(
            path=path,
            path_costs=path_costs,
            avoided_grids=avoided_grids,
            selected_reason=reason
        )
        
        return {
            "status": "success",
            "path_explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/path-risks/{path_id}")
async def get_path_risk_analysis(path_id: str):
    """Get detailed risk analysis for a path"""
    try:
        from backend.core.explainable_ai.path_explainer import path_explainer
        
        # Find path explanation
        path_exp = next((p for p in path_explainer.path_explanations if p["path_id"] == path_id), None)
        
        if not path_exp:
            raise HTTPException(status_code=404, detail="Path not found")
        
        return {
            "status": "success",
            "path_analysis": path_exp
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/uncertainty-analysis")
async def analyze_prediction_uncertainty(features: Dict[str, Any], noise_level: float = 0.1):
    """Analyze prediction uncertainty using Monte Carlo simulation"""
    try:
        from backend.core.explainable_ai.uncertainty_engine import uncertainty_engine
        
        # Filter out cache-busting and metadata parameters
        clean_features = {k: v for k, v in features.items() if not k.startswith('_')}
        
        result = uncertainty_engine.estimate_uncertainty(
            model_fn=risk_model.predict,
            input_features=clean_features,
            noise_level=noise_level
        )
        
        return {
            "status": "success",
            "uncertainty_analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sensor-reliability")
async def check_sensor_reliability(sensor_readings: List[float], sensor_type: str = "water_level"):
    """Check reliability of sensor data"""
    try:
        from backend.core.explainable_ai.uncertainty_engine import uncertainty_engine
        
        # Define expected ranges for different sensor types
        ranges = {
            "water_level": (0, 5),  # meters
            "rainfall": (0, 200),  # mm/hr
            "temperature": (-10, 50)  # celsius
        }
        
        expected_range = ranges.get(sensor_type, (0, 100))
        
        result = uncertainty_engine.estimate_sensor_reliability(
            sensor_readings=sensor_readings,
            expected_range=expected_range
        )
        
        return {
            "status": "success",
            "sensor_type": sensor_type,
            "reliability_analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/natural-language-explanation")
async def generate_natural_language_explanation(
    ward_id: str,
    explanation_type: str,
    data: Dict[str, Any]
):
    """Generate natural language explanation"""
    try:
        from backend.core.explainable_ai.nl_explainer import nl_explainer
        
        if explanation_type == "risk_decision":
            text = nl_explainer.explain_risk_decision(
                ward_id=ward_id,
                risk_score=data.get("risk_score", 0),
                features=data.get("features", {}),
                feature_contributions=data.get("feature_contributions", {}),
                action=data.get("action", "MONITOR")
            )
        elif explanation_type == "counterfactual":
            text = nl_explainer.explain_counterfactual(data)
        elif explanation_type == "path":
            text = nl_explainer.explain_path_selection(data)
        elif explanation_type == "uncertainty":
            text = nl_explainer.explain_uncertainty(data)
        else:
            raise HTTPException(status_code=400, detail="Unknown explanation type")
        
        return {
            "status": "success",
            "explanation_text": text
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/comprehensive-report")
async def generate_comprehensive_report(
    ward_id: str, 
    features: Dict[str, Any],
    disaster_type: str = "flood"  # Add disaster_type parameter
):
    """Generate comprehensive XAI report for a ward"""
    try:
        from backend.core.explainable_ai.nl_explainer import nl_explainer
        from backend.core.explainable_ai.counterfactual_analyzer import CounterfactualAnalyzer
        from backend.core.explainable_ai.uncertainty_engine import uncertainty_engine
        
        # Filter out cache-busting and metadata parameters
        clean_features = {k: v for k, v in features.items() if not k.startswith('_')}
        
        # Add disaster_type to features for detection
        clean_features['_disaster_type'] = disaster_type
        
        # Get risk assessment
        risk_prediction = risk_model.predict(clean_features)
        risk_explanation = risk_model.explain_risk(clean_features)
        
        # Get counterfactual
        analyzer = CounterfactualAnalyzer()
        counterfactual = analyzer.generate_counterfactual(
            model_fn=risk_model.predict,
            original_input=clean_features,
            original_output=risk_prediction,
            target_output={"risk_score": 0.3},
            max_changes=2
        )
        
        # Get uncertainty
        uncertainty = uncertainty_engine.estimate_uncertainty(
            model_fn=risk_model.predict,
            input_features=clean_features,
            noise_level=0.1
        )
        
        # Generate comprehensive report with disaster type
        report_text = nl_explainer.generate_summary_report(
            ward_id=ward_id,
            risk_data={
                "risk_score": risk_prediction["risk_score"],
                "features": clean_features,
                "feature_contributions": risk_explanation["feature_contributions"],
                "action": risk_explanation["recommended_action"]
            },
            counterfactual=counterfactual if counterfactual.get("success") else None,
            uncertainty=uncertainty,
            disaster_type=disaster_type  # Pass disaster type
        )
        
        return {
            "status": "success",
            "ward_id": ward_id,
            "disaster_type": disaster_type,
            "report": report_text,
            "structured_data": {
                "risk_assessment": risk_explanation,
                "counterfactual": counterfactual,
                "uncertainty": uncertainty
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_decision(request: ExplainDecisionRequest):
    """Generate complete explanation for a decision."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        # Simple model function for demo
        def model_fn(inputs):
            severity = inputs.get('disaster_severity', 0)
            return {'risk_score': severity * 10}
        
        from backend.core.explainable_ai.decision_tracer import DecisionType
        
        # Map string to DecisionType
        decision_type_map = {
            'evacuation': DecisionType.EVACUATION,
            'resource_allocation': DecisionType.RESOURCE_ALLOCATION,
            'infrastructure_repair': DecisionType.INFRASTRUCTURE_REPAIR,
            'coalition_formation': DecisionType.COALITION_FORMATION,
            'policy_selection': DecisionType.POLICY_SELECTION,
            'risk_assessment': DecisionType.RISK_ASSESSMENT
        }
        
        decision_type = decision_type_map.get(
            request.decision_type.lower(),
            DecisionType.RISK_ASSESSMENT
        )
        
        explanation = _explanation_integrator.explain_decision(
            request.decision_id,
            decision_type,
            request.context,
            model_fn,
            request.inputs,
            request.outputs,
            request.user_id
        )
        
        return {
            'status': 'success',
            'explanation': explanation
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/explanation/{decision_id}")
async def get_explanation(decision_id: str):
    """Get explanation for a previously explained decision."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        explanation = _explanation_integrator.get_explanation(decision_id)
        
        if explanation is None:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        return {
            'status': 'success',
            'explanation': explanation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/why")
async def explain_why(request: WhyQuestionRequest):
    """Answer specific 'why' questions about a decision."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        answer = _explanation_integrator.explain_why(
            request.decision_id,
            request.question
        )
        
        return {
            'status': 'success',
            'question': request.question,
            'answer': answer
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/{decision_id1}/{decision_id2}")
async def compare_decisions(decision_id1: str, decision_id2: str):
    """Compare two decisions."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        comparison = _explanation_integrator.compare_decisions(
            decision_id1,
            decision_id2
        )
        
        return {
            'status': 'success',
            'comparison': comparison
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trace/{trace_id}")
async def get_trace(trace_id: str):
    """Get decision trace."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        trace = _explanation_integrator.tracer.get_trace(trace_id)
        
        if trace is None:
            raise HTTPException(status_code=404, detail="Trace not found")
        
        return {
            'status': 'success',
            'trace': trace.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/causal-graph/{decision_id}")
async def get_causal_graph(decision_id: str):
    """Get causal graph for a decision."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        graph = _explanation_integrator.causal_generator.get_graph(decision_id)
        
        if graph is None:
            raise HTTPException(status_code=404, detail="Causal graph not found")
        
        return {
            'status': 'success',
            'graph': graph
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confidence/{decision_id}")
async def get_confidence(decision_id: str):
    """Get confidence assessment for a decision."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        # Get from audit logs
        audit_trail = _explanation_integrator.audit_interpreter.get_decision_audit_trail(decision_id)
        
        if not audit_trail:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        return {
            'status': 'success',
            'confidence': audit_trail[0].get('confidence', 0),
            'explanation': audit_trail[0].get('explanation', '')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit/logs")
async def get_audit_logs(limit: int = 10):
    """Get recent audit logs."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        logs = _explanation_integrator.audit_interpreter.audit_logs[-limit:]
        
        return {
            'status': 'success',
            'logs': logs,
            'total_logs': len(_explanation_integrator.audit_interpreter.audit_logs)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit/interpret")
async def interpret_audit_logs(
    decision_type: Optional[str] = None
):
    """Interpret audit logs and generate insights."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        interpretation = _explanation_integrator.audit_interpreter.interpret_logs(
            decision_type=decision_type
        )
        
        return {
            'status': 'success',
            'interpretation': interpretation
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{report_id}")
async def get_transparency_report(report_id: str):
    """Get transparency report."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        report = _explanation_integrator.report_builder.get_report(report_id)
        
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            'status': 'success',
            'report': report
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports")
async def list_transparency_reports(limit: int = 10):
    """List recent transparency reports."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        reports = _explanation_integrator.report_builder.list_reports(limit)
        
        return {
            'status': 'success',
            'reports': reports
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics():
    """Get explainability system statistics."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        stats = _explanation_integrator.get_statistics()
        
        return {
            'status': 'success',
            'statistics': stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualization/shap/{decision_id}")
async def get_shap_visualization(decision_id: str):
    """Get SHAP visualization data."""
    if _explanation_integrator is None:
        raise HTTPException(status_code=503, detail="Explainability system not initialized")
    
    try:
        # Get latest SHAP explanation
        if not _explanation_integrator.shap_explainer.explanations:
            raise HTTPException(status_code=404, detail="No SHAP explanations available")
        
        explanation = _explanation_integrator.shap_explainer.explanations[-1]
        viz_data = _explanation_integrator.shap_explainer.visualize_shap_values(explanation)
        
        return {
            'status': 'success',
            'visualization': viz_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def initialize_explainability_routes(explanation_integrator):
    """Initialize route dependencies."""
    global _explanation_integrator
    _explanation_integrator = explanation_integrator
