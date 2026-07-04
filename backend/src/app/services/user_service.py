from dataclasses import dataclass

from app.core.security import hash_password, verify_password


@dataclass(frozen=True)
class UserRecord:
    id: str
    email: str
    name: str
    role: str
    hashed_password: str


class UserService:
    """User lookup abstraction; replace in-memory storage with persistence later."""

    def __init__(self) -> None:
        self._users_by_email = {
            "admin@example.com": UserRecord(
                id="00000000-0000-4000-8000-000000000001",
                email="admin@example.com",
                name="Platform Admin",
                role="admin",
                hashed_password=hash_password("ChangeMe123!"),
            )
        }

    def authenticate(self, email: str, password: str) -> UserRecord | None:
        user = self._users_by_email.get(email.lower())
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_id(self, user_id: str) -> UserRecord | None:
        return next((user for user in self._users_by_email.values() if user.id == user_id), None)
