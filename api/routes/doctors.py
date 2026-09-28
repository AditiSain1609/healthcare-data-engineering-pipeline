from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Doctor

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()

    return [
        {
            "doctor_id": doctor.doctor_id,
            "doctor_name": doctor.doctor_name,
            "specialization": doctor.specialization,
            "city": doctor.city,
            "consultation_fee": float(doctor.consultation_fee)
            if doctor.consultation_fee is not None
            else None,
        }
        for doctor in doctors
    ]


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = (
        db.query(Doctor)
        .filter(Doctor.doctor_id == doctor_id)
        .first()
    )

    if not doctor:
        return {
            "message": "Doctor not found"
        }

    return {
        "doctor_id": doctor.doctor_id,
        "doctor_name": doctor.doctor_name,
        "specialization": doctor.specialization,
        "city": doctor.city,
        "consultation_fee": float(doctor.consultation_fee)
        if doctor.consultation_fee is not None
        else None,
    }