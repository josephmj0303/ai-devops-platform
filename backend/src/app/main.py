import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.models.health import HealthResponse, ReadinessResponse

settings = get_settings()
app = FastAPI(
    title=settings.app.APP_NAME,
    version=settings.app.APP_VERSION,
    docs_url=settings.api.DOCS_URL,
    redoc_url=settings.api.REDOC_URL,
    openapi_url=settings.api.OPENAPI_URL,
)
configure_logging(settings)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Enterprise FastAPI backend for the AI DevOps Platform. "
        "AI capabilities are not enabled yet."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.backend_cors_origins] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    logger.info(
        "Starting %s version=%s environment=%s",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )

@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
	"environment": settings.app_env,
        "status": "running",
    }

@app.get("/health/live", response_model=HealthResponse, tags=["health"])
def liveness() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/health/ready", response_model=ReadinessResponse, tags=["health"])
def readiness() -> ReadinessResponse:
    return ReadinessResponse(status="ready", checks={"api": "ok"})
