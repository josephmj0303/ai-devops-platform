from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_analysis import AIAnalysis


class AIAnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        analysis: AIAnalysis,
    ) -> AIAnalysis:
        self.db.add(analysis)

        await self.db.commit()
        await self.db.refresh(analysis)

        return analysis

    async def list_by_user(
        self,
        user_id,
    ) -> list[AIAnalysis]:
        result = await self.db.execute(
            select(AIAnalysis)
            .where(AIAnalysis.user_id == user_id)
            .order_by(AIAnalysis.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        analysis_id: int,
    ) -> AIAnalysis | None:
        result = await self.db.execute(
            select(AIAnalysis)
            .where(AIAnalysis.id == analysis_id)
        )

        return result.scalar_one_or_none()
