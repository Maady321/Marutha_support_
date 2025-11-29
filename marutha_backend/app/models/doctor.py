from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    specialization = Column(String(200), nullable=True, index=True)
    qualifications = Column(Text, nullable=True)
    experience_years = Column(Integer, nullable=True)
    phone = Column(String(30), nullable=True)
    bio = Column(Text, nullable=True)
    clinic_address = Column(Text, nullable=True)

    available = Column(Boolean, nullable=False, server_default="true")
    is_active = Column(Boolean, nullable=False, server_default="true")

    from sqlalchemy.sql import func
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # relationships
    user = relationship("User", backref="doctor", uselist=False)
    patients = relationship("Patient", backref="assigned_doctor", lazy="select")
    consultations = relationship("Consultation", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Doctor id={self.id} user_id={self.user_id} specialization={self.specialization}"
