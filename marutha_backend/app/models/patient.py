import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    medical_history = sa.Column(sa.Text, nullable=True)
    dob = sa.Column(sa.Date, nullable=True)
    gender = sa.Column(sa.String(20), nullable=True)
    address = sa.Column(sa.Text, nullable=True)

    # Foreign key to Doctor
    doctor_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("doctors.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Correct foreign key to Stage table
    current_stage_id = sa.Column(UUID(as_uuid=True), nullable=True)

    created_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )

    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("User", backref="patient", uselist=False)

    # Patient has many stages
    stages = relationship(
        "Stage", back_populates="patient", cascade="all, delete-orphan"
    )

    consultations = relationship(
        "Consultation", back_populates="patient", cascade="all, delete-orphan"
    )
