# app/routers/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.roles import require_role
from app.core.deps import get_db, get_current_user
from app.services.user_service import (
    list_users, get_user_by_id, create_user, update_user, delete_user
)
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

# Public (Admin protected) endpoints

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 50, role: Optional[str] = None,
               current_user = Depends(require_role("admin")) , db: Session = Depends(get_db)):
    return list_users(db, skip=skip, limit=limit, role=role)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(payload: UserCreate, current_user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return create_user(db, payload.email, payload.password, payload.name, payload.role)

@router.get("/me", response_model=UserOut)
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, current_user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def put_user(user_id: str, payload: UserUpdate, current_user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    data = payload.dict(exclude_unset=True)
    # allow admin to reset password by providing "password" field
    return update_user(db, user, data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: str, current_user = Depends(require_role("admin")), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return None
