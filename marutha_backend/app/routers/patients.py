# app/routers/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.deps import get_db, get_current_user
from app.core.roles import require_role
from app.services.patient_service import (
    create_patient, get_patient, get_patient_by_user_id, list_patients,
    update_patient, delete_patient, add_stage, get_stages, get_progression
)
from app.schemas.patient import (
    PatientCreate, PatientOut, PatientUpdate, StageCreate, StageOut, ProgressPoint
)
from app.models.patient import Patient as PatientModel

router = APIRouter(prefix="/patients", tags=["patients"])

# Create patient (admin or doctor can create a patient record for an existing user)
@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient_record(payload: PatientCreate, db: Session = Depends(get_db),
                          current_user = Depends(require_role("admin", "doctor"))):
    patient = create_patient(db, payload.user_id, payload.medical_history, payload.dob, payload.gender, payload.address)
    return patient

# List patients - admin and doctor only
@router.get("/", response_model=List[PatientOut])
def read_patients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db),
                  current_user = Depends(require_role("admin", "doctor"))):
    return list_patients(db, skip=skip, limit=limit)

# Read single patient - owner (patient) can read their own, admin/doctor can read any
@router.get("/{patient_id}", response_model=PatientOut)
def read_patient(patient_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # allow owner
    if current_user.role == "patient":
        own = get_patient_by_user_id(db, current_user.id)
        if not own or str(own.id) != str(patient_id):
            raise HTTPException(status_code=403, detail="Not authorized to view this patient")
    # allow admin/doctor
    elif current_user.role not in ("admin", "doctor"):
        raise HTTPException(status_code=403, detail="Not authorized to view this patient")

    return patient

# Update patient - admin/doctor
@router.put("/{patient_id}", response_model=PatientOut)
def put_patient(patient_id: str, payload: PatientUpdate, db: Session = Depends(get_db),
                current_user = Depends(require_role("admin", "doctor"))):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    data = payload.dict(exclude_unset=True)
    return update_patient(db, patient, data)

# Delete patient - admin only
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_patient(patient_id: str, db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    delete_patient(db, patient)
    return None

# Add stage entry - doctor or admin can add a stage
@router.post("/{patient_id}/stages", response_model=StageOut, status_code=status.HTTP_201_CREATED)
def create_stage(patient_id: str, payload: StageCreate, db: Session = Depends(get_db), current_user = Depends(require_role("admin", "doctor"))):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    stage = add_stage(db, patient, payload.stage_name, recorded_by=current_user.id, notes=payload.notes)
    return stage

# Get stage history - owner or admin/doctor
@router.get("/{patient_id}/stages", response_model=List[StageOut])
def list_stage_history(patient_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # owner allowed
    if current_user.role == "patient":
        own = get_patient_by_user_id(db, current_user.id)
        if not own or str(own.id) != str(patient_id):
            raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role not in ("admin", "doctor"):
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_stages(db, patient)

# Get progression data (graph-ready)
@router.get("/{patient_id}/progression", response_model=List[ProgressPoint])
def progression(patient_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    patient = get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # same access rules as above
    if current_user.role == "patient":
        own = get_patient_by_user_id(db, current_user.id)
        if not own or str(own.id) != str(patient_id):
            raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role not in ("admin", "doctor"):
        raise HTTPException(status_code=403, detail="Not authorized")
    raw = get_progression(db, patient)
    # map to ProgressPoint
    return [{"stage_name": r["stage_name"], "recorded_at": r["recorded_at"], "notes": r["notes"]} for r in raw]
