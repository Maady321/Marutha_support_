# app/routers/volunteers.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.volunteer import VolunteerCreate, VolunteerUpdate, VolunteerOut
from app.services.volunteer_service import (
    list_volunteers, get_volunteer_by_id, create_volunteer, update_volunteer, delete_volunteer
)
from app.core.deps import get_db, get_current_user
from app.core.roles import require_role

router = APIRouter(prefix="/volunteers", tags=["volunteers"])


@router.get("/", response_model=List[VolunteerOut])
def read_volunteers(skip: int = 0, limit: int = 50, active: Optional[bool] = Query(None),
                    current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    return list_volunteers(db, skip=skip, limit=limit, active=active)


@router.post("/", response_model=VolunteerOut, status_code=status.HTTP_201_CREATED)
def create_new_volunteer(payload: VolunteerCreate, current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    return create_volunteer(db, payload, created_by=current_user.id)


@router.get("/{volunteer_id}", response_model=VolunteerOut)
def read_volunteer(volunteer_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    v = get_volunteer_by_id(db, volunteer_id)
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return v


@router.put("/{volunteer_id}", response_model=VolunteerOut)
def put_volunteer(volunteer_id: str, payload: VolunteerUpdate, current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    v = get_volunteer_by_id(db, volunteer_id)
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    data = payload.dict(exclude_unset=True)
    return update_volunteer(db, v, data)


@router.delete("/{volunteer_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_volunteer(volunteer_id: str, current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    v = get_volunteer_by_id(db, volunteer_id)
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    delete_volunteer(db, v)
    return None
