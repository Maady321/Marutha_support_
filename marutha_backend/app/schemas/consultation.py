from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------------------------------
# Base Schema
# -----------------------------------------------------
class ConsultationBase(BaseModel):
    patient_id: str
    doctor_id: str
    scheduled_time: datetime
    reason: Optional[str] = None


# -----------------------------------------------------
# Create Consultation
# -----------------------------------------------------
class ConsultationCreate(ConsultationBase):
    pass


# -----------------------------------------------------
# Update Consultation
# -----------------------------------------------------
class ConsultationUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None  # pending / approved / completed / cancelled


# -----------------------------------------------------
# Output Schema
# -----------------------------------------------------
from uuid import UUID

# -----------------------------------------------------
# Output Schema
# -----------------------------------------------------
class ConsultationOut(BaseModel):
    id: UUID
    patient_id: UUID
    doctor_id: UUID
    scheduled_time: datetime
    reason: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
