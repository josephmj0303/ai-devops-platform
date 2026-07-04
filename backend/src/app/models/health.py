from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str | None = None
    environment: str | None = None


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]
