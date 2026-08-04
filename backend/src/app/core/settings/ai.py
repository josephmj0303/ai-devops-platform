from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """
    AI Provider Configuration
    """

    # Active AI Provider
    PROVIDER: str = "openai"

    # OpenAI
    OPENAI_API_KEY: SecretStr = SecretStr("")
    OPENAI_MODEL: str = "gpt-5.5"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
