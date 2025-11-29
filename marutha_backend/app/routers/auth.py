from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, UserOut
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_tokens
)
from app.core.security import REFRESH_SECRET, ALGORITHM
from app.core.deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user.email, user.password, user.name, user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(db, user.email, user.password)
        access_token, refresh_token = create_tokens(db_user.id)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
