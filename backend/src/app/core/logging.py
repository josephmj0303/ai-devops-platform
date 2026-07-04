import logging
import sys

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure process-wide structured-enough logging for containers."""

    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
