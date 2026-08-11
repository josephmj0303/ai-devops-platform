from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseSettings):

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://192.168.56.20:5173",
        "http://localhost:8080",
        "http://192.168.56.20:8080",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
