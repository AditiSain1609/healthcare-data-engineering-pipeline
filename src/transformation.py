import pandas as pd
import os

from src.ingestion import load_all_data
from src.cleaning import clean_all_data
from src.validation import validate_all_data

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# PATIENT METRICS
# =========================================================

def create_patient_metrics(data):
    patients = data["patients"]
    appointments = data["appointments"]
    billing = data["billing"]

    appointment_count = (
        appointments
        .groupby("patient_id")
        .size()
        .reset_index(name="total_appointments")
    )

    billing_metrics = (
        billing
        .groupby("appointment_id")["billing_amount"]
        .sum()
        .reset_index()
    )

    appointment_billing = appointments.merge(
        billing_metrics,
        on="appointment_id",
        how="left"
    )

    patient_billing = (
        appointment_billing
        .groupby("patient_id")["billing_amount"]
        .sum()
        .reset_index(name="total_billing")
    )

    avg_billing = (
        appointment_billing
        .groupby("patient_id")["billing_amount"]
        .mean()
        .reset_index(name="avg_appointment_value")
    )

    last_appointment = (
        appointments
        .groupby("patient_id")["appointment_date"]
        .max()
        .reset_index(name="last_appointment")
    )

    result = patients.merge(
        appointment_count,
        on="patient_id",
        how="left"
    )

    result = result.merge(
        patient_billing,
        on="patient_id",
        how="left"
    )

    result = result.merge(
        avg_billing,
        on="patient_id",
        how="left"
    )

    result = result.merge(
        last_appointment,
        on="patient_id",
        how="left"
    )

    result["total_appointments"] = (
        result["total_appointments"].fillna(0).astype(int)
    )

    result["total_billing"] = result["total_billing"].fillna(0)

    result["avg_appointment_value"] = (
        result["avg_appointment_value"].fillna(0)
    )

    return result


# =========================================================
# DOCTOR METRICS
# =========================================================

def create_doctor_metrics(data):
    doctors = data["doctors"]
    appointments = data["appointments"]
    services = data["appointment_services"]
    billing = data["billing"]

    service_count = (
        services
        .groupby("doctor_id")
        .size()
        .reset_index(name="total_services")
    )

    doctor_appointments = (
        appointments
        .groupby("doctor_id")
        .size()
        .reset_index(name="total_appointments")
    )

    doctor_revenue = (
        services
        .merge(
            billing[["appointment_id", "billing_amount"]],
            on="appointment_id",
            how="left"
        )
        .groupby("doctor_id")["billing_amount"]
        .sum()
        .reset_index(name="total_revenue")
    )

    result = doctors.merge(
        service_count,
        on="doctor_id",
        how="left"
    )

    result = result.merge(
        doctor_appointments,
        on="doctor_id",
        how="left"
    )

    result = result.merge(
        doctor_revenue,
        on="doctor_id",
        how="left"
    )

    result["total_services"] = (
        result["total_services"].fillna(0).astype(int)
    )

    result["total_appointments"] = (
        result["total_appointments"].fillna(0).astype(int)
    )

    result["total_revenue"] = (
        result["total_revenue"].fillna(0)
    )

    result["consultation_fee"] = (
        pd.to_numeric(
            result["consultation_fee"],
            errors="coerce"
        )
    )

    return result


# =========================================================
# BUSINESS METRICS
# =========================================================

def create_business_metrics(data):
    appointments = data["appointments"]
    billing = data["billing"]

    appointment_billing = appointments.merge(
        billing[["appointment_id", "billing_amount"]],
        on="appointment_id",
        how="left"
    )

    # Daily revenue
    daily_revenue = (
        appointment_billing
        .groupby(
            appointment_billing["appointment_date"].dt.date
        )["billing_amount"]
        .sum()
        .reset_index(name="daily_revenue")
    )

    daily_revenue.rename(
        columns={"appointment_date": "date"},
        inplace=True
    )

    # Monthly revenue
    appointment_billing["month"] = (
        appointment_billing["appointment_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_revenue = (
        appointment_billing
        .groupby("month")["billing_amount"]
        .sum()
        .reset_index(name="monthly_revenue")
    )

    # Average appointment value
    average_appointment_value = (
        appointment_billing["billing_amount"]
        .mean()
    )

    # Cancellation percentage
    total_appointments = len(appointments)

    cancelled_appointments = (
        appointments["status"] == "Cancelled"
    ).sum()

    cancellation_percentage = (
        cancelled_appointments / total_appointments * 100
        if total_appointments > 0
        else 0
    )

    return {
        "daily_revenue": daily_revenue,
        "monthly_revenue": monthly_revenue,
        "average_appointment_value": average_appointment_value,
        "cancellation_percentage": cancellation_percentage
    }


# =========================================================
# MAIN TRANSFORMATION PIPELINE
# =========================================================

def transform_all_data(data):

    patient_metrics = create_patient_metrics(data)

    doctor_metrics = create_doctor_metrics(data)

    business_metrics = create_business_metrics(data)

    return {
        "patient_metrics": patient_metrics,
        "doctor_metrics": doctor_metrics,
        "business_metrics": business_metrics
    }


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("\nLoading raw data...")
    raw_data = load_all_data()

    print("Cleaning data...")
    cleaned_data = clean_all_data(raw_data)

    print("Validating data...")
    valid_data = validate_all_data(cleaned_data)

    print("\nTransforming data...")

    transformed_data = transform_all_data(valid_data)

    patient_metrics = transformed_data["patient_metrics"]
    doctor_metrics = transformed_data["doctor_metrics"]
    business_metrics = transformed_data["business_metrics"]

    # Save outputs

    patient_metrics.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "patient_metrics.csv"
        ),
        index=False
    )

    doctor_metrics.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "doctor_metrics.csv"
        ),
        index=False
    )

    business_metrics["daily_revenue"].to_csv(
        os.path.join(
            OUTPUT_DIR,
            "daily_revenue.csv"
        ),
        index=False
    )

    business_metrics["monthly_revenue"].to_csv(
        os.path.join(
            OUTPUT_DIR,
            "monthly_revenue.csv"
        ),
        index=False
    )

    print("\n" + "=" * 50)
    print("TRANSFORMATION SUMMARY")
    print("=" * 50)

    print(
        f"Patient metrics: "
        f"{len(patient_metrics)} records"
    )

    print(
        f"Doctor metrics: "
        f"{len(doctor_metrics)} records"
    )

    print(
        f"Average appointment value: "
        f"{business_metrics['average_appointment_value']:.2f}"
    )

    print(
        f"Cancellation percentage: "
        f"{business_metrics['cancellation_percentage']:.2f}%"
    )

    print("=" * 50)

    print("\nTransformation completed successfully!")