from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    API_PREFIX: str = "/api"

    API_VERSION: str = "v1"

    OPENAPI_URL: str = "/openapi.json"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
