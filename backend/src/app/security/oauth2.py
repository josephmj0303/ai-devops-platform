from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.security.jwt import InvalidTokenError, verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:

    try:
        payload = verify_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return int(user_id)

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
