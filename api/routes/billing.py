from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Billing

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


@router.get("/")
def get_billing(db: Session = Depends(get_db)):
    billing_records = db.query(Billing).all()

    return [
        {
            "billing_id": billing.billing_id,
            "appointment_id": billing.appointment_id,
            "billing_amount": float(billing.billing_amount)
            if billing.billing_amount is not None
            else None,
            "payment_type": billing.payment_type,
            "payment_status": billing.payment_status,
            "transaction_date": billing.transaction_date,
        }
        for billing in billing_records
    ]


@router.get("/{billing_id}")
def get_bill(
    billing_id: int,
    db: Session = Depends(get_db)
):
    billing = (
        db.query(Billing)
        .filter(Billing.billing_id == billing_id)
        .first()
    )

    if not billing:
        return {
            "message": "Billing record not found"
        }

    return {
        "billing_id": billing.billing_id,
        "appointment_id": billing.appointment_id,
        "billing_amount": float(billing.billing_amount)
        if billing.billing_amount is not None
        else None,
        "payment_type": billing.payment_type,
        "payment_status": billing.payment_status,
        "transaction_date": billing.transaction_date,
    }