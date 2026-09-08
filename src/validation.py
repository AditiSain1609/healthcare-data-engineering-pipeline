import pandas as pd
import os
import re

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_valid_email(email):
    if pd.isna(email):
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, str(email)))


def save_invalid_records(name, df):
    file_path = os.path.join(
        OUTPUT_DIR,
        f"invalid_{name}.csv"
    )

    df.to_csv(file_path, index=False)

    print(
        f"Saved {len(df)} invalid {name} records -> {file_path}"
    )


# --------------------------------------------------
# PATIENT VALIDATION
# --------------------------------------------------

def validate_patients(df):

    df = df.copy()

    valid = (
        df["patient_id"].notna()
        &
        ~df["patient_id"].duplicated(keep=False)
        &
        df["email"].apply(is_valid_email)
    )

    valid_df = df[valid].copy()
    invalid_df = df[~valid].copy()

    save_invalid_records("patients", invalid_df)

    return valid_df, invalid_df


# --------------------------------------------------
# DOCTOR VALIDATION
# --------------------------------------------------

def validate_doctors(df):

    df = df.copy()

    valid = (
        df["doctor_id"].notna()
        &
        ~df["doctor_id"].duplicated(keep=False)
        &
        df["consultation_fee"].notna()
        &
        (df["consultation_fee"] > 0)
    )

    valid_df = df[valid].copy()
    invalid_df = df[~valid].copy()

    save_invalid_records("doctors", invalid_df)

    return valid_df, invalid_df


# --------------------------------------------------
# APPOINTMENT VALIDATION
# --------------------------------------------------

def validate_appointments(
    df,
    valid_patient_ids,
    valid_doctor_ids
):

    df = df.copy()

    valid = (
        df["appointment_id"].notna()
        &
        ~df["appointment_id"].duplicated(keep=False)
        &
        df["patient_id"].isin(valid_patient_ids)
        &
        df["doctor_id"].isin(valid_doctor_ids)
        &
        df["appointment_date"].notna()
    )

    valid_df = df[valid].copy()
    invalid_df = df[~valid].copy()

    save_invalid_records("appointments", invalid_df)

    return valid_df, invalid_df


# --------------------------------------------------
# APPOINTMENT SERVICES VALIDATION
# --------------------------------------------------

def validate_appointment_services(
    df,
    valid_appointment_ids,
    valid_doctor_ids
):

    df = df.copy()

    valid = (
        df["appointment_id"].isin(valid_appointment_ids)
        &
        df["doctor_id"].isin(valid_doctor_ids)
        &
        df["duration_minutes"].notna()
        &
        (df["duration_minutes"] > 0)
        &
        df["quantity"].notna()
        &
        (df["quantity"] > 0)
    )

    valid_df = df[valid].copy()
    invalid_df = df[~valid].copy()

    save_invalid_records(
        "appointment_services",
        invalid_df
    )

    return valid_df, invalid_df


# --------------------------------------------------
# BILLING VALIDATION
# --------------------------------------------------

def validate_billing(
    df,
    valid_appointment_ids
):

    df = df.copy()

    accepted_statuses = {
        "Successful",
        "Failed",
        "Pending"
    }

    valid = (
        df["billing_id"].notna()
        &
        ~df["billing_id"].duplicated(keep=False)
        &
        df["appointment_id"].isin(valid_appointment_ids)
        &
        df["billing_amount"].notna()
        &
        (df["billing_amount"] > 0)
        &
        df["payment_status"].isin(accepted_statuses)
    )

    valid_df = df[valid].copy()
    invalid_df = df[~valid].copy()

    save_invalid_records(
        "billing",
        invalid_df
    )

    return valid_df, invalid_df


# --------------------------------------------------
# COMPLETE VALIDATION
# --------------------------------------------------

def validate_all_data(data):

    results = {}

    # Patients
    valid_patients, _ = validate_patients(
        data["patients"]
    )

    results["patients"] = valid_patients

    # Doctors
    valid_doctors, _ = validate_doctors(
        data["doctors"]
    )

    results["doctors"] = valid_doctors

    # Appointments
    valid_appointments, _ = validate_appointments(
        data["appointments"],
        valid_patients["patient_id"],
        valid_doctors["doctor_id"]
    )

    results["appointments"] = valid_appointments

    # Services
    valid_services, _ = validate_appointment_services(
        data["appointment_services"],
        valid_appointments["appointment_id"],
        valid_doctors["doctor_id"]
    )

    results["appointment_services"] = valid_services

    # Billing
    valid_billing, _ = validate_billing(
        data["billing"],
        valid_appointments["appointment_id"]
    )

    results["billing"] = valid_billing

    return results


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    from ingestion import load_all_data
    from cleaning import clean_all_data

    print("\nLoading raw data...")

    raw_data = load_all_data()

    print("Cleaning data...")

    cleaned_data = clean_all_data(raw_data)

    print("Validating data...\n")

    valid_data = validate_all_data(
        cleaned_data
    )

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    for name, df in valid_data.items():
        print(
            f"{name}: {len(df)} valid records"
        )

    print("=" * 60)