from app.core.settings import get_settings

from .ollama import OllamaProvider
from .openai import OpenAIProvider

settings = get_settings()

def get_provider():
    """
    Return the configured AI provider.
    """

    provider = settings.ai.PROVIDER.lower()

    if provider == "ollama":
        return OllamaProvider()

    if provider == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {provider}"
    )
