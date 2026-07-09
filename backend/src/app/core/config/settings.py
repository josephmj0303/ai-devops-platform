from functools import lru_cache

from app.core.config.ai import AISettings
from app.core.config.api import APISettings
from app.core.config.app import AppSettings
from app.core.config.cors import CORSSettings
from app.core.config.database import DatabaseSettings
from app.core.config.observability import ObservabilitySettings
from app.core.config.redis import RedisSettings
from app.core.config.security import SecuritySettings


class Settings:

    def __init__(self):

        self.app = AppSettings()

        self.api = APISettings()

        self.security = SecuritySettings()

        self.database = DatabaseSettings()

        self.redis = RedisSettings()

        self.ai = AISettings()

        self.observability = ObservabilitySettings()

        self.cors = CORSSettings()


@lru_cache
def get_settings():

    return Settings()
