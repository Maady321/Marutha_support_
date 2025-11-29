# app/routers/doctors.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.doctor import Doctor
from app.core.roles import require_role
from app.core.deps import get_db, get_current_user

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorOut,
    AvailabilityUpdate
)

from app.services.doctor_service import (
    create_doctor,
    list_doctors,
    get_doctor_by_id,
    update_doctor,
    delete_doctor,
    update_availability
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])
@router.post("/", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_new_doctor(
    payload: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    # check if user_id already assigned to any doctor
    from uuid import UUID
    try:
        user_uuid = UUID(payload.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
        
    existing = db.query(Doctor).filter_by(user_id=user_uuid).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists for this user")

    data = payload.dict()
    return create_doctor(db, data)


# ---------------------------
# LIST ALL DOCTORS
# ---------------------------
@router.get("/", response_model=List[DoctorOut])
def get_doctors(
    skip: int = 0,
    limit: int = 50,
    available: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return list_doctors(db, skip=skip, limit=limit, available=available)


# ---------------------------
# GET DOCTOR BY ID
# ---------------------------
@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ---------------------------
# UPDATE DOCTOR DETAILS (ADMIN)
# ---------------------------
@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor_route(
    doctor_id: str,
    payload: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    data = payload.dict(exclude_unset=True)
    return update_doctor(db, doctor, data)


# ---------------------------
# DELETE DOCTOR (ADMIN ONLY)
# ---------------------------
@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    delete_doctor(db, doctor)
    return None


# ---------------------------
# UPDATE DOCTOR AVAILABILITY
# ---------------------------
@router.patch("/{doctor_id}/availability", response_model=DoctorOut)
def update_doctor_availability(
    doctor_id: str,
    payload: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return update_availability(db, doctor, payload.available)
