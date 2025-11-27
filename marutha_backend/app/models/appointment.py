from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)

    datetime_start = Column(DateTime(timezone=True), nullable=False)
    datetime_end = Column(DateTime(timezone=True), nullable=False)

    visit_type = Column(String(50), default="in_person")
    reason = Column(Text)
    notes = Column(Text)

    status = Column(String(30), default="pending")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
