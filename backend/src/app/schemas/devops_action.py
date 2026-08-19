from datetime import datetime
from pydantic import BaseModel, Field

class DockerRestartRequest(BaseModel):
    analysis_id: int
    container_name: str = Field(min_length=1, max_length=100)

class KubernetesDeploymentRestartRequest(BaseModel):
    analysis_id: int
    namespace: str = Field(min_length=1, max_length=100)
    deployment_name: str = Field(min_length=1, max_length=100)

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

class DockerContainer(BaseModel):
    name: str
    status: str
    image: str

class DevOpsActionHistoryItem(BaseModel):
    id: int
    analysis_id: int
    action: str
    target: str
    status: str
    message: str
    created_at: datetime
