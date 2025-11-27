from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token
)


def register_user(db: Session, email: str, password: str, name: str, role: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("User already exists")

    hashed = hash_password(password)
    new_user = User(
        email=email,
        hashed_password=hashed,
        name=name,
        role=role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    return user


def create_tokens(user_id: int):
    access = create_access_token({"user_id": user_id})
    refresh = create_refresh_token({"user_id": user_id})
    return access, refresh
