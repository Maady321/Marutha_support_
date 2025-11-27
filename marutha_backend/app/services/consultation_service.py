import uuid
from sqlalchemy.orm import Session
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationUpdate

# --------------------------------------------------------------------------- #
# Create consultation
# --------------------------------------------------------------------------- #
def create_consultation(db: Session, patient_id: str, doctor_id: str,
                        scheduled_time, reason: str):
    cons = Consultation(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        doctor_id=doctor_id,
        scheduled_time=scheduled_time,
        reason=reason,
        status="scheduled"
    )
    db.add(cons)
    db.commit()
    db.refresh(cons)
    return cons

# --------------------------------------------------------------------------- #
# List all consultations
# --------------------------------------------------------------------------- #
def list_consultations(db: Session):
    return db.query(Consultation).all()

# --------------------------------------------------------------------------- #
# Get consultation by ID
# --------------------------------------------------------------------------- #
def get_consultation_by_id(db: Session, consult_id: str):
    return db.query(Consultation).filter(Consultation.id == consult_id).first()

# --------------------------------------------------------------------------- #
# Update consultation
# --------------------------------------------------------------------------- #
def update_consultation(db: Session, consultation: Consultation,
                        payload: ConsultationUpdate):
    data = payload.dict(exclude_unset=True)

    for key, value in data.items():
        setattr(consultation, key, value)

    db.commit()
    db.refresh(consultation)
    return consultation

# --------------------------------------------------------------------------- #
# Delete consultation
# --------------------------------------------------------------------------- #
def delete_consultation(db: Session, consultation: Consultation):
    db.delete(consultation)
    db.commit()
