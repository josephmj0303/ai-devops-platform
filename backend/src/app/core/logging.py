import logging
import sys

from app.core.settings import get_settings

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging() -> None:
    """
    Configure application logging.

    This configures the root logger so all application modules share
    a consistent logging format. Logs are written to stdout, making
    them compatible with Docker, Kubernetes, and centralized logging
    systems such as Loki and CloudWatch.
    """
    settings = get_settings()

    logging.basicConfig(
        level=settings.observability.LOG_LEVEL.upper(),
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Example:
        from app.core.logging import get_logger

        logger = get_logger(__name__)
        logger.info("Application started")
    """
    return logging.getLogger(name)
