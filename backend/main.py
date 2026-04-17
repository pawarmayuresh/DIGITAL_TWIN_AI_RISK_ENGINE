from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pathlib import Path

from .config import settings
from .dependency_container import engine
from .api import router as api_router
from .api.evacuation_routes import router as evacuation_router
from .api.explainability_routes import router as explainability_router
from .api.infrastructure_routes import router as infrastructure_router
from .api.knowledge_routes import router as knowledge_router
from .api.realtime_policy_routes import router as realtime_policy_router
from .api.alert_routes import router as alert_router
from .api.csp_routes import router as csp_router


def create_app():
    app = FastAPI(title="AI Strategic Risk Engine", version=settings.app_version)

    # Configure CORS - allow frontend to access backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
        expose_headers=["*"],  # Expose all headers to frontend
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: {}", exc)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    app.include_router(api_router, prefix="/api")
    app.include_router(evacuation_router)
    app.include_router(explainability_router)
    app.include_router(infrastructure_router)
    app.include_router(knowledge_router)
    app.include_router(realtime_policy_router)
    app.include_router(alert_router)
    app.include_router(csp_router)

    # Serve static files
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

    # Root endpoint - serve dashboard
    @app.get("/")
    async def root():
        dashboard_path = Path(__file__).parent / "static" / "dashboard.html"
        if dashboard_path.exists():
            return FileResponse(str(dashboard_path), media_type="text/html")
        return {"message": "Welcome to AI Strategic Risk Engine. Visit /api/health/live for status"}

    @app.on_event("startup")
    def on_startup():
        try:
            conn = engine.connect()
            conn.close()
            logger.info("Database connection OK")
        except Exception as e:
            logger.error("Database connection failed: {}", e)

    return app


app = create_app()
