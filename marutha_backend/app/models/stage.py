# app/models/stage.py
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base

class Stage(Base):
    __tablename__ = "stages"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_name = sa.Column(sa.String(100), nullable=False)
    notes = sa.Column(sa.Text, nullable=True)
    recorded_by = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    recorded_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)

    patient = relationship("Patient", back_populates="stages")
