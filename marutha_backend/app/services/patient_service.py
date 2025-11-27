# app/services/patient_service.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.patient import Patient
from app.models.stage import Stage
from fastapi import HTTPException, status
from datetime import datetime

def create_patient(db: Session, user_id: str, medical_history: Optional[str]=None,
                   dob=None, gender: Optional[str]=None, address: Optional[str]=None) -> Patient:
    # ensure user doesn't already have a patient record
    existing = db.query(Patient).filter(Patient.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient record already exists for this user")
    patient = Patient(user_id=user_id, medical_history=medical_history, dob=dob, gender=gender, address=address)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patient_by_user_id(db: Session, user_id: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.user_id == user_id).first()

def list_patients(db: Session, skip: int = 0, limit: int = 50) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient: Patient, data: dict) -> Patient:
    for k, v in data.items():
        if v is not None and hasattr(patient, k):
            setattr(patient, k, v)
    patient.updated_at = datetime.utcnow()
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient: Patient) -> None:
    db.delete(patient)
    db.commit()

# Stage operations
def add_stage(db: Session, patient: Patient, stage_name: str, recorded_by: Optional[str], notes: Optional[str]=None) -> Stage:
    stage = Stage(patient_id=patient.id, stage_name=stage_name, recorded_by=recorded_by, notes=notes)
    db.add(stage)
    db.commit()
    db.refresh(stage)
    # update patient's current_stage_id
    patient.current_stage_id = stage.id
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return stage

def get_stages(db: Session, patient: Patient, skip: int = 0, limit: int = 100) -> List[Stage]:
    return db.query(Stage).filter(Stage.patient_id == patient.id).order_by(Stage.recorded_at.desc()).offset(skip).limit(limit).all()

def get_progression(db: Session, patient: Patient):
    stages = db.query(Stage).filter(Stage.patient_id == patient.id).order_by(Stage.recorded_at.asc()).all()
    # return list of dicts
    return [{"stage_name": s.stage_name, "recorded_at": s.recorded_at, "notes": s.notes} for s in stages]
