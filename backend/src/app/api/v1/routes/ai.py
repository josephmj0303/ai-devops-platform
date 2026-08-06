from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    DockerReviewRequest,
    DockerReviewResponse,
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
