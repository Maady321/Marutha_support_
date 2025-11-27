from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
from datetime import datetime


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)

    scheduled_time = Column(DateTime, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String, default="scheduled")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
