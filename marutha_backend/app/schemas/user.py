# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = "patient"

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    is_active: bool
    profile_photo_url: Optional[str] = None

    class Config:
        from_attributes = True
