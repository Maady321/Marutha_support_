import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.String, nullable=False, default="patient")
    is_active = sa.Column(sa.Boolean, default=True)
