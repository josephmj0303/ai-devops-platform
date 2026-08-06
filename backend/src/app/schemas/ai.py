from pydantic import BaseModel


class AIChatRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None


class AIChatResponse(BaseModel):
    response: str


class DockerReviewRequest(BaseModel):
    dockerfile: str


class DockerReviewResponse(BaseModel):
    review: str


class KubernetesReviewRequest(BaseModel):
    manifest: str


class KubernetesReviewResponse(BaseModel):
    review: str


class TerraformReviewRequest(BaseModel):
    terraform: str


class TerraformReviewResponse(BaseModel):
    review: str


class LogExplanationRequest(BaseModel):
    logs: str


class LogExplanationResponse(BaseModel):
    explanation: str
