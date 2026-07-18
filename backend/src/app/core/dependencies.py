from app.core.settings import get_settings


def get_app_settings():
    """
    Dependency for application settings.
    """

    return get_settings()
