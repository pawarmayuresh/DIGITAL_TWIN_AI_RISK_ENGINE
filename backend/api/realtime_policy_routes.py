"""
API Routes for Real-time Policy Engine
Handles real-time situation updates and adaptive policy recommendations
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

from backend.core.policy_engine.realtime_policy_engine import (
    RealTimePolicyEngine,
    RealTimeSituation,
    UncertaintyLevel,
    HumanBehaviorModel
)

router = APIRouter(prefix="/api/policy/realtime", tags=["Real-time Policy"])

# Global engine instance
policy_engine = RealTimePolicyEngine()


# Pydantic models for request/response
class SituationUpdate(BaseModel):
    """Real-time situation update"""
    rain_intensity: float
    water_level: float
    wind_speed: float = 0.0
    visibility: float = 1000.0
    power_availability: float
    communication_status: float
    road_accessibility: float
    population_at_risk: int
    population_evacuated: int = 0
    casualties: int = 0
    injured: int = 0
    uncertainty_level: str  # "LOW", "MEDIUM", "HIGH", "EXTREME"
    information_accuracy: float = 0.8
    rumor_spread_rate: float = 0.3
    emergency_vehicles: int = 20
    medical_personnel: int = 50
    shelter_capacity: int = 5000
    food_supplies: float = 5.0


class PolicySimulationRequest(BaseModel):
    """Request to simulate policy outcome"""
    policy_id: str
    time_horizon: int = 24


class PolicyComparisonRequest(BaseModel):
    """Request to compare multiple policies"""
    policy_ids: List[str]


@router.post("/situation/update")
async def update_situation(situation_data: SituationUpdate):
    """
    Update current real-time situation
    
    This endpoint receives real-time data from sensors and updates
    the policy engine's understanding of the current crisis.
    """
    try:
        # Convert to UncertaintyLevel enum
        uncertainty_map = {
            "LOW": UncertaintyLevel.LOW,
            "MEDIUM": UncertaintyLevel.MEDIUM,
            "HIGH": UncertaintyLevel.HIGH,
            "EXTREME": UncertaintyLevel.EXTREME
        }
        uncertainty = uncertainty_map.get(
            situation_data.uncertainty_level.upper(),
            UncertaintyLevel.MEDIUM
        )
        
        # Create situation object
        situation = RealTimeSituation(
            timestamp=datetime.now(),
            rain_intensity=situation_data.rain_intensity,
            water_level=situation_data.water_level,
            wind_speed=situation_data.wind_speed,
            visibility=situation_data.visibility,
            power_availability=situation_data.power_availability,
            communication_status=situation_data.communication_status,
            road_accessibility=situation_data.road_accessibility,
            population_at_risk=situation_data.population_at_risk,
            population_evacuated=situation_data.population_evacuated,
            casualties=situation_data.casualties,
            injured=situation_data.injured,
            uncertainty_level=uncertainty,
            information_accuracy=situation_data.information_accuracy,
            rumor_spread_rate=situation_data.rumor_spread_rate,
            emergency_vehicles=situation_data.emergency_vehicles,
            medical_personnel=situation_data.medical_personnel,
            shelter_capacity=situation_data.shelter_capacity,
            food_supplies=situation_data.food_supplies
        )
        
        # Update engine
        policy_engine.update_situation(situation)
        
        severity = situation.get_crisis_severity()
        
        return {
            "success": True,
            "timestamp": situation.timestamp.isoformat(),
            "situation_severity": severity,
            "severity_level": (
                "CRITICAL" if severity > 0.7 else
                "HIGH" if severity > 0.5 else
                "MEDIUM" if severity > 0.3 else
                "LOW"
            ),
            "human_behavior": {
                "panic_level": policy_engine.behavior_model.panic_level,
                "trust_level": policy_engine.behavior_model.trust_in_authority,
                "compliance_rate": policy_engine.behavior_model.compliance_rate,
                "evacuation_willingness": policy_engine.behavior_model.evacuation_willingness
            },
            "message": "Situation updated successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/situation/current")
async def get_current_situation():
    """Get current situation and human behavior analysis"""
    
    if not policy_engine.current_situation:
        raise HTTPException(status_code=404, detail="No situation data available")
    
    situation = policy_engine.current_situation
    behavior = policy_engine.behavior_model
    
    return {
        "timestamp": situation.timestamp.isoformat(),
        "environmental_conditions": {
            "rain_intensity": situation.rain_intensity,
            "water_level": situation.water_level,
            "wind_speed": situation.wind_speed,
            "visibility": situation.visibility
        },
        "infrastructure_status": {
            "power_availability": situation.power_availability,
            "communication_status": situation.communication_status,
            "road_accessibility": situation.road_accessibility
        },
        "population_metrics": {
            "at_risk": situation.population_at_risk,
            "evacuated": situation.population_evacuated,
            "casualties": situation.casualties,
            "injured": situation.injured,
            "evacuation_progress": (
                situation.population_evacuated / max(1, situation.population_at_risk)
            )
        },
        "uncertainty": {
            "level": situation.uncertainty_level.value,
            "information_accuracy": situation.information_accuracy,
            "rumor_spread_rate": situation.rumor_spread_rate
        },
        "resources": {
            "emergency_vehicles": situation.emergency_vehicles,
            "medical_personnel": situation.medical_personnel,
            "shelter_capacity": situation.shelter_capacity,
            "food_supplies_days": situation.food_supplies
        },
        "crisis_severity": situation.get_crisis_severity(),
        "human_behavior": {
            "panic_level": behavior.panic_level,
            "trust_in_authority": behavior.trust_in_authority,
            "risk_perception": behavior.risk_perception,
            "compliance_rate": behavior.compliance_rate,
            "evacuation_willingness": behavior.evacuation_willingness,
            "decision_paralysis": behavior.decision_paralysis,
            "rumor_susceptibility": behavior.rumor_susceptibility,
            "behavior_distribution": behavior.predict_behavior_distribution(),
            "expected_compliance": behavior.estimate_evacuation_compliance()
        }
    }


@router.get("/recommendations")
async def get_policy_recommendations():
    """
    Get adaptive policy recommendations based on current situation
    
    Returns top 3 recommended policies with effectiveness scores,
    barriers, and adaptive strategy.
    """
    
    if not policy_engine.current_situation:
        raise HTTPException(
            status_code=404,
            detail="No situation data available. Please update situation first."
        )
    
    try:
        recommendations = policy_engine.get_adaptive_recommendations()
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/policies")
async def list_all_policies():
    """List all available adaptive policies"""
    
    policies = []
    for policy_id, policy in policy_engine.policies.items():
        policies.append({
            "policy_id": policy.policy_id,
            "name": policy.name,
            "description": policy.description,
            "target_population": policy.target_population,
            "implementation_time_hours": policy.implementation_time,
            "cost": policy.cost,
            "base_effectiveness": policy.base_effectiveness,
            "current_effectiveness": policy.current_effectiveness,
            "required_resources": policy.required_resources,
            "uncertainty_sensitivity": policy.uncertainty_sensitivity,
            "behavior_dependency": policy.behavior_dependency
        })
    
    return {
        "total_policies": len(policies),
        "policies": policies
    }


@router.post("/policy/simulate")
async def simulate_policy(request: PolicySimulationRequest):
    """
    Simulate outcome of a specific policy
    
    Returns expected evacuees, casualties, resource usage,
    and human behavior factors with uncertainty ranges.
    """
    
    if not policy_engine.current_situation:
        raise HTTPException(
            status_code=404,
            detail="No situation data available. Please update situation first."
        )
    
    try:
        outcome = policy_engine.simulate_policy_outcome(
            request.policy_id,
            request.time_horizon
        )
        
        if "error" in outcome:
            raise HTTPException(status_code=404, detail=outcome["error"])
        
        return outcome
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/compare")
async def compare_policies(request: PolicyComparisonRequest):
    """
    Compare multiple policies under current conditions
    
    Returns side-by-side comparison with recommendation
    for best policy based on success probability.
    """
    
    if not policy_engine.current_situation:
        raise HTTPException(
            status_code=404,
            detail="No situation data available. Please update situation first."
        )
    
    try:
        comparison = policy_engine.compare_policies_realtime(request.policy_ids)
        
        if "error" in comparison:
            raise HTTPException(status_code=404, detail=comparison["error"])
        
        return comparison
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/behavior/analysis")
async def get_behavior_analysis():
    """
    Get detailed human behavior analysis
    
    Returns psychological factors, behavioral tendencies,
    and predicted behavior distribution in population.
    """
    
    behavior = policy_engine.behavior_model
    
    return {
        "psychological_factors": {
            "panic_level": behavior.panic_level,
            "trust_in_authority": behavior.trust_in_authority,
            "risk_perception": behavior.risk_perception,
            "social_influence": behavior.social_influence
        },
        "behavioral_tendencies": {
            "compliance_rate": behavior.compliance_rate,
            "evacuation_willingness": behavior.evacuation_willingness,
            "helping_behavior": behavior.helping_behavior
        },
        "uncertainty_responses": {
            "information_seeking": behavior.information_seeking,
            "rumor_susceptibility": behavior.rumor_susceptibility,
            "decision_paralysis": behavior.decision_paralysis
        },
        "demographics": {
            "age_distribution": behavior.age_distribution,
            "education_level": behavior.education_level,
            "previous_disaster_experience": behavior.previous_disaster_experience
        },
        "behavior_distribution": behavior.predict_behavior_distribution(),
        "expected_evacuation_compliance": behavior.estimate_evacuation_compliance(),
        "interpretation": {
            "dominant_behavior": max(
                behavior.predict_behavior_distribution().items(),
                key=lambda x: x[1]
            )[0],
            "compliance_level": (
                "HIGH" if behavior.compliance_rate > 0.7 else
                "MEDIUM" if behavior.compliance_rate > 0.4 else
                "LOW"
            ),
            "panic_status": (
                "CRITICAL" if behavior.panic_level > 0.7 else
                "HIGH" if behavior.panic_level > 0.5 else
                "MODERATE" if behavior.panic_level > 0.3 else
                "LOW"
            )
        }
    }


@router.post("/test/scenario")
async def test_scenario(scenario_name: str = "moderate_flood"):
    """
    Load a test scenario for demonstration
    
    Available scenarios:
    - moderate_flood: Moderate flooding with medium uncertainty
    - severe_crisis: Severe crisis with high panic
    - communication_failure: Infrastructure failure scenario
    - high_uncertainty: Extreme uncertainty scenario
    """
    
    scenarios = {
        "moderate_flood": SituationUpdate(
            rain_intensity=65.0,
            water_level=1.2,
            wind_speed=30.0,
            power_availability=0.7,
            communication_status=0.8,
            road_accessibility=0.6,
            population_at_risk=5000,
            population_evacuated=1000,
            casualties=2,
            injured=10,
            uncertainty_level="MEDIUM",
            information_accuracy=0.75,
            rumor_spread_rate=0.4,
            emergency_vehicles=25,
            medical_personnel=60,
            shelter_capacity=6000,
            food_supplies=4.0
        ),
        "severe_crisis": SituationUpdate(
            rain_intensity=95.0,
            water_level=2.5,
            wind_speed=60.0,
            power_availability=0.3,
            communication_status=0.4,
            road_accessibility=0.2,
            population_at_risk=15000,
            population_evacuated=3000,
            casualties=15,
            injured=50,
            uncertainty_level="HIGH",
            information_accuracy=0.5,
            rumor_spread_rate=0.8,
            emergency_vehicles=15,
            medical_personnel=40,
            shelter_capacity=8000,
            food_supplies=2.0
        ),
        "communication_failure": SituationUpdate(
            rain_intensity=75.0,
            water_level=1.8,
            wind_speed=40.0,
            power_availability=0.2,
            communication_status=0.1,
            road_accessibility=0.4,
            population_at_risk=8000,
            population_evacuated=1500,
            casualties=5,
            injured=25,
            uncertainty_level="EXTREME",
            information_accuracy=0.3,
            rumor_spread_rate=0.9,
            emergency_vehicles=20,
            medical_personnel=45,
            shelter_capacity=7000,
            food_supplies=3.0
        ),
        "high_uncertainty": SituationUpdate(
            rain_intensity=80.0,
            water_level=2.0,
            wind_speed=50.0,
            power_availability=0.5,
            communication_status=0.3,
            road_accessibility=0.3,
            population_at_risk=10000,
            population_evacuated=2000,
            casualties=8,
            injured=30,
            uncertainty_level="EXTREME",
            information_accuracy=0.4,
            rumor_spread_rate=0.85,
            emergency_vehicles=18,
            medical_personnel=50,
            shelter_capacity=7500,
            food_supplies=2.5
        )
    }
    
    if scenario_name not in scenarios:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario '{scenario_name}' not found. Available: {list(scenarios.keys())}"
        )
    
    # Load scenario
    scenario_data = scenarios[scenario_name]
    result = await update_situation(scenario_data)
    
    # Get recommendations
    recommendations = await get_policy_recommendations()
    
    return {
        "scenario_loaded": scenario_name,
        "situation_update": result,
        "recommendations": recommendations
    }
