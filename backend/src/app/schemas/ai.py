from typing import Literal

from pydantic import BaseModel, Field

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


class DevOpsAnalysisResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    component: str = Field(min_length=1, max_length=100)
    summary: str
    likely_cause: str
    impact: str
    recommended_actions: list[str] = Field(min_length=1)

class DockerAnalysisResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    component: str = Field(min_length=1, max_length=100)
    summary: str
    findings: list[str] = Field(min_length=1)
    recommended_actions: list[str] = Field(min_length=1)

class KubernetesAnalysisResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    component: str = Field(min_length=1, max_length=100)
    summary: str
    findings: list[str] = Field(min_length=1)
    recommended_actions: list[str] = Field(min_length=1)

class TerraformAnalysisResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    component: str = Field(min_length=1, max_length=100)
    summary: str
    findings: list[str] = Field(min_length=1)
    recommended_actions: list[str] = Field(min_length=1)
