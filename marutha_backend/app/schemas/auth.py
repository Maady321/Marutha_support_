from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = "patient"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
