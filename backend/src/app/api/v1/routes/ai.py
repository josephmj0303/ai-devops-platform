from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse
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
    """
    Generate an AI response.
    """

    service = AIService()

    response = await service.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    )

    return AIChatResponse(response=response)
