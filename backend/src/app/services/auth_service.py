from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, Token
from app.security.hashing import PasswordHasher
from app.security.jwt import create_access_token


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(
        self,
        request: LoginRequest,
    ) -> Token:

        user = await self.repository.get_by_email(request.email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not PasswordHasher.verify(
            request.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password")

        token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        return Token(
            access_token=token
        )
