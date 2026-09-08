import pandas as pd
import numpy as np


# --------------------------------------------------
# Clean Patients
# --------------------------------------------------
def clean_patients(df):

    df = df.copy()

    # Remove duplicate patients
    df = df.drop_duplicates(subset=["patient_id"])

    # Standardize text
    df["city"] = df["city"].str.strip().str.title()

    # Standardize email
    df["email"] = df["email"].str.strip().str.lower()

    # Convert date column
    df["date_of_birth"] = pd.to_datetime(
        df["date_of_birth"],
        errors="coerce"
    )

    return df


# --------------------------------------------------
# Clean Doctors
# --------------------------------------------------
def clean_doctors(df):

    df = df.copy()

    # Remove duplicate doctors
    df = df.drop_duplicates(subset=["doctor_id"])

    # Standardize text
    df["doctor_name"] = df["doctor_name"].str.strip()
    df["specialization"] = (
        df["specialization"]
        .str.strip()
        .str.title()
    )
    df["city"] = df["city"].str.strip().str.title()

    # Convert consultation fee to numeric
    df["consultation_fee"] = pd.to_numeric(
        df["consultation_fee"],
        errors="coerce"
    )

    return df


# --------------------------------------------------
# Clean Appointments
# --------------------------------------------------
def clean_appointments(df):

    df = df.copy()

    # Remove duplicate appointments
    df = df.drop_duplicates(subset=["appointment_id"])

    # Convert IDs to numeric
    df["patient_id"] = pd.to_numeric(
        df["patient_id"],
        errors="coerce"
    )

    df["doctor_id"] = pd.to_numeric(
        df["doctor_id"],
        errors="coerce"
    )

    # Convert appointment date
    df["appointment_date"] = pd.to_datetime(
        df["appointment_date"],
        errors="coerce"
    )

    # Standardize text
    df["appointment_type"] = (
        df["appointment_type"]
        .str.strip()
        .str.title()
    )

    df["status"] = (
        df["status"]
        .str.strip()
        .str.title()
    )

    return df


# --------------------------------------------------
# Clean Appointment Services
# --------------------------------------------------
def clean_appointment_services(df):

    df = df.copy()

    # Convert numeric columns
    df["appointment_id"] = pd.to_numeric(
        df["appointment_id"],
        errors="coerce"
    )

    df["doctor_id"] = pd.to_numeric(
        df["doctor_id"],
        errors="coerce"
    )

    df["duration_minutes"] = pd.to_numeric(
        df["duration_minutes"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    # Standardize service name
    df["service_name"] = (
        df["service_name"]
        .str.strip()
        .str.title()
    )

    return df


# --------------------------------------------------
# Clean Billing
# --------------------------------------------------
def clean_billing(df):

    df = df.copy()

    # Convert numeric columns
    df["appointment_id"] = pd.to_numeric(
        df["appointment_id"],
        errors="coerce"
    )

    df["billing_amount"] = pd.to_numeric(
        df["billing_amount"],
        errors="coerce"
    )

    # Standardize payment type
    df["payment_type"] = (
        df["payment_type"]
        .str.strip()
        .str.title()
    )

    # Standardize payment status
    df["payment_status"] = (
        df["payment_status"]
        .str.strip()
        .str.title()
    )

    # Convert transaction date
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    return df


# --------------------------------------------------
# Clean All Datasets
# --------------------------------------------------
def clean_all_data(data):

    cleaned_data = {}

    cleaned_data["patients"] = clean_patients(
        data["patients"]
    )

    cleaned_data["doctors"] = clean_doctors(
        data["doctors"]
    )

    cleaned_data["appointments"] = clean_appointments(
        data["appointments"]
    )

    cleaned_data["appointment_services"] = (
        clean_appointment_services(
            data["appointment_services"]
        )
    )

    cleaned_data["billing"] = clean_billing(
        data["billing"]
    )

    return cleaned_data


# --------------------------------------------------
# Test Cleaning
# --------------------------------------------------
if __name__ == "__main__":

    from ingestion import load_all_data

    print("\nLoading raw data...")
    raw_data = load_all_data()

    print("\nCleaning data...")
    cleaned_data = clean_all_data(raw_data)

    print("\nCleaning completed!\n")

    for name, df in cleaned_data.items():

        print(
            f"{name}: "
            f"{len(df)} records"
        )

        print(
            f"Missing values: "
            f"{df.isnull().sum().sum()}"
        )

        print("-" * 40)
        