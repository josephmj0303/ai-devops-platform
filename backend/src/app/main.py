from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.logging import configure_logging, get_logger
from app.core.settings import get_settings
from app.middleware import register_middleware

settings = get_settings()

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle events.
    """

    logger.info(
        "Starting %s v%s (%s)",
        settings.app.APP_NAME,
        settings.app.APP_VERSION,
        settings.app.ENVIRONMENT,
    )

    yield

    logger.info(
        "Stopping %s",
        settings.app.APP_NAME,
    )


app = FastAPI(
    title=settings.app.APP_NAME,
    version=settings.app.APP_VERSION,
    description="Enterprise AI DevOps Platform Backend",
    docs_url=settings.api.DOCS_URL,
    redoc_url=settings.api.REDOC_URL,
    openapi_url=settings.api.OPENAPI_URL,
    lifespan=lifespan,
)

register_middleware(app)

from app.exceptions import register_exception_handlers

register_exception_handlers(app)

app.include_router(
    api_router,
    prefix=f"{settings.api.API_PREFIX}/{settings.api.API_VERSION}",
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.app.APP_NAME,
        "version": settings.app.APP_VERSION,
        "environment": settings.app.ENVIRONMENT,
        "status": "running",
    }
