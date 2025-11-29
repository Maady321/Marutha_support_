from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class AppointmentBase(BaseModel):
    patient_id: uuid.UUID
    doctor_id: uuid.UUID
    datetime_start: datetime
    datetime_end: datetime
    visit_type: str = "in_person"
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    visit_type: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class AppointmentOut(AppointmentBase):
    id: uuid.UUID
    status: str
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
