from pydantic_settings import BaseSettings, SettingsConfigDict


class ObservabilitySettings(BaseSettings):

    LOG_LEVEL: str = "INFO"

    ENABLE_METRICS: bool = True

    ENABLE_TRACING: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
