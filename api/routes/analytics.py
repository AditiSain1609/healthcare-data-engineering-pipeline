from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Appointment, Billing, Doctor, Patient

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_patients = db.query(func.count(Patient.patient_id)).scalar()
    total_doctors = db.query(func.count(Doctor.doctor_id)).scalar()
    total_appointments = db.query(
        func.count(Appointment.appointment_id)
    ).scalar()

    total_revenue = db.query(
        func.coalesce(func.sum(Billing.billing_amount), 0)
    ).scalar()

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "total_revenue": float(total_revenue),
    }


@router.get("/top-patients")
def get_top_patients(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Patient.patient_id,
            Patient.first_name,
            Patient.last_name,
            func.sum(Billing.billing_amount).label("total_billing")
        )
        .join(
            Appointment,
            Patient.patient_id == Appointment.patient_id
        )
        .join(
            Billing,
            Appointment.appointment_id == Billing.appointment_id
        )
        .group_by(
            Patient.patient_id,
            Patient.first_name,
            Patient.last_name
        )
        .order_by(
            func.sum(Billing.billing_amount).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "patient_id": row.patient_id,
            "patient_name": f"{row.first_name} {row.last_name}",
            "total_billing": float(row.total_billing),
        }
        for row in results
    ]


@router.get("/top-doctors")
def get_top_doctors(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Doctor.doctor_id,
            Doctor.doctor_name,
            func.sum(Billing.billing_amount).label("total_revenue")
        )
        .join(
            Appointment,
            Doctor.doctor_id == Appointment.doctor_id
        )
        .join(
            Billing,
            Appointment.appointment_id == Billing.appointment_id
        )
        .group_by(
            Doctor.doctor_id,
            Doctor.doctor_name
        )
        .order_by(
            func.sum(Billing.billing_amount).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "doctor_id": row.doctor_id,
            "doctor_name": row.doctor_name,
            "total_revenue": float(row.total_revenue),
        }
        for row in results
    ]


@router.get("/revenue-by-city")
def get_revenue_by_city(db: Session = Depends(get_db)):
    results = (
        db.query(
            Doctor.city,
            func.sum(Billing.billing_amount).label("total_revenue")
        )
        .join(
            Appointment,
            Doctor.doctor_id == Appointment.doctor_id
        )
        .join(
            Billing,
            Appointment.appointment_id == Billing.appointment_id
        )
        .group_by(Doctor.city)
        .order_by(
            func.sum(Billing.billing_amount).desc()
        )
        .all()
    )

    return [
        {
            "city": row.city,
            "total_revenue": float(row.total_revenue),
        }
        for row in results
    ]


@router.get("/cancellation-rate")
def get_cancellation_rate(db: Session = Depends(get_db)):
    total_appointments = db.query(
        func.count(Appointment.appointment_id)
    ).scalar()

    cancelled_appointments = db.query(
        func.count(Appointment.appointment_id)
    ).filter(
        func.lower(Appointment.status) == "cancelled"
    ).scalar()

    if total_appointments == 0:
        rate = 0
    else:
        rate = (cancelled_appointments / total_appointments) * 100

    return {
        "total_appointments": total_appointments,
        "cancelled_appointments": cancelled_appointments,
        "cancellation_rate_percentage": round(rate, 2),
    }