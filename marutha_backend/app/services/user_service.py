# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException, status
from typing import Optional

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session, skip: int = 0, limit: int = 50, role: Optional[str] = None):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    return q.offset(skip).limit(limit).all()

def create_user(db: Session, email: str, password: str, name: str, role: str = "patient") -> User:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    user = User(email=email, hashed_password=hash_password(password), name=name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, data: dict) -> User:
    for k, v in data.items():
        if k == "password" and v is not None:
            setattr(user, "hashed_password", hash_password(v))
        elif hasattr(user, k) and v is not None:
            setattr(user, k, v)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
