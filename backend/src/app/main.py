from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.logging import configure_logging, get_logger
from app.core.settings import get_settings

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
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=f"{settings.api.API_PREFIX}/{settings.api.API_VERSION}",
)


@app.on_event("startup")
async def startup_event() -> None:
    logger.info(
        "Starting %s v%s (%s)",
        settings.app.APP_NAME,
        settings.app.APP_VERSION,
        settings.app.ENVIRONMENT,
    )


@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.app.APP_NAME,
        "version": settings.app.APP_VERSION,
        "environment": settings.app.ENVIRONMENT,
        "status": "running",
    }
