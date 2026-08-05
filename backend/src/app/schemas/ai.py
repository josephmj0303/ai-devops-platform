from pydantic import BaseModel


class AIChatRequest(BaseModel):
    prompt: str
    system_prompt: str | None = None


class AIChatResponse(BaseModel):
    response: str

