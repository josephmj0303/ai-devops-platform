from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

class CurrentUser(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
