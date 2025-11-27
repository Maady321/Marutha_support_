# app/schemas/medication.py
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field
from uuid import UUID

class MedicationBase(BaseModel):
    name: str = Field(..., example="Morphine")
    dosage: str = Field(..., example="10 mg")
    frequency: str = Field(..., example="Once daily")
    route: Optional[str] = Field(None, example="oral")
    instructions: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class MedicationCreate(MedicationBase):
    prescribed_by: Optional[UUID] = None

class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    instructions: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    reason_for_stop: Optional[str] = None
    last_administered_at: Optional[datetime] = None
    missed_doses: Optional[str] = None

class MedicationOut(MedicationBase):
    id: UUID
    patient_id: UUID
    prescribed_by: Optional[UUID]
    status: str
    reason_for_stop: Optional[str]
    last_administered_at: Optional[datetime]
    missed_doses: Optional[str]
    created_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
