from pydantic import BaseModel, Field


class DockerRestartRequest(BaseModel):
    container_name: str = Field(min_length=1, max_length=100)


class DevOpsActionResponse(BaseModel):
    action: str
    target: str
    status: str
    message: str


class AvailableAction(BaseModel):
    action: str
    name: str
    description: str
    target_type: str
    enabled: bool


class AvailableActionsResponse(BaseModel):
    component: str
    actions: list[AvailableAction]
