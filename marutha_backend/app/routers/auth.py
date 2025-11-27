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

router = APIRouter(prefix="/auth", tags=["Auth"])
