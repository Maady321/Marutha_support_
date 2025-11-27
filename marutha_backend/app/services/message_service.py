from sqlalchemy.orm import Session
from app.models.message import Message

def send_message(db: Session, sender_id: str, receiver_id: str, content: str):
    msg = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_conversation(db: Session, user1: str, user2: str):
    return db.query(Message).filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).order_by(Message.created_at.asc()).all()


def get_unread(db: Session, user_id: str):
    return db.query(Message).filter(
        Message.receiver_id == user_id,
        Message.is_read == False
    ).order_by(Message.created_at.desc()).all()


def mark_as_read(db: Session, message_id: str, user_id: str):
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.receiver_id == user_id
    ).first()

    if not message:
        return None

    message.is_read = True
    db.commit()
    db.refresh(message)
    return message
