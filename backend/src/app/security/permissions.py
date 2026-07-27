from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.security.oauth2 import get_current_user_id


def require_roles(*roles: str) -> Callable:
    async def checker(
        user_id: UUID = Depends(get_current_user_id),
        session: AsyncSession = Depends(get_db),
    ):
        repository = UserRepository(session)
        user = await repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return checker

require_admin = require_roles("admin")

require_developer = require_roles(
    "admin",
    "developer",
)

require_authenticated = require_roles(
    "admin",
    "developer",
    "viewer",
)
