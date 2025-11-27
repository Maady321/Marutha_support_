from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


def list_appointments(db: Session):
    return db.query(Appointment).all()


def get_appointment_by_id(db: Session, appointment_id: str):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def create_appointment(db: Session, data: AppointmentCreate, user_id: str):
    appt = Appointment(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        datetime_start=data.datetime_start,
        datetime_end=data.datetime_end,
        visit_type=data.visit_type,
        reason=data.reason,
        notes=data.notes,
        created_by=user_id
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


def update_appointment(db: Session, appointment, data: dict):
    for key, value in data.items():
        setattr(appointment, key, value)
    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment):
    db.delete(appointment)
    db.commit()
