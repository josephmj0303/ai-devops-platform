from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import get_settings
from app.core.security import decode_token
from app.services.user_service import UserRecord, UserService

bearer_scheme = HTTPBearer(auto_error=False)


def get_user_service() -> UserService:
    return UserService()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRecord:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        payload = decode_token(credentials.credentials, settings)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    user = user_service.get_by_id(str(payload.get("sub", "")))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown token subject",
        )
    return user
