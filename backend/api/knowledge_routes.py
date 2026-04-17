"""
Knowledge Representation API Routes - INTEGRATED WITH REAL-TIME MUMBAI DATA
Exposes Propositional Logic, FOL, SOL, Inference, and Planning using live data
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
import pandas as pd
import os

from backend.core.knowledge_engine import (
    KnowledgeBase, Predicate, InferenceEngine,
    Action, Planner, HeuristicPlanner, HierarchicalPlanner, HierarchicalTask,
    SymbolicLogicEngine, LogicProgram, analyze_with_expert_system, analyze_ward_expert_system
)
from sympy import And, Implies

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# Global knowledge base instance
kb = KnowledgeBase()
inference_engine = InferenceEngine(kb)


def load_realtime_data():
    """Load real-time data from Mumbai sensors and infrastructure"""
    data = {}
    
    try:
        # Load rainfall data
        rain_file = "data/mumbai/realtime/rain_sensors.csv"
        if os.path.exists(rain_file):
            df = pd.read_csv(rain_file)
            data['rainfall'] = df.to_dict('records')
        
        # Load water level data
        water_file = "data/mumbai/realtime/water_level_sensors.csv"
        if os.path.exists(water_file):
            df = pd.read_csv(water_file)
            data['water_levels'] = df.to_dict('records')
        
        # Load traffic data
        traffic_file = "data/mumbai/realtime/traffic_density.csv"
        if os.path.exists(traffic_file):
            df = pd.read_csv(traffic_file)
            data['traffic'] = df.to_dict('records')
        
        # Load infrastructure status
        infra_file = "data/mumbai/static/infrastructure_nodes_probabilistic.csv"
        if os.path.exists(infra_file):
            df = pd.read_csv(infra_file)
            data['infrastructure'] = df.to_dict('records')
            
    except Exception as e:
        print(f"Error loading real-time data: {e}")
    
    return data


@router.get("/realtime/analyze")
async def analyze_realtime_data():
    """
    Analyze real-time Mumbai data using knowledge representation
    Applies propositional logic, FOL, and inference to live data
    """
    global kb, inference_engine
    
    # Reset knowledge base
    kb = KnowledgeBase()
    inference_engine = InferenceEngine(kb)
    
    # Load real-time data
    data = load_realtime_data()
    
    # PROPOSITIONAL LOGIC - Analyze conditions
    rainfall_data = data.get('rainfall', [])
    water_data = data.get('water_levels', [])
    traffic_data = data.get('traffic', [])
    infra_data = data.get('infrastructure', [])
    
    # Calculate averages
    avg_rainfall = sum(r.get('rainfall_mm', 0) for r in rainfall_data) / len(rainfall_data) if rainfall_data else 0
    avg_water = sum(w.get('water_level_m', 0) for w in water_data) / len(water_data) if water_data else 0
    avg_traffic = sum(t.get('density', 0) for t in traffic_data) / len(traffic_data) if traffic_data else 0
    
    # Add propositional facts based on thresholds
    if avg_rainfall > 50:
        kb.add_fact("heavy_rainfall")
    if avg_water > 2.0:
        kb.add_fact("high_water_level")
    if avg_traffic > 0.7:
        kb.add_fact("traffic_congestion")
    
    # Count infrastructure failures
    failed_infra = sum(1 for i in infra_data if i.get('Initial_Failed', 0) > 0.5)
    if failed_infra > 2:
        kb.add_fact("infrastructure_failures")
    
    # Add propositional rules
    kb.add_rule(
        ["heavy_rainfall", "high_water_level"],
        "flooding_risk",
        "Flooding_Detection_Rule"
    )
    kb.add_rule(
        ["flooding_risk", "traffic_congestion"],
        "evacuation_needed",
        "Evacuation_Trigger_Rule"
    )
    kb.add_rule(
        ["evacuation_needed", "infrastructure_failures"],
        "emergency_declared",
        "Emergency_Declaration_Rule"
    )
    
    # Run forward chaining
    inference_engine.forward_chain()
    
    # FIRST-ORDER LOGIC - Ward-specific analysis
    ward_analysis = {}
    
    for rain in rainfall_data[:5]:  # Analyze first 5 wards
        ward = rain.get('ward_id', 'Unknown')
        rainfall_mm = rain.get('rainfall_mm', 0)
        
        # Add FOL predicates
        if rainfall_mm > 50:
            kb.add_fact(Predicate("HeavyRainfall", ward))
        
        # Find water level for same ward
        ward_water = next((w for w in water_data if w.get('ward_id') == ward), None)
        if ward_water and ward_water.get('water_level_m', 0) > 2.0:
            kb.add_fact(Predicate("HighWaterLevel", ward))
        
        # Add FOL rules for this ward
        kb.add_rule(
            [Predicate("HeavyRainfall", ward), Predicate("HighWaterLevel", ward)],
            Predicate("FloodRisk", ward),
            f"FOL_Flood_Rule_{ward}"
        )
        
        ward_analysis[ward] = {
            "rainfall_mm": rainfall_mm,
            "water_level_m": ward_water.get('water_level_m', 0) if ward_water else 0
        }
    
    # Run forward chaining again with FOL
    inference_engine.forward_chain()
    
    # SECOND-ORDER LOGIC - Meta-reasoning
    for ward in ward_analysis.keys():
        inference_engine.second_order_reasoning(ward)
    
    # PLANNING - Generate action plan if emergency
    plan = None
    if kb.has_fact("emergency_declared"):
        actions = [
            Action("ActivateEmergencyServices", ["emergency_declared"], ["services_active"], cost=1),
            Action("IssueEvacuationOrder", ["services_active"], ["evacuation_ordered"], cost=2),
            Action("DeployRescueTeams", ["evacuation_ordered"], ["rescue_deployed"], cost=3),
            Action("EstablishShelters", ["rescue_deployed"], ["shelters_ready"], cost=2)
        ]
        
        planner = HeuristicPlanner(actions)
        plan = planner.plan({"emergency_declared"}, "shelters_ready")
    
    return {
        "success": True,
        "timestamp": pd.Timestamp.now().isoformat(),
        "data_sources": {
            "rainfall_sensors": len(rainfall_data),
            "water_sensors": len(water_data),
            "traffic_sensors": len(traffic_data),
            "infrastructure_nodes": len(infra_data)
        },
        "metrics": {
            "avg_rainfall_mm": round(avg_rainfall, 2),
            "avg_water_level_m": round(avg_water, 2),
            "avg_traffic_density": round(avg_traffic, 2),
            "failed_infrastructure": failed_infra
        },
        "propositional_logic": {
            "facts": [str(f) for f in kb.facts if isinstance(f, str)],
            "rules": [r["name"] for r in kb.rules if isinstance(r["conclusion"], str)]
        },
        "first_order_logic": {
            "predicates": [str(f) for f in kb.facts if isinstance(f, Predicate)],
            "ward_analysis": ward_analysis
        },
        "inference_trace": kb.inference_trace,
        "emergency_plan": plan,
        "state": kb.get_state_dict()
    }


@router.get("/realtime/ward/{ward_id}")
async def analyze_ward_realtime(ward_id: str):
    """
    Analyze specific ward using real-time data and logical reasoning
    """
    global kb, inference_engine
    
    kb = KnowledgeBase()
    inference_engine = InferenceEngine(kb)
    
    data = load_realtime_data()
    
    # Find ward-specific data
    ward_rain = next((r for r in data.get('rainfall', []) if r.get('ward_id') == ward_id), None)
    ward_water = next((w for w in data.get('water_levels', []) if w.get('ward_id') == ward_id), None)
    ward_traffic = next((t for t in data.get('traffic', []) if t.get('ward_id') == ward_id), None)
    
    # Add FOL facts for this ward
    if ward_rain and ward_rain.get('rainfall_mm', 0) > 50:
        kb.add_fact(Predicate("HeavyRainfall", ward_id))
    
    if ward_water and ward_water.get('water_level_m', 0) > 2.0:
        kb.add_fact(Predicate("HighWaterLevel", ward_id))
    
    if ward_traffic and ward_traffic.get('density', 0) > 0.7:
        kb.add_fact(Predicate("TrafficCongestion", ward_id))
    
    # Add FOL rules
    kb.add_rule(
        [Predicate("HeavyRainfall", ward_id), Predicate("HighWaterLevel", ward_id)],
        Predicate("FloodRisk", ward_id),
        f"Flood_Rule_{ward_id}"
    )
    
    kb.add_rule(
        [Predicate("FloodRisk", ward_id), Predicate("TrafficCongestion", ward_id)],
        Predicate("EvacuationDifficult", ward_id),
        f"Evacuation_Rule_{ward_id}"
    )
    
    # Run inference
    inference_engine.forward_chain()
    inference_engine.second_order_reasoning(ward_id)
    
    # Check if evacuation needed (backward chaining)
    evacuation_needed = inference_engine.backward_chain(Predicate("EvacuationDifficult", ward_id))
    
    # Generate action plan if needed
    plan = None
    if evacuation_needed:
        actions = [
            Action("ClearTrafficRoutes", [f"traffic_{ward_id}"], [f"routes_clear_{ward_id}"], cost=2),
            Action("DeployBoats", [f"routes_clear_{ward_id}"], [f"boats_ready_{ward_id}"], cost=3),
            Action("EvacuateResidents", [f"boats_ready_{ward_id}"], [f"residents_safe_{ward_id}"], cost=4)
        ]
        
        planner = Planner(actions)
        plan = planner.plan({f"traffic_{ward_id}"}, f"residents_safe_{ward_id}")
    
    return {
        "success": True,
        "ward_id": ward_id,
        "realtime_data": {
            "rainfall_mm": ward_rain.get('rainfall_mm', 0) if ward_rain else 0,
            "water_level_m": ward_water.get('water_level_m', 0) if ward_water else 0,
            "traffic_density": ward_traffic.get('density', 0) if ward_traffic else 0
        },
        "logical_reasoning": {
            "facts": [str(f) for f in kb.facts],
            "rules_triggered": [t["rule_name"] for t in kb.inference_trace if t.get("rule_name")],
            "evacuation_needed": evacuation_needed
        },
        "inference_trace": kb.inference_trace,
        "action_plan": plan,
        "state": kb.get_state_dict()
    }


@router.post("/realtime/continuous")
async def start_continuous_reasoning():
    """
    Start continuous real-time reasoning
    This endpoint demonstrates how the system continuously monitors and reasons
    """
    results = []
    
    for i in range(5):  # Simulate 5 time steps
        result = await analyze_realtime_data()
        results.append({
            "timestep": i + 1,
            "analysis": result
        })
    
    return {
        "success": True,
        "message": "Continuous reasoning completed",
        "timesteps": len(results),
        "results": results
    }


# Keep original demo endpoints for comparison
@router.get("/demo/static")
async def run_static_demo():
    """Run static demo (for comparison with real-time)"""
    global kb, inference_engine
    
    kb = KnowledgeBase()
    inference_engine = InferenceEngine(kb)
    
    # Static example
    kb.add_fact("unemployment_high")
    kb.add_fact("inflation_high")
    kb.add_rule(["unemployment_high", "inflation_high"], "social_unrest", "Economic_Rule")
    
    inference_engine.forward_chain()
    
    return {
        "success": True,
        "type": "static_demo",
        "state": kb.get_state_dict()
    }


@router.post("/reset")
async def reset_knowledge_base():
    """Reset the knowledge base"""
    global kb, inference_engine
    
    kb = KnowledgeBase()
    inference_engine = InferenceEngine(kb)
    
    return {
        "success": True,
        "message": "Knowledge base reset"
    }


@router.get("/realtime/quick")
async def quick_realtime_analysis(disaster_type: str = "flood"):
    """
    OPTIMIZED: Quick real-time analysis using expert system
    Lightweight and fast - processes only aggregated data
    """
    try:
        data = load_realtime_data()
        
        # Calculate quick aggregates based on disaster type
        rainfall_data = data.get('rainfall', [])
        water_data = data.get('water_levels', [])
        traffic_data = data.get('traffic', [])
        infra_data = data.get('infrastructure', [])
        
        avg_rainfall = sum(r.get('rainfall_mm', 0) for r in rainfall_data) / max(len(rainfall_data), 1)
        avg_water = sum(w.get('water_level_m', 0) for w in water_data) / max(len(water_data), 1)
        avg_traffic = sum(t.get('density', 0) for t in traffic_data) / max(len(traffic_data), 1)
        failed_infra = sum(1 for i in infra_data if i.get('Initial_Failed', 0) > 0.5)
        
        # Generate disaster-specific sensor data
        import random
        import numpy as np
        
        if disaster_type == "fire":
            # Simulate fire conditions with HIGH variability to trigger rules
            temperature = 30 + random.uniform(15, 25)  # 45-55°C (will trigger extreme heat)
            wind_speed = 20 + random.uniform(20, 30)   # 40-50 km/h (will trigger high wind)
            humidity = random.uniform(15, 45)          # 15-45% (often triggers low humidity)
            
            expert_data = {
                'temperature': temperature,
                'wind_speed': wind_speed,
                'humidity': humidity,
                'failed_infrastructure': failed_infra
            }
            
            metrics = {
                "temperature_celsius": round(temperature, 1),
                "wind_speed_kmh": round(wind_speed, 1),
                "humidity_percent": round(humidity, 1),
                "failed_infrastructure": failed_infra
            }
            
        elif disaster_type == "contamination":
            # Simulate contamination conditions with HIGH values
            air_quality = random.uniform(150, 450)     # AQI 150-450 (often severe)
            water_contam = random.uniform(0.3, 0.95)   # 0.3-0.95 contamination level
            chemical = random.uniform(0.2, 0.8)        # 0.2-0.8 chemical level
            
            expert_data = {
                'air_quality_index': air_quality,
                'water_contamination': water_contam,
                'chemical_level': chemical,
                'failed_infrastructure': failed_infra
            }
            
            metrics = {
                "air_quality_index": round(air_quality, 0),
                "water_contamination_level": round(water_contam, 2),
                "chemical_level": round(chemical, 2),
                "failed_infrastructure": failed_infra
            }
            
        else:  # flood (default)
            expert_data = {
                'rainfall': avg_rainfall,
                'water_level': avg_water,
                'traffic_density': avg_traffic,
                'failed_infrastructure': failed_infra
            }
            
            metrics = {
                "avg_rainfall_mm": round(avg_rainfall, 2),
                "avg_water_level_m": round(avg_water, 2),
                "avg_traffic_density": round(avg_traffic, 2),
                "failed_infrastructure": failed_infra
            }
        
        # Run expert system analysis
        expert_result = analyze_with_expert_system(expert_data, disaster_type=disaster_type)
        
        # Run symbolic logic for consistency check
        symbolic_engine = SymbolicLogicEngine()
        heavy_rain = symbolic_engine.define_proposition("heavy_rain")
        high_water = symbolic_engine.define_proposition("high_water")
        flood_risk = symbolic_engine.define_proposition("flood_risk")
        
        # Create implication: (heavy_rain AND high_water) -> flood_risk
        expr = Implies(And(heavy_rain, high_water), flood_risk)
        
        # Check if consistent with current values
        if disaster_type == "flood":
            current_values = {
                "heavy_rain": avg_rainfall > 50,
                "high_water": avg_water > 2.0,
                "flood_risk": avg_rainfall > 50 and avg_water > 2.0
            }
        elif disaster_type == "fire":
            current_values = {
                "heavy_rain": False,
                "high_water": False,
                "flood_risk": False
            }
        else:  # contamination
            current_values = {
                "heavy_rain": False,
                "high_water": False,
                "flood_risk": False
            }
        
        consistency = symbolic_engine.evaluate(expr, current_values)
        
        return {
            "success": True,
            "timestamp": pd.Timestamp.now().isoformat(),
            "disaster_type": disaster_type,
            "metrics": metrics,
            "expert_system": {
                "risk_level": expert_result["risk_level"],
                "total_rules_fired": expert_result["total_rules"],
                "rules": expert_result["rules_fired"][:5],  # Top 5 rules
                "decisions": expert_result["decisions"]
            },
            "symbolic_logic": {
                "consistent": consistency,
                "propositions": current_values
            },
            "data_sources": {
                "rainfall_sensors": len(rainfall_data),
                "water_sensors": len(water_data),
                "traffic_sensors": len(traffic_data),
                "infrastructure_nodes": len(infra_data)
            }
        }
    except Exception as e:
        import traceback
        print(f"ERROR in quick_realtime_analysis: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/realtime/ward-quick/{ward_id:path}")
async def quick_ward_analysis(ward_id: str, disaster_type: str = "flood"):
    """
    OPTIMIZED: Quick ward analysis using expert system
    Fast single-ward analysis
    """
    data = load_realtime_data()
    
    # Find ward-specific data
    ward_rain = next((r for r in data.get('rainfall', []) if r.get('ward_id') == ward_id), None)
    ward_water = next((w for w in data.get('water_levels', []) if w.get('ward_id') == ward_id), None)
    ward_traffic = next((t for t in data.get('traffic', []) if t.get('ward_id') == ward_id), None)
    
    # Count infrastructure failures in ward
    ward_infra = [i for i in data.get('infrastructure', []) if i.get('ward_id') == ward_id]
    failed_infra = sum(1 for i in ward_infra if i.get('Initial_Failed', 0) > 0.5)
    
    # Generate disaster-specific data
    import random
    
    if disaster_type == "fire":
        temperature = 30 + random.uniform(15, 25)  # 45-55°C
        wind_speed = 20 + random.uniform(20, 30)   # 40-50 km/h
        humidity = random.uniform(15, 45)          # 15-45%
        
        ward_data = {
            'temperature': temperature,
            'wind_speed': wind_speed,
            'humidity': humidity,
            'failed_infrastructure': failed_infra
        }
        
        sensor_data = {
            'temperature': round(temperature, 1),
            'wind_speed': round(wind_speed, 1),
            'humidity': round(humidity, 1),
            'failed_infrastructure': failed_infra
        }
        
    elif disaster_type == "contamination":
        air_quality = random.uniform(150, 450)     # AQI 150-450
        water_contam = random.uniform(0.3, 0.95)   # 0.3-0.95
        chemical = random.uniform(0.2, 0.8)        # 0.2-0.8
        
        ward_data = {
            'air_quality_index': air_quality,
            'water_contamination': water_contam,
            'chemical_level': chemical,
            'failed_infrastructure': failed_infra
        }
        
        sensor_data = {
            'air_quality_index': round(air_quality, 0),
            'water_contamination': round(water_contam, 2),
            'chemical_level': round(chemical, 2),
            'failed_infrastructure': failed_infra
        }
        
    else:  # flood
        ward_data = {
            'rainfall_mm': ward_rain.get('rainfall_mm', 0) if ward_rain else 0,
            'water_level_m': ward_water.get('water_level_m', 0) if ward_water else 0,
            'traffic_density': ward_traffic.get('density', 0) if ward_traffic else 0,
            'failed_infrastructure': failed_infra
        }
        
        sensor_data = ward_data.copy()
    
    # Run expert system
    expert_result = analyze_ward_expert_system(ward_data, disaster_type=disaster_type)
    
    # Run logic programming for ward dependencies
    logic_program = LogicProgram()
    
    # Assert facts based on disaster type
    if disaster_type == "flood":
        if ward_data.get('rainfall_mm', 0) > 50:
            logic_program.assert_fact("HeavyRainfall", ward_id)
        if ward_data.get('water_level_m', 0) > 2.0:
            logic_program.assert_fact("HighWaterLevel", ward_id)
        if ward_data.get('traffic_density', 0) > 0.7:
            logic_program.assert_fact("TrafficCongestion", ward_id)
        
        # Define rules
        logic_program.assert_rule(
            ("FloodRisk", (ward_id,)),
            [("HeavyRainfall", (ward_id,)), ("HighWaterLevel", (ward_id,))]
        )
        
        # Query
        flood_risk = logic_program.query("FloodRisk", ward_id)
        risk_detected = len(flood_risk) > 0
        
    elif disaster_type == "fire":
        if ward_data.get('temperature', 0) > 40:
            logic_program.assert_fact("HighTemperature", ward_id)
        if ward_data.get('wind_speed', 0) > 35:
            logic_program.assert_fact("HighWind", ward_id)
        
        logic_program.assert_rule(
            ("FireRisk", (ward_id,)),
            [("HighTemperature", (ward_id,)), ("HighWind", (ward_id,))]
        )
        
        fire_risk = logic_program.query("FireRisk", ward_id)
        risk_detected = len(fire_risk) > 0
        
    else:  # contamination
        if ward_data.get('air_quality_index', 0) > 200:
            logic_program.assert_fact("PoorAirQuality", ward_id)
        if ward_data.get('water_contamination', 0) > 0.5:
            logic_program.assert_fact("WaterContaminated", ward_id)
        
        logic_program.assert_rule(
            ("ContaminationRisk", (ward_id,)),
            [("PoorAirQuality", (ward_id,)), ("WaterContaminated", (ward_id,))]
        )
        
        contam_risk = logic_program.query("ContaminationRisk", ward_id)
        risk_detected = len(contam_risk) > 0
    
    return {
        "success": True,
        "ward_id": ward_id,
        "timestamp": pd.Timestamp.now().isoformat(),
        "disaster_type": disaster_type,
        "sensor_data": sensor_data,
        "expert_system": {
            "risk_level": expert_result["risk_level"],
            "rules_fired": expert_result["rules_fired"],
            "decisions": expert_result["decisions"]
        },
        "logic_programming": {
            "risk_detected": risk_detected,
            "facts": {k: list(v) for k, v in logic_program.facts.items()}
        }
    }


# ============================================================================
# ADVANCED INFERENCE ENDPOINTS
# ============================================================================

from backend.core.knowledge_engine.advanced_inference import AdvancedInferenceEngine

# Global advanced inference engine
advanced_engine = AdvancedInferenceEngine()


@router.post("/advanced/abductive")
async def abductive_reasoning_endpoint(
    observations: List[str],
    hypotheses: List[Dict]
):
    """
    Abductive Reasoning: Find best explanation for observations
    
    Example:
    POST /api/knowledge/advanced/abductive
    {
        "observations": ["high_water_level", "heavy_rainfall", "flooded_streets"],
        "hypotheses": [
            {
                "name": "monsoon_flood",
                "explains": ["high_water_level", "heavy_rainfall", "flooded_streets"],
                "assumptions": ["monsoon_season"],
                "prior": 0.6,
                "description": "Seasonal monsoon causing widespread flooding"
            },
            {
                "name": "dam_breach",
                "explains": ["high_water_level", "flooded_streets"],
                "assumptions": ["dam_failure", "upstream_release"],
                "prior": 0.2,
                "description": "Dam breach releasing large water volume"
            }
        ]
    }
    """
    try:
        result = advanced_engine.abductive_reasoning(observations, hypotheses)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/analogical")
async def analogical_reasoning_endpoint(
    current_situation: Dict,
    past_cases: List[Dict]
):
    """
    Analogical Reasoning: Find similar past cases
    
    Example:
    POST /api/knowledge/advanced/analogical
    {
        "current_situation": {
            "features": {"rainfall": 80, "water_level": 2.5, "traffic_density": 0.8}
        },
        "past_cases": [
            {
                "id": "case_2019_monsoon",
                "features": {"rainfall": 75, "water_level": 2.3, "traffic_density": 0.7},
                "solution": "evacuate_low_lying_areas",
                "outcome": "successful"
            }
        ]
    }
    """
    try:
        result = advanced_engine.analogical_reasoning(current_situation, past_cases)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/fuzzy")
async def fuzzy_reasoning_endpoint(crisp_values: Dict[str, float]):
    """
    Fuzzy Reasoning: Handle imprecise measurements
    
    Example:
    POST /api/knowledge/advanced/fuzzy
    {
        "rainfall": 65,
        "water_level": 2.3,
        "traffic_density": 0.75,
        "temperature": 38
    }
    """
    try:
        result = advanced_engine.fuzzy_reasoning(crisp_values)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/probabilistic")
async def probabilistic_reasoning_endpoint(
    evidence: Dict[str, bool],
    network: Optional[Dict] = None
):
    """
    Probabilistic Reasoning: Bayesian inference
    
    Example:
    POST /api/knowledge/advanced/probabilistic
    {
        "evidence": {
            "heavy_rain": true,
            "high_temperature": false,
            "chemical_smell": false
        },
        "network": {
            "prior_flood": 0.3,
            "prior_fire": 0.1,
            "prior_contamination": 0.05
        }
    }
    """
    try:
        if network is None:
            network = {}
        result = advanced_engine.probabilistic_reasoning(evidence, network)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/temporal")
async def temporal_reasoning_endpoint(events: List[Dict]):
    """
    Temporal Reasoning: Analyze event sequences
    
    Example:
    POST /api/knowledge/advanced/temporal
    {
        "events": [
            {"event": "rainfall_started", "time": "10:00", "duration": 120},
            {"event": "water_rising", "time": "11:30", "duration": 60},
            {"event": "traffic_jam", "time": "11:45", "duration": 90}
        ]
    }
    """
    try:
        result = advanced_engine.temporal_reasoning(events)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/meta")
async def meta_reasoning_endpoint(problem_characteristics: Dict):
    """
    Meta-Reasoning: Choose best reasoning strategy
    
    Example:
    POST /api/knowledge/advanced/meta
    {
        "has_past_cases": true,
        "has_uncertainty": true,
        "has_temporal_data": false,
        "needs_explanation": true,
        "has_vague_concepts": true,
        "has_probabilities": false
    }
    """
    try:
        result = advanced_engine.meta_reasoning(problem_characteristics)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/hybrid")
async def hybrid_reasoning_endpoint(
    data: Dict,
    strategies: Optional[List[str]] = None
):
    """
    Hybrid Reasoning: Combine multiple strategies
    
    Example:
    POST /api/knowledge/advanced/hybrid
    {
        "data": {
            "rainfall": 75,
            "water_level": 2.8,
            "traffic_density": 0.85,
            "temperature": 32,
            "events": [
                {"event": "rainfall_started", "time": "10:00"},
                {"event": "flooding_reported", "time": "12:00"}
            ]
        },
        "strategies": ["fuzzy", "probabilistic", "temporal"]
    }
    """
    try:
        result = advanced_engine.hybrid_reasoning(data, strategies)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/advanced/history")
async def get_reasoning_history():
    """Get history of reasoning strategies used"""
    try:
        history = advanced_engine.get_reasoning_history()
        stats = advanced_engine.get_strategy_statistics()
        return {
            "history": history,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/clear-history")
async def clear_reasoning_history():
    """Clear reasoning history"""
    try:
        advanced_engine.clear_history()
        return {"message": "Reasoning history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advanced/grid-simulation-analysis")
async def grid_simulation_analysis(simulation_data: Dict):
    """
    Analyze grid simulation results using multiple reasoning strategies
    Returns different reasoning each time based on simulation state
    
    Example:
    POST /api/knowledge/advanced/grid-simulation-analysis
    {
        "ward": "Kurla",
        "rainfall_mm": 85,
        "water_level_m": 2.7,
        "traffic_density": 0.82,
        "temperature": 31,
        "failed_infrastructure": 3,
        "evacuation_progress": 0.45,
        "simulation_step": 15,
        "events": [
            {"event": "heavy_rain_detected", "time": "10:00"},
            {"event": "water_level_rising", "time": "11:00"},
            {"event": "evacuation_started", "time": "11:30"}
        ]
    }
    """
    try:
        ward = simulation_data.get("ward", "Unknown")
        step = simulation_data.get("simulation_step", 0)
        
        # Determine which reasoning strategy to use based on simulation step
        # This ensures different reasoning each time
        strategy_cycle = [
            "fuzzy",
            "probabilistic",
            "temporal",
            "abductive",
            "analogical",
            "hybrid"
        ]
        
        primary_strategy = strategy_cycle[step % len(strategy_cycle)]
        
        results = {
            "ward": ward,
            "simulation_step": step,
            "primary_strategy": primary_strategy,
            "timestamp": pd.Timestamp.now().isoformat(),
            "reasoning_results": {}
        }
        
        # Apply primary strategy
        if primary_strategy == "fuzzy":
            fuzzy_result = advanced_engine.fuzzy_reasoning({
                "rainfall": simulation_data.get("rainfall_mm", 0),
                "water_level": simulation_data.get("water_level_m", 0),
                "traffic_density": simulation_data.get("traffic_density", 0),
                "temperature": simulation_data.get("temperature", 25)
            })
            results["reasoning_results"]["fuzzy"] = fuzzy_result
            results["primary_conclusion"] = f"Fuzzy analysis: Risk level {fuzzy_result['risk_level']} with score {fuzzy_result['crisp_risk_score']:.2f}"
        
        elif primary_strategy == "probabilistic":
            prob_result = advanced_engine.probabilistic_reasoning({
                "heavy_rain": simulation_data.get("rainfall_mm", 0) > 50,
                "high_temperature": simulation_data.get("temperature", 25) > 35,
                "chemical_smell": False
            }, {})
            results["reasoning_results"]["probabilistic"] = prob_result
            results["primary_conclusion"] = f"Bayesian inference: Most likely {prob_result['most_likely_disaster']} with {prob_result['confidence']:.2%} confidence"
        
        elif primary_strategy == "temporal":
            if "events" in simulation_data:
                temporal_result = advanced_engine.temporal_reasoning(simulation_data["events"])
                results["reasoning_results"]["temporal"] = temporal_result
                patterns = len(temporal_result.get("temporal_patterns", []))
                predictions = len(temporal_result.get("predictions", []))
                results["primary_conclusion"] = f"Temporal analysis: Found {patterns} patterns, {predictions} predictions"
            else:
                results["primary_conclusion"] = "Temporal analysis: No events data available"
        
        elif primary_strategy == "abductive":
            # Generate observations from simulation data
            observations = []
            if simulation_data.get("rainfall_mm", 0) > 50:
                observations.append("heavy_rainfall")
            if simulation_data.get("water_level_m", 0) > 2.0:
                observations.append("high_water_level")
            if simulation_data.get("traffic_density", 0) > 0.7:
                observations.append("severe_traffic")
            if simulation_data.get("failed_infrastructure", 0) > 2:
                observations.append("infrastructure_failures")
            
            hypotheses = [
                {
                    "name": "monsoon_flood",
                    "explains": ["heavy_rainfall", "high_water_level"],
                    "assumptions": ["monsoon_season"],
                    "prior": 0.6,
                    "description": "Seasonal monsoon flooding"
                },
                {
                    "name": "infrastructure_collapse",
                    "explains": ["infrastructure_failures", "high_water_level"],
                    "assumptions": ["aging_infrastructure"],
                    "prior": 0.3,
                    "description": "Infrastructure failure causing flooding"
                },
                {
                    "name": "drainage_blockage",
                    "explains": ["high_water_level", "severe_traffic"],
                    "assumptions": ["blocked_drains"],
                    "prior": 0.4,
                    "description": "Blocked drainage system"
                }
            ]
            
            abductive_result = advanced_engine.abductive_reasoning(observations, hypotheses)
            results["reasoning_results"]["abductive"] = abductive_result
            best = abductive_result.get("best_explanation", {})
            results["primary_conclusion"] = f"Abductive reasoning: Best explanation is {best.get('hypothesis', 'unknown')} with {best.get('score', 0):.2f} score"
        
        elif primary_strategy == "analogical":
            # Create past cases for comparison
            past_cases = [
                {
                    "id": "2019_monsoon_kurla",
                    "features": {"rainfall": 80, "water_level": 2.5, "traffic_density": 0.75},
                    "solution": "immediate_evacuation",
                    "outcome": "successful"
                },
                {
                    "id": "2020_flood_bandra",
                    "features": {"rainfall": 60, "water_level": 2.0, "traffic_density": 0.6},
                    "solution": "staged_evacuation",
                    "outcome": "successful"
                },
                {
                    "id": "2021_heavy_rain_andheri",
                    "features": {"rainfall": 90, "water_level": 3.0, "traffic_density": 0.85},
                    "solution": "emergency_evacuation",
                    "outcome": "partially_successful"
                }
            ]
            
            current = {
                "features": {
                    "rainfall": simulation_data.get("rainfall_mm", 0),
                    "water_level": simulation_data.get("water_level_m", 0),
                    "traffic_density": simulation_data.get("traffic_density", 0)
                }
            }
            
            analogical_result = advanced_engine.analogical_reasoning(current, past_cases)
            results["reasoning_results"]["analogical"] = analogical_result
            results["primary_conclusion"] = f"Analogical reasoning: Recommended solution is {analogical_result.get('recommended_solution', 'unknown')}"
        
        elif primary_strategy == "hybrid":
            hybrid_result = advanced_engine.hybrid_reasoning({
                "rainfall": simulation_data.get("rainfall_mm", 0),
                "water_level": simulation_data.get("water_level_m", 0),
                "traffic_density": simulation_data.get("traffic_density", 0),
                "temperature": simulation_data.get("temperature", 25),
                "events": simulation_data.get("events", [])
            })
            results["reasoning_results"]["hybrid"] = hybrid_result
            results["primary_conclusion"] = f"Hybrid reasoning: Combined risk score {hybrid_result['combined_risk_score']:.2f}, level {hybrid_result['risk_level']}"
        
        # Add secondary analysis (always include expert system)
        expert_result = analyze_with_expert_system({
            'rainfall': simulation_data.get('rainfall_mm', 0),
            'water_level': simulation_data.get('water_level_m', 0),
            'traffic_density': simulation_data.get('traffic_density', 0),
            'failed_infrastructure': simulation_data.get('failed_infrastructure', 0)
        }, disaster_type="flood")
        
        results["reasoning_results"]["expert_system"] = expert_result
        results["expert_conclusion"] = f"Expert system: {expert_result['risk_level']} risk, {expert_result['total_rules']} rules fired"
        
        # Generate recommendations based on all reasoning
        recommendations = []
        
        # Extract risk levels from all strategies
        risk_indicators = []
        
        if "fuzzy" in results["reasoning_results"]:
            risk_indicators.append(results["reasoning_results"]["fuzzy"]["crisp_risk_score"])
        
        if "hybrid" in results["reasoning_results"]:
            risk_indicators.append(results["reasoning_results"]["hybrid"]["combined_risk_score"])
        
        if "expert_system" in results["reasoning_results"]:
            risk_level = results["reasoning_results"]["expert_system"]["risk_level"]
            risk_map = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.75, "CRITICAL": 0.95, "EXTREME": 0.98}
            risk_indicators.append(risk_map.get(risk_level, 0.5))
        
        avg_risk = sum(risk_indicators) / len(risk_indicators) if risk_indicators else 0.5
        
        if avg_risk > 0.8:
            recommendations.append("🚨 CRITICAL: Immediate evacuation required")
            recommendations.append("Deploy all available rescue teams")
            recommendations.append("Activate emergency protocols")
        elif avg_risk > 0.6:
            recommendations.append("⚠️ HIGH RISK: Prepare for evacuation")
            recommendations.append("Alert emergency services")
            recommendations.append("Monitor situation closely")
        elif avg_risk > 0.4:
            recommendations.append("⚠️ MODERATE RISK: Stay alert")
            recommendations.append("Avoid unnecessary travel")
            recommendations.append("Keep emergency supplies ready")
        else:
            recommendations.append("✅ LOW RISK: Normal operations")
            recommendations.append("Continue monitoring")
        
        results["recommendations"] = recommendations
        results["average_risk_score"] = avg_risk
        results["next_strategy"] = strategy_cycle[(step + 1) % len(strategy_cycle)]
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
