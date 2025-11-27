# app/services/volunteer_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.volunteer import Volunteer
from app.schemas.volunteer import VolunteerCreate, VolunteerUpdate
import uuid


def list_volunteers(db: Session, skip: int = 0, limit: int = 50, active: Optional[bool] = None) -> List[Volunteer]:
    q = db.query(Volunteer).offset(skip).limit(limit)
    if active is not None:
        q = q.filter(Volunteer.is_active == active)
    return q.all()


def get_volunteer_by_id(db: Session, volunteer_id: str) -> Optional[Volunteer]:
    return db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()


def create_volunteer(db: Session, payload: VolunteerCreate, created_by: str = None) -> Volunteer:
    v = Volunteer(
        user_id=payload.user_id,
        phone=payload.phone,
        skills=payload.skills,
        bio=payload.bio,
        location=payload.location,
        is_active=payload.is_active,
        created_by=created_by
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


def update_volunteer(db: Session, volunteer: Volunteer, data: dict) -> Volunteer:
    for key, value in data.items():
        if hasattr(volunteer, key):
            setattr(volunteer, key, value)
    db.commit()
    db.refresh(volunteer)
    return volunteer


def delete_volunteer(db: Session, volunteer: Volunteer):
    db.delete(volunteer)
    db.commit()
