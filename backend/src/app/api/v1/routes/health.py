from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def api_health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(status="ok", version=settings.app_version, environment=settings.app_env)


@router.get("/health/dependencies", response_model=ReadinessResponse)
def dependency_health() -> ReadinessResponse:
    return ReadinessResponse(
        status="ready",
        checks={"database": "not_configured", "queue": "not_configured"},
    )
