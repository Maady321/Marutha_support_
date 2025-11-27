# app/models/medication.py
import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class MedicationStatus:
    ACTIVE = "active"
    STOPPED = "stopped"
    COMPLETED = "completed"

class Medication(Base):
    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)

    name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequency = Column(String(100), nullable=False)
    route = Column(String(100), nullable=True)
    instructions = Column(Text, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    status = Column(String(30), nullable=False, default=MedicationStatus.ACTIVE)
    reason_for_stop = Column(Text, nullable=True)
    last_administered_at = Column(DateTime(timezone=True), nullable=True)
    missed_doses = Column(String(255), nullable=True)

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    is_active = Column(Boolean, default=True)
