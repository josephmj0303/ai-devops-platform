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

    # Application state
    app.state.db = None
    app.state.redis = None
    app.state.ai_client = None

    # PostgreSQL
    # app.state.db = create_database_pool()

    # Redis
    # app.state.redis = create_redis_client()

    # AI Client
    # app.state.ai_client = OpenAI(...)

    yield

    logger.info(
        "Stopping %s",
        settings.app.APP_NAME,
    )

    #
    # Future cleanup
    #

    # if app.state.db:
    #     await app.state.db.close()

    # if app.state.redis:
    #     await app.state.redis.close()
