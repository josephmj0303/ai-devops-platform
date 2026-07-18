from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.lifespan import lifespan
from app.core.logging import configure_logging, get_logger
from app.core.settings import get_settings
from app.exceptions import register_exception_handlers
from app.middleware import register_middleware

settings = get_settings()

configure_logging()
logger = get_logger(__name__)

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
