from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.db.session import get_db


def get_app_settings():
    return get_settings()


async def get_db_session(
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    return db
