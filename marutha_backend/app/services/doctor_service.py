# app/services/doctor_service.py
from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.core.security import hash_password
from datetime import datetime


# ---------------------------
# CREATE DOCTOR
# ---------------------------
def create_doctor(db: Session, data: dict):
    from uuid import UUID
    if 'user_id' in data and isinstance(data['user_id'], str):
        data['user_id'] = UUID(data['user_id'])
    doctor = Doctor(**data)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


# ---------------------------
# GET ALL DOCTORS
# ---------------------------
def list_doctors(db: Session, skip: int = 0, limit: int = 50, available: bool = None):
    query = db.query(Doctor)

    if available is not None:
        query = query.filter(Doctor.available == available)

    return query.offset(skip).limit(limit).all()


# ---------------------------
# GET SINGLE DOCTOR
# ---------------------------
def get_doctor_by_id(db: Session, doctor_id: str):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def get_doctor_by_user(db: Session, user_id: str):
    return db.query(Doctor).filter(Doctor.user_id == user_id).first()


# ---------------------------
# UPDATE DOCTOR
# ---------------------------
def update_doctor(db: Session, doctor: Doctor, data: dict):
    for key, value in data.items():
        setattr(doctor, key, value)

    doctor.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(doctor)
    return doctor


# ---------------------------
# DELETE DOCTOR
# ---------------------------
def delete_doctor(db: Session, doctor: Doctor):
    db.delete(doctor)
    db.commit()
    return True


# ---------------------------
# UPDATE AVAILABILITY
# ---------------------------
def update_availability(db: Session, doctor: Doctor, available: bool):
    doctor.available = available
    doctor.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(doctor)
    return doctor
