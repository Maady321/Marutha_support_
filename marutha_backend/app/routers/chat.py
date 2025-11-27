from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.schemas.message import MessageCreate, MessageOut
from app.services.message_service import (
    send_message, get_conversation, get_unread, mark_as_read
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/send", response_model=MessageOut)
def send(msg: MessageCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return send_message(db, current_user.id, msg.receiver_id, msg.content)


@router.get("/conversation/{user_id}", response_model=list[MessageOut])
def conversation(user_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_conversation(db, current_user.id, user_id)


@router.get("/unread", response_model=list[MessageOut])
def unread_messages(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_unread(db, current_user.id)


@router.patch("/read/{message_id}", response_model=MessageOut)
def mark_read(message_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    msg = mark_as_read(db, message_id, current_user.id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found or not authorized")
    return msg
