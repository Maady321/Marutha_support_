from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.services.appointment_service import (
    list_appointments, get_appointment_by_id,
    create_appointment, update_appointment, delete_appointment
)
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[AppointmentOut])
def get_appointments(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return list_appointments(db)


@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def new_appointment(payload: AppointmentCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_appointment(db, payload, current_user.id)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def read_appointment(appointment_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")
    return appt


@router.put("/{appointment_id}", response_model=AppointmentOut)
def put_appointment(appointment_id: str, payload: AppointmentUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")
    return update_appointment(db, appt, payload.dict(exclude_unset=True))


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_appointment(appointment_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    appt = get_appointment_by_id(db, appointment_id)
    if not appt:
        raise HTTPException(404, "Appointment not found")
    delete_appointment(db, appt)
    return None
