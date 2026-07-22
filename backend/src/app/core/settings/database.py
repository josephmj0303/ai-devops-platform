from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_devops"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
