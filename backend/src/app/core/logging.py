import logging
import sys

from app.core.settings import get_settings


def configure_logging() -> None:
    """
    Configure application logging.
    """

    settings = get_settings()

    logging.basicConfig(
        level=settings.observability.LOG_LEVEL,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.
    """
    return logging.getLogger(name)
