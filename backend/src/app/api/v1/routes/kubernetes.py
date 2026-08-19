from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.kubernetes import KubernetesClusterSummary
from app.security.dependencies import get_current_user
from app.services.kubernetes import KubernetesService


router = APIRouter(
    prefix="/kubernetes",
    tags=["Kubernetes"],
)


@router.get(
    "/summary",
    response_model=KubernetesClusterSummary,
)
async def get_cluster_summary(
    current_user: User = Depends(get_current_user),
):
    service = KubernetesService()

    return service.get_cluster_summary()
