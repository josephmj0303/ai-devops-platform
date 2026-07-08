from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "AI DevOps Platform"

    APP_VERSION: str = "0.1.0"

    ENVIRONMENT: str = Field(default="local")

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )
