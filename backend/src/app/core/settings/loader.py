from functools import lru_cache

from app.core.settings.ai import AISettings
from app.core.settings.api import APISettings
from app.core.settings.app import AppSettings
from app.core.settings.cors import CORSSettings
from app.core.settings.database import DatabaseSettings
from app.core.settings.observability import ObservabilitySettings
from app.core.settings.redis import RedisSettings
from app.core.settings.security import SecuritySettings


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
