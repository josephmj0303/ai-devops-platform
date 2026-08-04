from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
from app.core.config import settings


def get_provider():
    """
    Return the configured AI provider.
    """

    provider = settings.AI_PROVIDER.lower()

    if provider == "ollama":
        return OllamaProvider()

    if provider == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )
