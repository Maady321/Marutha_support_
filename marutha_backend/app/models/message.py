from sqlalchemy import Column, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
