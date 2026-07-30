from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Project name",
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Project description",
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
