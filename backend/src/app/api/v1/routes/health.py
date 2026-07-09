from fastapi import APIRouter

from app.core.settings import get_settings
from app.models.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def api_health() -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        version=settings.app.APP_VERSION,
        environment=settings.app.ENVIRONMENT,
    )


@router.get("/health/dependencies", response_model=ReadinessResponse)
def dependency_health() -> ReadinessResponse:
    return ReadinessResponse(
        status="ready",
        checks={
            "database": "not_configured",
            "redis": "not_configured",
        },
    )
