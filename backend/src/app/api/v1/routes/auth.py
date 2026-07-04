from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_user_service
from app.core.config import Settings, get_settings
from app.core.security import create_access_token
from app.models.auth import LoginRequest, TokenResponse, UserPublic
from app.services.user_service import UserRecord, UserService

router = APIRouter(prefix="/auth", tags=["authentication"])


def to_public_user(user: UserRecord) -> UserPublic:
    return UserPublic(id=user.id, email=user.email, name=user.name, role=user.role)


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    settings: Annotated[Settings, Depends(get_settings)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> TokenResponse:
    user = user_service.authenticate(request.email, request.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(user.id, settings, {"role": user.role})
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.access_token_expire_minutes * 60,
        user=to_public_user(user),
    )


@router.get("/me", response_model=UserPublic)
def me(current_user: Annotated[UserRecord, Depends(get_current_user)]) -> UserPublic:
    return to_public_user(current_user)
