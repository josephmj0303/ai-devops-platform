from .base import AIProvider


class OllamaProvider(AIProvider):
    """Ollama AI provider."""

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        raise NotImplementedError(
            "Ollama provider not implemented yet."
        )
