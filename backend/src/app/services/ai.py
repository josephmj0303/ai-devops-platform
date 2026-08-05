from app.providers import get_provider


class AIService:
    def __init__(self):
        self.provider = get_provider()

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        return await self.provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )
