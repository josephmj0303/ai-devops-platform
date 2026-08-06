from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    DockerReviewRequest,
    DockerReviewResponse,
    KubernetesReviewRequest,
    KubernetesReviewResponse,
)
from app.security.dependencies import get_current_user
from app.services.ai import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
async def chat(
    request: AIChatRequest,
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    response = await service.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    )

    return AIChatResponse(response=response)


@router.post(
    "/review/dockerfile",
    response_model=DockerReviewResponse,
)
async def review_dockerfile(
    request: DockerReviewRequest,
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = f"""
You are an experienced DevOps Engineer.

Review the following Dockerfile.

Focus on:

- Security
- Image size
- Best practices
- Performance
- Production readiness

Dockerfile:

{request.dockerfile}
"""

    response = await service.generate(prompt=prompt)

    return DockerReviewResponse(review=response)

@router.post(
    "/review/kubernetes",
    response_model=KubernetesReviewResponse,
)
async def review_kubernetes(
    request: KubernetesReviewRequest,
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = f"""
You are an experienced Kubernetes and DevOps Engineer.

Review the following Kubernetes manifest.

Focus on:

- Resource requests and limits
- Liveness probe
- Readiness probe
- Security context
- Labels and selectors
- Image version
- Production readiness

Provide practical recommendations.

Manifest:

{request.manifest}
"""

    response = await service.generate(prompt=prompt)

    return KubernetesReviewResponse(review=response)
