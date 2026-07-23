from passlib.context import CryptContext


class PasswordHasher:
    """
    Handles password hashing and verification.
    """

    _pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @classmethod
    def hash(cls, password: str) -> str:
        """
        Hash a plain-text password.
        """
        return cls._pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        """
        return cls._pwd_context.verify(
            plain_password,
            hashed_password,
        )
