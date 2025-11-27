# app/schemas/volunteer.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class VolunteerBase(BaseModel):
    user_id: Optional[uuid.UUID] = None  # optional link to a users table account
    phone: Optional[str] = None
    skills: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = True
    location: Optional[str] = None


class VolunteerCreate(VolunteerBase):
    user_id: Optional[uuid.UUID] = None
    phone: Optional[str] = None


class VolunteerUpdate(BaseModel):
    phone: Optional[str] = None
    skills: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    location: Optional[str] = None


class VolunteerOut(VolunteerBase):
    id: uuid.UUID
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
