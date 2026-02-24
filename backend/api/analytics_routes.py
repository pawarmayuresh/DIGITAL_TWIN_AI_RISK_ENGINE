"""
Analytics API Routes
Provides endpoints for KPIs, resilience metrics, and scenario comparison
"""
from fastapi import APIRouter
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter(tags=["analytics"])

# Import analytics modules
try:
    from backend.core.analytics_engine.kpi_calculator import KPICalculator
    from backend.core.analytics_engine.resilience_index import ResilienceIndexCalculator
    from backend.core.analytics_engine.economic_loss_estimator import EconomicLossEstimator
    from backend.core.analytics_engine.scenario_comparator import ScenarioComparator
except ImportError:
    KPICalculator = None
    ResilienceIndexCalculator = None
    EconomicLossEstimator = None
    ScenarioComparator = None


@router.get("/kpis")
async def get_kpis():
    """Get current KPI metrics"""
    if not KPICalculator:
        return {
            "population_affected": 15000,
            "infrastructure_damage": 0.25,
            "economic_loss": 50000000,
            "recovery_time": 30,
            "casualties": 50
        }
    
    calculator = KPICalculator()
    # Mock state for demo
    state = {
        "population": {"total": 500000, "affected": 15000, "displaced": 5000},
        "infrastructure": {"total_nodes": 100, "damaged_nodes": 25},
        "economy": {"baseline_gdp": 1000000000, "current_gdp": 950000000},
        "casualties": 50
    }
    return calculator.calculate_all_kpis(state)


@router.get("/resilience-index")
async def get_resilience_index():
    """Get resilience index metrics"""
    if not ResilienceIndexCalculator:
        return {
            "overall_resilience": 85.0,
            "robustness": 87.0,
            "redundancy": 82.0,
            "resourcefulness": 88.0,
            "social_cohesion": 78.0
        }
    
    calculator = ResilienceIndexCalculator()
    # Mock state for demo
    state = {
        "infrastructure": {"health": 0.85, "redundancy": 0.82},
        "resources": {"availability": 0.88, "diversity": 0.85},
        "social": {"cohesion": 0.78, "trust": 0.80}
    }
    return calculator.calculate_resilience_index(state)


@router.get("/resilience")
async def get_resilience_score():
    """Get overall resilience score"""
    index = await get_resilience_index()
    return {"resilience_score": index.get("overall_resilience", 85.0)}


@router.get("/economic-losses")
async def get_economic_losses():
    """Get economic loss breakdown"""
    if not EconomicLossEstimator:
        return {
            "total_loss": 50000000,
            "direct_damage": 30000000,
            "indirect_loss": 15000000,
            "recovery_cost": 5000000
        }
    
    estimator = EconomicLossEstimator()
    # Mock disaster impact
    impact = {
        "infrastructure_damage": 0.25,
        "population_affected": 15000,
        "duration_days": 30
    }
    return estimator.estimate_losses(impact)


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
