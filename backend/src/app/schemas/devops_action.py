from pydantic import BaseModel, Field


class DockerRestartRequest(BaseModel):
    container_name: str = Field(min_length=1, max_length=100)


class DevOpsActionResponse(BaseModel):
    action: str
    target: str
    status: str
    message: str
