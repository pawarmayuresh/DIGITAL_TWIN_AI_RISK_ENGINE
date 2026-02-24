"""
Strategic AI API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

router = APIRouter()

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from core.strategic_ai import (
    PolicySimulator,
    ClassicalPlanner,
    HeuristicSearch,
    ResourceAllocator,
    AllocationStrategy,
    ScenarioComparator,
    Scenario,
    OptimizationScorer,
    ScoringWeights
)

# Global instances
policy_sim = PolicySimulator()
planner = ClassicalPlanner()
heuristic_search = HeuristicSearch()
resource_allocator = ResourceAllocator()
scenario_comparator = ScenarioComparator()
optimizer = OptimizationScorer()


class PolicySimulationRequest(BaseModel):
    policy_id: str
    current_state: Dict


class PlanningRequest(BaseModel):
    initial_conditions: List[str]
    goals: List[str]
    max_depth: int = 10


class ResourceAllocationRequest(BaseModel):
    demands: Dict[str, Dict]
    strategy: str = "proportional"


class ScenarioComparisonRequest(BaseModel):
    scenario_ids: List[str]
    weights: Optional[Dict[str, float]] = None


@router.get("/policies")
async def get_all_policies():
    """Get all available policies"""
    try:
        return {"policies": policy_sim.get_all_policies()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/simulate")
async def simulate_policy(request: PolicySimulationRequest):
    """Simulate a policy"""
    try:
        result = policy_sim.simulate_policy(
            request.policy_id,
            request.current_state
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/compare")
async def compare_policies(policy_ids: List[str], current_state: Dict):
    """Compare multiple policies"""
    try:
        result = policy_sim.compare_policies(policy_ids, current_state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policies/recommend")
async def recommend_policies(current_state: Dict, budget: float, max_policies: int = 5):
    """Recommend policy bundle"""
    try:
        result = policy_sim.recommend_policy_bundle(current_state, budget, max_policies)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan")
async def create_plan(request: PlanningRequest):
    """Create a disaster response plan"""
    try:
        result = planner.plan(
            request.initial_conditions,
            request.goals,
            request.max_depth
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plan/actions")
async def get_available_actions():
    """Get all available planning actions"""
    try:
        return {"actions": planner.get_all_actions()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan/heuristic")
async def heuristic_plan(request: PlanningRequest):
    """Create plan using heuristic search"""
    try:
        result = heuristic_search.search(
            request.initial_conditions,
            request.goals,
            planner.actions,
            1000
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources")
async def get_resources():
    """Get available resources"""
    try:
        return {"resources": resource_allocator.get_available_resources()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resources/allocate")
async def allocate_resources(request: ResourceAllocationRequest):
    """Allocate resources"""
    try:
        strategy = AllocationStrategy(request.strategy)
        result = resource_allocator.allocate_resources(request.demands, strategy)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resources/gap")
async def calculate_resource_gap(demands: Dict[str, Dict]):
    """Calculate resource gap"""
    try:
        result = resource_allocator.calculate_resource_gap(demands)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scenarios")
async def get_scenarios():
    """Get all scenarios"""
    try:
        return {"scenarios": scenario_comparator.get_all_scenarios()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenarios/compare")
async def compare_scenarios(request: ScenarioComparisonRequest):
    """Compare scenarios"""
    try:
        result = scenario_comparator.compare_scenarios(
            request.scenario_ids,
            request.weights
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/score")
async def score_strategy(strategy: Dict, outcomes: Dict, constraints: Optional[Dict] = None):
    """Score a strategy"""
    try:
        result = optimizer.score_strategy(strategy, outcomes, constraints)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/rank")
async def rank_strategies(strategies: List[Dict], outcomes_list: List[Dict], constraints: Optional[Dict] = None):
    """Rank multiple strategies"""
    try:
        result = optimizer.rank_strategies(strategies, outcomes_list, constraints)
        return {"ranked_strategies": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimize/pareto")
async def get_pareto_optimal():
    """Get Pareto-optimal strategies"""
    try:
        scores = optimizer.get_scores()
        pareto = optimizer.get_pareto_optimal(scores)
        return {"pareto_optimal": pareto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
