from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: str
    content: str

class MessageOut(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
