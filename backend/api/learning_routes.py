"""
Learning Layer API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

router = APIRouter(prefix="/api/learning", tags=["learning"])

# Global instances (will be injected via dependency container)
_training_pipeline = None
_simulation_trainer = None
_policy_evaluator = None
_checkpoint_manager = None


class TrainEpisodeRequest(BaseModel):
    disaster_type: str
    severity: float
    city_config: Optional[Dict[str, Any]] = None
    max_steps: int = 20


class TrainBatchRequest(BaseModel):
    scenarios: List[Dict[str, Any]]
    episodes_per_scenario: int = 5


class EvaluatePolicyRequest(BaseModel):
    test_scenarios: List[Dict[str, Any]]
    num_episodes_per_scenario: int = 5


@router.post("/train/episode")
async def train_episode(request: TrainEpisodeRequest):
    """Train for a single episode."""
    if _training_pipeline is None or _simulation_trainer is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        scenario = {
            'disaster_type': request.disaster_type,
            'severity': request.severity,
            'city_config': request.city_config or {}
        }
        
        result = _simulation_trainer.train_on_scenario(
            _training_pipeline,
            scenario,
            num_episodes=1
        )
        
        return {
            'status': 'success',
            'result': result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train/batch")
async def train_batch(request: TrainBatchRequest):
    """Train on multiple scenarios."""
    if _training_pipeline is None or _simulation_trainer is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        result = _simulation_trainer.train_on_multiple_scenarios(
            _training_pipeline,
            request.scenarios,
            request.episodes_per_scenario
        )
        
        return {
            'status': 'success',
            'result': result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training/summary")
async def get_training_summary():
    """Get training summary."""
    if _training_pipeline is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        summary = _training_pipeline.get_training_summary()
        return {
            'status': 'success',
            'summary': summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate")
async def evaluate_policy(request: EvaluatePolicyRequest):
    """Evaluate current policy."""
    if _policy_evaluator is None or _training_pipeline is None or _simulation_trainer is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        # Get agent from training pipeline
        agent = _training_pipeline.agent
        
        evaluation = _policy_evaluator.evaluate_policy(
            agent,
            request.test_scenarios,
            _simulation_trainer,
            request.num_episodes_per_scenario
        )
        
        return {
            'status': 'success',
            'evaluation': evaluation
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluation/report")
async def get_evaluation_report():
    """Get comprehensive evaluation report."""
    if _policy_evaluator is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        report = _policy_evaluator.generate_evaluation_report()
        return {
            'status': 'success',
            'report': report
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/save")
async def save_checkpoint(metadata: Optional[Dict[str, Any]] = None):
    """Save training checkpoint."""
    if _checkpoint_manager is None or _training_pipeline is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        checkpoint_id = _checkpoint_manager.save_checkpoint(
            _training_pipeline.agent,
            _training_pipeline.experience_store,
            metadata
        )
        
        return {
            'status': 'success',
            'checkpoint_id': checkpoint_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkpoint/load/{checkpoint_id}")
async def load_checkpoint(checkpoint_id: str):
    """Load training checkpoint."""
    if _checkpoint_manager is None or _training_pipeline is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        success = _checkpoint_manager.load_checkpoint(
            checkpoint_id,
            _training_pipeline.agent,
            _training_pipeline.experience_store
        )
        
        if success:
            return {
                'status': 'success',
                'checkpoint_id': checkpoint_id
            }
        else:
            raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/checkpoints")
async def list_checkpoints():
    """List all checkpoints."""
    if _checkpoint_manager is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        checkpoints = _checkpoint_manager.list_checkpoints()
        return {
            'status': 'success',
            'checkpoints': checkpoints
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scenarios/generate")
async def generate_scenarios(num_scenarios: int = 10):
    """Generate training scenarios."""
    if _simulation_trainer is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        scenarios = _simulation_trainer.generate_training_scenarios(num_scenarios)
        return {
            'status': 'success',
            'scenarios': scenarios
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics():
    """Get learning system statistics."""
    if _training_pipeline is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    
    try:
        stats = {
            'agent': _training_pipeline.agent.get_statistics(),
            'experience_store': _training_pipeline.experience_store.get_statistics(),
            'training': _training_pipeline.get_training_summary()
        }
        
        if _simulation_trainer:
            stats['simulation'] = _simulation_trainer.get_session_statistics()
        
        return {
            'status': 'success',
            'statistics': stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def initialize_learning_routes(
    training_pipeline,
    simulation_trainer,
    policy_evaluator,
    checkpoint_manager
):
    """Initialize route dependencies."""
    global _training_pipeline, _simulation_trainer, _policy_evaluator, _checkpoint_manager
    _training_pipeline = training_pipeline
    _simulation_trainer = simulation_trainer
    _policy_evaluator = policy_evaluator
    _checkpoint_manager = checkpoint_manager
