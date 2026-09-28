from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Appointment

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()

    return [
        {
            "appointment_id": appointment.appointment_id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "appointment_date": appointment.appointment_date,
            "appointment_type": appointment.appointment_type,
            "status": appointment.status,
        }
        for appointment in appointments
    ]


@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.appointment_id == appointment_id)
        .first()
    )

    if not appointment:
        return {
            "message": "Appointment not found"
        }

    return {
        "appointment_id": appointment.appointment_id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date,
        "appointment_type": appointment.appointment_type,
        "status": appointment.status,
    }