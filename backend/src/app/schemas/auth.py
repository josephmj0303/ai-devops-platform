from pydantic import BaseModel, EmailStr, Field


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str = "engineer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic
