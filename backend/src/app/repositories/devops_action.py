from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.devops_action import DevOpsAction


class DevOpsActionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        user_id,
        analysis_id: int,
        action: str,
        target: str,
        status: str,
        message: str,
    ) -> DevOpsAction:
        devops_action = DevOpsAction(
            user_id=user_id,
            analysis_id=analysis_id,
            action=action,
            target=target,
            status=status,
            message=message,
        )

        self.session.add(devops_action)
        await self.session.commit()
        await self.session.refresh(devops_action)

        return devops_action

    async def list_by_analysis(
        self,
        analysis_id: int,
    ) -> list[DevOpsAction]:
        result = await self.session.execute(
            select(DevOpsAction)
            .where(DevOpsAction.analysis_id == analysis_id)
            .order_by(DevOpsAction.created_at.desc())
        )

        return list(result.scalars().all())
