from .base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI provider."""

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        raise NotImplementedError(
            "OpenAI provider not implemented yet."
        )
