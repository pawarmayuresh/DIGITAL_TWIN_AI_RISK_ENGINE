"""
Analytics API Routes
Provides endpoints for KPIs, resilience metrics, and scenario comparison
"""
from fastapi import APIRouter
from typing import Dict, List, Optional
from pydantic import BaseModel
import random
import time
from loguru import logger

router = APIRouter(tags=["analytics"])

# Import analytics modules
try:
    from backend.core.analytics_engine.kpi_calculator import KPICalculator
    from backend.core.analytics_engine.resilience_index import ResilienceIndex
    from backend.core.analytics_engine.economic_loss_estimator import EconomicLossEstimator
    from backend.core.analytics_engine.scenario_comparator import ScenarioComparator
except ImportError:
    KPICalculator = None
    ResilienceIndex = None
    EconomicLossEstimator = None
    ScenarioComparator = None

# Global state for simulation
_simulation_state = {
    "timestep": 0,
    "last_update": time.time(),
    "base_resilience": 75.0,
    "trend": 1  # 1 for improving, -1 for declining
}


@router.get("/kpis")
async def get_kpis():
    """Get current KPI metrics with real-time simulation"""
    global _simulation_state
    
    # Generate dynamic KPI values
    timestep = _simulation_state["timestep"]
    base_resilience = _simulation_state["base_resilience"]
    
    # Population metrics (inversely related to resilience)
    population_affected = int(random.uniform(10000, 25000) * (100 - base_resilience) / 50)
    casualties = int(random.uniform(20, 150) * (100 - base_resilience) / 50)
    
    # Infrastructure metrics (directly related to resilience)
    infrastructure_damage = max(0.1, min(0.5, (100 - base_resilience) / 200 + random.uniform(-0.05, 0.05)))
    
    # Economic metrics
    economic_loss = int(random.uniform(30000000, 80000000) * (100 - base_resilience) / 50)
    
    # Recovery metrics
    recovery_time = int(random.uniform(15, 45) * (100 - base_resilience) / 50)
    
    if KPICalculator:
        calculator = KPICalculator()
        state = {
            "casualties": casualties,
            "population_affected": population_affected,
            "initial_population_at_risk": population_affected + int(random.uniform(5000, 10000)),
            "infrastructure_health": base_resilience,
            "economic_loss": economic_loss,
            "response_time": recovery_time,
            "resources_used": random.uniform(3000, 7000),
            "resources_available": 10000,
            "population_evacuated": int(population_affected * random.uniform(0.7, 0.95)),
            "population_at_risk": population_affected,
            "potential_cascading_failures": random.randint(5, 15),
            "actual_cascading_failures": random.randint(0, 5)
        }
        
        kpis = calculator.calculate_kpis(state)
        
        return {
            "population_affected": population_affected,
            "infrastructure_damage": infrastructure_damage,
            "economic_loss": economic_loss,
            "recovery_time": recovery_time,
            "casualties": casualties,
            "timestep": timestep,
            "kpis": {name: {
                "value": kpi.value,
                "unit": kpi.unit,
                "status": kpi.status,
                "trend": kpi.trend
            } for name, kpi in kpis.items()}
        }
    
    return {
        "population_affected": population_affected,
        "infrastructure_damage": infrastructure_damage,
        "economic_loss": economic_loss,
        "recovery_time": recovery_time,
        "casualties": casualties,
        "timestep": timestep
    }


@router.get("/resilience-index")
async def get_resilience_index():
    """Get resilience index metrics with real-time simulation"""
    global _simulation_state
    
    # Update timestep
    current_time = time.time()
    if current_time - _simulation_state["last_update"] > 1:
        _simulation_state["timestep"] += 1
        _simulation_state["last_update"] = current_time
        
        # Randomly change trend occasionally
        if random.random() < 0.1:
            _simulation_state["trend"] *= -1
    
    # Generate dynamic resilience scores with realistic variation
    base = _simulation_state["base_resilience"]
    variation = random.uniform(-3, 3)
    trend_effect = _simulation_state["trend"] * 0.5
    
    # Update base resilience gradually
    _simulation_state["base_resilience"] = max(60, min(95, base + trend_effect + variation * 0.1))
    
    overall = _simulation_state["base_resilience"]
    
    # Generate correlated component scores
    robustness = max(50, min(100, overall + random.uniform(-5, 5)))
    redundancy = max(50, min(100, overall + random.uniform(-8, 8)))
    resourcefulness = max(50, min(100, overall + random.uniform(-6, 6)))
    rapidity = max(50, min(100, overall + random.uniform(-7, 7)))
    
    if ResilienceIndex:
        calculator = ResilienceIndex()
        city_data = {
            "infrastructure_health": robustness,
            "building_code_compliance": 0.85,
            "backup_systems": redundancy / 100.0,
            "resource_stockpiles": resourcefulness / 100.0,
            "resources_available": 5000
        }
        disaster_response = {
            "resources_mobilized": int(5000 * (resourcefulness / 100.0)),
            "response_time": max(20, 60 - (rapidity / 100.0) * 40)
        }
        
        score = calculator.calculate_resilience(city_data, disaster_response)
        
        return {
            "overall_resilience": score.overall_score,
            "robustness": score.robustness,
            "redundancy": score.redundancy,
            "resourcefulness": score.resourcefulness,
            "rapidity": score.rapidity,
            "timestep": _simulation_state["timestep"],
            "trend": "improving" if _simulation_state["trend"] > 0 else "declining"
        }
    
    return {
        "overall_resilience": overall,
        "robustness": robustness,
        "redundancy": redundancy,
        "resourcefulness": resourcefulness,
        "rapidity": rapidity,
        "timestep": _simulation_state["timestep"],
        "trend": "improving" if _simulation_state["trend"] > 0 else "declining"
    }


@router.get("/resilience")
async def get_resilience_score():
    """Get overall resilience score"""
    index = await get_resilience_index()
    return {"resilience_score": index.get("overall_resilience", 85.0)}


@router.get("/economic-losses")
async def get_economic_losses():
    """Get economic loss breakdown with real-time simulation"""
    global _simulation_state
    
    try:
        base_resilience = _simulation_state["base_resilience"]
        
        # Generate dynamic economic losses (inversely related to resilience)
        total_loss = int(random.uniform(40000000, 90000000) * (100 - base_resilience) / 50)
        direct_damage = int(total_loss * random.uniform(0.5, 0.65))
        indirect_loss = int(total_loss * random.uniform(0.25, 0.35))
        recovery_cost = total_loss - direct_damage - indirect_loss
        
        if EconomicLossEstimator:
            try:
                estimator = EconomicLossEstimator()
                impact = {
                    "infrastructure_damage": (100 - base_resilience) / 200,
                    "population_affected": int(random.uniform(10000, 25000) * (100 - base_resilience) / 50),
                    "duration_days": int(random.uniform(15, 45) * (100 - base_resilience) / 50)
                }
                result = estimator.estimate_losses(impact)
                
                return {
                    "total_loss": result.total_loss,
                    "direct_damage": result.infrastructure_damage,
                    "indirect_loss": result.business_interruption,
                    "recovery_cost": result.recovery_cost,
                    "timestep": _simulation_state["timestep"],
                    "breakdown": {
                        "infrastructure": result.infrastructure_damage,
                        "business_interruption": result.business_interruption,
                        "emergency_response": result.emergency_response,
                        "recovery": result.recovery_cost
                    }
                }
            except Exception as e:
                logger.error(f"EconomicLossEstimator error: {e}")
                # Fall through to default response
        
        return {
            "total_loss": total_loss,
            "direct_damage": direct_damage,
            "indirect_loss": indirect_loss,
            "recovery_cost": recovery_cost,
            "timestep": _simulation_state["timestep"]
        }
    except Exception as e:
        logger.error(f"Economic losses endpoint error: {e}")
        import traceback
        traceback.print_exc()
        # Return default values
        return {
            "total_loss": 50000000,
            "direct_damage": 30000000,
            "indirect_loss": 15000000,
            "recovery_cost": 5000000,
            "timestep": 0
        }


@router.post("/compare-scenarios")
async def compare_scenarios(request: Dict):
    """Compare multiple scenarios"""
    scenario_ids = request.get("scenario_ids", [])
    
    if not ScenarioComparator or not scenario_ids:
        return {
            "scenarios": scenario_ids,
            "comparison": {
                "best_scenario": scenario_ids[0] if scenario_ids else "baseline",
                "metrics": {}
            }
        }
    
    comparator = ScenarioComparator()
    # Mock scenario data
    scenarios = {
        sid: {
            "resilience": 80 + (i * 5),
            "economic_loss": 50000000 - (i * 10000000),
            "recovery_time": 30 - (i * 5)
        }
        for i, sid in enumerate(scenario_ids)
    }
    
    return comparator.compare_scenarios(scenarios)


@router.post("/reset-simulation")
async def reset_simulation():
    """Reset the simulation state"""
    global _simulation_state
    
    _simulation_state = {
        "timestep": 0,
        "last_update": time.time(),
        "base_resilience": random.uniform(70, 85),
        "trend": random.choice([1, -1])
    }
    
    return {
        "success": True,
        "message": "Simulation reset",
        "initial_resilience": _simulation_state["base_resilience"]
    }


@router.get("/simulation-status")
async def get_simulation_status():
    """Get current simulation status"""
    global _simulation_state
    
    return {
        "timestep": _simulation_state["timestep"],
        "base_resilience": _simulation_state["base_resilience"],
        "trend": "improving" if _simulation_state["trend"] > 0 else "declining",
        "uptime_seconds": time.time() - _simulation_state["last_update"]
    }
