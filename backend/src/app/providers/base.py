from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract interface for AI providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        response_format: str | None = None,
    ) -> str:
        """
        Generate a response from an AI provider.
        """
        raise NotImplementedError
