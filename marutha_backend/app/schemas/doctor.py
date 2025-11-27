# app/schemas/doctor.py
from pydantic import BaseModel, Field, constr, conint
from typing import Optional
from datetime import datetime

UUIDStr = constr(regex=r"^[0-9a-fA-F-]{36}$")  # basic UUID v4-ish check


class DoctorCreate(BaseModel):
    user_id: UUIDStr
    specialization: Optional[str] = None
    qualifications: Optional[str] = None
    experience_years: Optional[conint(ge=0)] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    clinic_address: Optional[str] = None
    available: Optional[bool] = True

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None
    qualifications: Optional[str] = None
    experience_years: Optional[conint(ge=0)] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    clinic_address: Optional[str] = None
    available: Optional[bool] = None
    is_active: Optional[bool] = None

class DoctorOut(BaseModel):
    id: str
    user_id: str
    specialization: Optional[str]
    qualifications: Optional[str]
    experience_years: Optional[int]
    phone: Optional[str]
    bio: Optional[str]
    clinic_address: Optional[str]
    available: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DoctorSummary(BaseModel):
    id: str
    user_id: str
    specialization: Optional[str]
    experience_years: Optional[int]
    available: bool

    class Config:
        orm_mode = True

class AvailabilityUpdate(BaseModel):
    available: bool = Field(..., description="Doctor availability on/off")
