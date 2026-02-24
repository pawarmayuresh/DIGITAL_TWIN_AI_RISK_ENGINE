from fastapi import APIRouter
from .health_routes import router as health_router
from .demo_routes import router as demo_router
from .twin_routes import router as twin_router
from .strategic_ai_routes import router as strategic_ai_router
from .multi_agent_routes import router as multi_agent_router
from .learning_routes import router as learning_router
from .explainability_routes import router as explainability_router
from .analytics_routes import router as analytics_router
from .spatial_routes import router as spatial_router
from .mumbai_routes import router as mumbai_router

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(demo_router, prefix="/demo", tags=["demo"])
router.include_router(twin_router, prefix="/twin", tags=["digital-twin"])
router.include_router(strategic_ai_router, prefix="/strategic-ai", tags=["strategic-ai"])
router.include_router(multi_agent_router, prefix="/agents", tags=["multi-agent"])
router.include_router(learning_router, prefix="/learning", tags=["learning"])
router.include_router(explainability_router, prefix="/explainability", tags=["explainability"])
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
router.include_router(spatial_router, prefix="/spatial", tags=["spatial"])
router.include_router(mumbai_router, prefix="/mumbai", tags=["mumbai"])
