from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db
from app.core.roles import require_role
from app.schemas.consultation import (
    ConsultationCreate,
    ConsultationUpdate,
    ConsultationOut
)
from app.services.consultation_service import (
    create_consultation,
    list_consultations,
    get_consultation_by_id,
    update_consultation,
    delete_consultation
)



router = APIRouter(prefix="/consultations", tags=["consultations"])

# List all consultations (Admin only)
@router.get("/", response_model=List[ConsultationOut])
def get_consultations(db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    return list_consultations(db)

# Create consultation (Admin / Doctor)
@router.post("/", response_model=ConsultationOut)
def new_consultation(payload: ConsultationCreate, 
                     db: Session = Depends(get_db),
                     current_user = Depends(require_role("admin", "doctor"))):
    from uuid import UUID
    try:
        patient_uuid = UUID(payload.patient_id)
        doctor_uuid = UUID(payload.doctor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    return create_consultation(
        db,
        patient_uuid,
        doctor_uuid,
        payload.scheduled_time,
        payload.reason
    )

# Get single consultation
@router.get("/{consult_id}", response_model=ConsultationOut)
def read_consult(consult_id: str, 
                 db: Session = Depends(get_db),
                 current_user = Depends(require_role("admin", "doctor"))):
    cons = get_consultation_by_id(db, consult_id)
    if not cons:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return cons

# Update (doctor/admin)
@router.put("/{consult_id}", response_model=ConsultationOut)
def update_consult(consult_id: str, payload: ConsultationUpdate,
                   db: Session = Depends(get_db),
                   current_user = Depends(require_role("admin", "doctor"))):
    cons = get_consultation_by_id(db, consult_id)
    if not cons:
        raise HTTPException(status_code=404, detail="Consultation not found")

    return update_consultation(db, cons, payload)

# Delete consultation
@router.delete("/{consult_id}")
def remove_consult(consult_id: str, 
                   db: Session = Depends(get_db),
                   current_user = Depends(require_role("admin"))):
    cons = get_consultation_by_id(db, consult_id)
    if not cons:
        raise HTTPException(status_code=404, detail="Consultation not found")

    delete_consultation(db, cons)
    return {"deleted": True}
