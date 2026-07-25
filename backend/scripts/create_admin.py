import asyncio
import sys
from pathlib import Path

# Add backend/src to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.security.hashing import PasswordHasher


async def create_admin():
    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("Admin user already exists.")
            return

        admin = User(
            email="admin@example.com",
            username="admin",
            full_name="Platform Administrator",
            hashed_password=PasswordHasher.hash("Admin@123"),
            role="admin",
            is_active=True,
            is_verified=True,
        )

        session.add(admin)

        await session.commit()

        print("Admin user created successfully.")


if __name__ == "__main__":
    asyncio.run(create_admin())
