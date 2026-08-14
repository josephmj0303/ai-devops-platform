from uuid import UUID

from app.models.ai_analysis import AIAnalysis
from app.repositories.ai_analysis import AIAnalysisRepository


class AIAnalysisService:
    def __init__(self, repository: AIAnalysisRepository):
        self.repository = repository

    async def create_analysis(
        self,
        user_id: UUID,
        analysis_type: str,
        input_text: str,
        result: dict,
    ) -> AIAnalysis:
        analysis = AIAnalysis(
            user_id=user_id,
            analysis_type=analysis_type,
            input_text=input_text,
            result=result,
        )

        return await self.repository.create(analysis)

    async def list_user_analyses(
        self,
        user_id: UUID,
    ) -> list[AIAnalysis]:
        return await self.repository.list_by_user(user_id)

    async def get_analysis(
        self,
        analysis_id: int,
    ) -> AIAnalysis | None:
        return await self.repository.get_by_id(analysis_id)
