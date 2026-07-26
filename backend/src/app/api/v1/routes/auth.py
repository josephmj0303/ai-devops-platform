from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, Token, CurrentUser
from app.services.auth_service import AuthService
from uuid import UUID
from app.security.oauth2 import get_current_user_id


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    repository = UserRepository(session)
    service = AuthService(repository)

    try:
        return await service.login(request)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

@router.get("/me", response_model=CurrentUser)
async def me(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
):
    repository = UserRepository(session)
    service = AuthService(repository)

    try:
        return await service.get_current_user(user_id)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
