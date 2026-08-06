import httpx

from app.core.settings import get_settings

from .base import AIProvider

settings = get_settings()


class OllamaProvider(AIProvider):
    """Ollama AI provider using the REST API."""

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:

        payload = {
            "model": settings.ai.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=300.0) as client:

            response = await client.post(
                f"{settings.ai.OLLAMA_BASE_URL}/api/generate",
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data["response"]
