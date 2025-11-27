# app/services/medication_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.models.medication import Medication, MedicationStatus
from app.models.user import User  # if needed
from app.models.patient import Patient  # ensure import path matches your project

def list_medications_for_patient(db: Session, patient_id: UUID, skip: int = 0, limit: int = 100) -> List[Medication]:
    return db.query(Medication).filter(Medication.patient_id == patient_id, Medication.is_active == True).offset(skip).limit(limit).all()

def get_medication(db: Session, medication_id: UUID) -> Optional[Medication]:
    return db.query(Medication).filter(Medication.id == medication_id, Medication.is_active == True).first()

def create_medication(db: Session, patient_id: UUID, payload, created_by: UUID = None) -> Medication:
    med = Medication(
        patient_id=patient_id,
        name=payload.name,
        dosage=payload.dosage,
        frequency=payload.frequency,
        route=payload.route,
        instructions=payload.instructions,
        start_date=payload.start_date,
        end_date=payload.end_date,
        prescribed_by=getattr(payload, "prescribed_by", None),
        created_by=created_by
    )
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

def update_medication(db: Session, med: Medication, patch: dict) -> Medication:
    for k, v in patch.items():
        if hasattr(med, k):
            setattr(med, k, v)
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

def stop_medication(db: Session, med: Medication, reason: Optional[str] = None, stopped_by: Optional[UUID] = None) -> Medication:
    med.status = MedicationStatus.STOPPED
    if reason:
        med.reason_for_stop = reason
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

def record_administration(db: Session, med: Medication, when: Optional[datetime] = None) -> Medication:
    med.last_administered_at = when or datetime.utcnow()
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

def add_missed_dose(db: Session, med: Medication, missed_date_str: str) -> Medication:
    # Append comma-separated missed dates (simple approach)
    if med.missed_doses:
        med.missed_doses = f"{med.missed_doses},{missed_date_str}"
    else:
        med.missed_doses = missed_date_str
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

def delete_medication(db: Session, med: Medication):
    # soft-delete pattern
    med.is_active = False
    db.add(med)
    db.commit()
    return
