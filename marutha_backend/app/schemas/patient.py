# app/schemas/patient.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class StageCreate(BaseModel):
    stage_name: str
    notes: Optional[str] = None

from uuid import UUID

class StageOut(BaseModel):
    id: UUID
    patient_id: UUID
    stage_name: str
    notes: Optional[str]
    recorded_by: Optional[UUID]
    recorded_at: datetime

    class Config:
        from_attributes = True

class PatientCreate(BaseModel):
    user_id: str   # FK to users.id
    medical_history: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None

class PatientUpdate(BaseModel):
    medical_history: Optional[str]
    dob: Optional[date]
    gender: Optional[str]
    address: Optional[str]

class PatientOut(BaseModel):
    id: UUID
    user_id: UUID
    medical_history: Optional[str]
    dob: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    current_stage_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProgressPoint(BaseModel):
    stage_name: str
    recorded_at: datetime
    notes: Optional[str]
