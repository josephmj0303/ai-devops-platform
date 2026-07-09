from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):

    OPENAI_API_KEY: SecretStr = SecretStr("")

    MODEL_NAME: str = "gpt-5.5"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
