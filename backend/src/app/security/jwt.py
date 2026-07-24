from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.settings import get_settings


class InvalidTokenError(Exception):
    """Raised when a JWT token is invalid or has expired."""
    pass


settings = get_settings()


def create_access_token(data: dict[str, Any]) -> str:
    """
    Create a signed JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.security.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.security.SECRET_KEY.get_secret_value(),
        algorithm=settings.security.ALGORITHM,
    )


def verify_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Returns:
        The decoded JWT payload.

    Raises:
        InvalidTokenError: If the token is invalid or has expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.security.SECRET_KEY.get_secret_value(),
            algorithms=[settings.security.ALGORITHM],
        )

        return payload

    except JWTError as exc:
        raise InvalidTokenError("Invalid or expired token") from exc
