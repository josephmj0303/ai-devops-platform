from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import get_logger
from app.core.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    logger.info(
        "Starting %s v%s (%s)",
        settings.app.APP_NAME,
        settings.app.APP_VERSION,
        settings.app.ENVIRONMENT,
    )

    #
    # Future initialization
    #
    # PostgreSQL
    # Redis
    # AI Client
    #

    yield

    logger.info(
        "Stopping %s",
        settings.app.APP_NAME,
    )

    #
    # Future cleanup
    #
