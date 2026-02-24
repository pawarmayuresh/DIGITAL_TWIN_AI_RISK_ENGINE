from fastapi import APIRouter
from ..config import settings

router = APIRouter()


@router.get("/live")
def live():
    return {"status": "alive"}


@router.get("/ready")
def ready():
    return {"status": "ready"}


@router.get("/version")
def version():
    return {"version": settings.app_version, "env": settings.app_env}
