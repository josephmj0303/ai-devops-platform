from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    DockerReviewRequest,
    DockerReviewResponse,
    KubernetesReviewRequest,
    KubernetesReviewResponse,
    TerraformReviewRequest,
    TerraformReviewResponse,
    LogExplanationRequest,
    LogExplanationResponse,
    DevOpsAnalysisResponse,
    DockerAnalysisResponse,
    KubernetesAnalysisResponse,
    TerraformAnalysisResponse,
)
from app.security.dependencies import get_current_user
from app.services.ai import AIService

from app.prompts.chat import build_chat_prompt
from app.prompts.dockerfile import (build_dockerfile_review_prompt, build_structured_dockerfile_analysis_prompt,)
from app.prompts.kubernetes import (build_kubernetes_review_prompt, build_structured_kubernetes_analysis_prompt,)
from app.prompts.terraform import (build_terraform_review_prompt, build_structured_terraform_analysis_prompt,)
from app.prompts.logs import (build_log_analysis_prompt, build_structured_log_analysis_prompt,)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.ai_analysis import AIAnalysisRepository
from app.schemas.ai_analysis import AIAnalysisResponse
from app.services.ai_analysis import AIAnalysisService

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

    prompt = build_chat_prompt(request.prompt)

    response = await service.generate(
        prompt=prompt,
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

    prompt = build_dockerfile_review_prompt(
        request.dockerfile
    )

    response = await service.generate(
        prompt=prompt
    )

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

    prompt = build_kubernetes_review_prompt(
        request.manifest
    )

    response = await service.generate(
        prompt=prompt
    )

    return KubernetesReviewResponse(review=response)


@router.post(
    "/review/terraform",
    response_model=TerraformReviewResponse,
)
async def review_terraform(
    request: TerraformReviewRequest,
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_terraform_review_prompt(
        request.terraform
    )

    response = await service.generate(
        prompt=prompt
    )

    return TerraformReviewResponse(review=response)


@router.post(
    "/explain/log",
    response_model=LogExplanationResponse,
)
async def explain_log(
    request: LogExplanationRequest,
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_log_analysis_prompt(
        request.logs
    )

    response = await service.generate(
        prompt=prompt
    )

    return LogExplanationResponse(
        explanation=response
    )


@router.post(
    "/analyze/logs",
    response_model=DevOpsAnalysisResponse,
)
async def analyze_logs(
    request: LogExplanationRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_structured_log_analysis_prompt(
        request.logs
    )

    analysis = await service.analyze_logs(
        prompt=prompt
    )

    repository = AIAnalysisRepository(session)
    analysis_service = AIAnalysisService(repository)

    await analysis_service.create_analysis(
        user_id=current_user.id,
        analysis_type="logs",
        input_text=request.logs,
        result=analysis,
    )

    return DevOpsAnalysisResponse(**analysis)


@router.post(
    "/analyze/dockerfile",
    response_model=DockerAnalysisResponse,
)
async def analyze_dockerfile(
    request: DockerReviewRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_structured_dockerfile_analysis_prompt(
        request.dockerfile
    )

    analysis = await service.analyze_dockerfile(
        prompt=prompt
    )

    repository = AIAnalysisRepository(session)
    analysis_service = AIAnalysisService(repository)

    await analysis_service.create_analysis(
        user_id=current_user.id,
        analysis_type="dockerfile",
        input_text=request.dockerfile,
        result=analysis,
    )

    return DockerAnalysisResponse(**analysis)


@router.post(
    "/analyze/kubernetes",
    response_model=KubernetesAnalysisResponse,
)
async def analyze_kubernetes(
    request: KubernetesReviewRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_structured_kubernetes_analysis_prompt(
        request.manifest
    )

    analysis = await service.analyze_kubernetes(
        prompt=prompt
    )

    repository = AIAnalysisRepository(session)
    analysis_service = AIAnalysisService(repository)

    await analysis_service.create_analysis(
        user_id=current_user.id,
        analysis_type="kubernetes",
        input_text=request.manifest,
        result=analysis,
    )

    return KubernetesAnalysisResponse(**analysis)


@router.post(
    "/analyze/terraform",
    response_model=TerraformAnalysisResponse,
)
async def analyze_terraform(
    request: TerraformReviewRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AIService()

    prompt = build_structured_terraform_analysis_prompt(
        request.terraform
    )

    analysis = await service.analyze_terraform(
        prompt=prompt
    )

    repository = AIAnalysisRepository(session)
    analysis_service = AIAnalysisService(repository)

    await analysis_service.create_analysis(
        user_id=current_user.id,
        analysis_type="terraform",
        input_text=request.terraform,
        result=analysis,
    )

    return TerraformAnalysisResponse(**analysis)


@router.get(
    "/history",
    response_model=list[AIAnalysisResponse],
)
async def get_analysis_history(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = AIAnalysisRepository(session)
    service = AIAnalysisService(repository)

    return await service.list_user_analyses(
        current_user.id
    )
