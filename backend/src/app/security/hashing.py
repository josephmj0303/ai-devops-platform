from pwdlib import PasswordHash


class PasswordHasher:
    """
    Handles password hashing and verification.
    """

    _password_hash = PasswordHash.recommended()

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._password_hash.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._password_hash.verify(plain_password, hashed_password)
