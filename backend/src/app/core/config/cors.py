from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseSettings):

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
