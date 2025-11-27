# app/routers/medications.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import SessionLocal
from app.schemas.medication import MedicationCreate, MedicationOut, MedicationUpdate
from app.services.medication_service import (
    list_medications_for_patient, get_medication, create_medication, update_medication,
    stop_medication, record_administration, add_missed_dose, delete_medication
)
from app.core.deps import get_db, get_current_user
from app.core.roles import require_role

router = APIRouter(prefix="/medications", tags=["medications"])

# get meds for a patient
@router.get("/patient/{patient_id}", response_model=List[MedicationOut])
def get_meds_for_patient(patient_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_medications_for_patient(db, patient_id, skip=skip, limit=limit)

@router.post("/patient/{patient_id}", response_model=MedicationOut, status_code=status.HTTP_201_CREATED)
def create_med(patient_id: UUID, payload: MedicationCreate, db: Session = Depends(get_db), current_user = Depends(require_role("doctor"))):
    med = create_medication(db, patient_id, payload, created_by=current_user.id)
    return med

@router.get("/{med_id}", response_model=MedicationOut)
def read_med(med_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return med

@router.put("/{med_id}", response_model=MedicationOut)
def put_med(med_id: UUID, payload: MedicationUpdate, db: Session = Depends(get_db), current_user = Depends(require_role("doctor"))):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    data = payload.dict(exclude_unset=True)
    return update_medication(db, med, data)

@router.patch("/{med_id}/stop", response_model=MedicationOut)
def stop_med_endpoint(med_id: UUID, reason: str = None, db: Session = Depends(get_db), current_user = Depends(require_role("doctor"))):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return stop_medication(db, med, reason=reason, stopped_by=current_user.id)

@router.patch("/{med_id}/administer", response_model=MedicationOut)
def administer_med(med_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return record_administration(db, med)

@router.patch("/{med_id}/missed", response_model=MedicationOut)
def missed_dose(med_id: UUID, missed_date: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return add_missed_dose(db, med, missed_date)

@router.delete("/{med_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_med(med_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    med = get_medication(db, med_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    delete_medication(db, med)
    return None
