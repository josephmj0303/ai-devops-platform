import asyncio

import httpx
from fastapi import APIRouter
from sqlalchemy import text

from app.core.settings import get_settings
from app.db.session import engine
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["Health"])


async def check_database() -> str:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return "healthy"
    except Exception:
        return "unhealthy"


async def check_redis() -> str:
    try:
        reader, writer = await asyncio.open_connection("redis", 6379)

        writer.write(b"*1\r\n$4\r\nPING\r\n")
        await writer.drain()

        response = await reader.read(32)

        writer.close()
        await writer.wait_closed()

        if response.startswith(b"+PONG"):
            return "healthy"

        return "unhealthy"
    except Exception:
        return "unhealthy"


async def check_ollama() -> str:
    settings = get_settings()

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.ai.OLLAMA_BASE_URL}/api/tags"
            )

        if response.status_code == 200:
            return "healthy"

        return "unhealthy"
    except Exception:
        return "unhealthy"


@router.get("/health", response_model=HealthResponse)
def api_health() -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        version=settings.app.APP_VERSION,
        environment=settings.app.ENVIRONMENT,
    )


@router.get("/health/dependencies", response_model=ReadinessResponse)
async def dependency_health() -> ReadinessResponse:
    database, redis, ollama = await asyncio.gather(
        check_database(),
        check_redis(),
        check_ollama(),
    )

    checks = {
        "database": database,
        "redis": redis,
        "ollama": ollama,
    }

    status = "ready" if all(value == "healthy" for value in checks.values()) else "not_ready"

    return ReadinessResponse(
        status=status,
        checks=checks,
    )
