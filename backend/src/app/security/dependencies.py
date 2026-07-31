from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.oauth2 import get_current_user_id
from app.services.auth_service import AuthService


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db),
) -> User:
    repository = UserRepository(session)
    service = AuthService(repository)

    return await service.get_current_user(user_id)
