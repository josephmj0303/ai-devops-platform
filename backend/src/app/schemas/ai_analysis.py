from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIAnalysisResponse(BaseModel):
    id: int
    user_id: UUID
    analysis_type: str
    input_text: str
    result: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
