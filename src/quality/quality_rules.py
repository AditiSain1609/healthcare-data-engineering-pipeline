import pandas as pd


# ============================================================
# PATIENT QUALITY RULES
# ============================================================

def check_patient_id_not_null(df):
    return df["patient_id"].notna()


def check_patient_id_unique(df):
    return ~df["patient_id"].duplicated(keep=False)


def check_patient_email(df):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return df["email"].notna() & df["email"].astype(str).str.match(
        pattern, na=False
    )


# ============================================================
# DOCTOR QUALITY RULES
# ============================================================

def check_doctor_id_unique(df):
    return ~df["doctor_id"].duplicated(keep=False)


def check_consultation_fee(df):
    return df["consultation_fee"].notna() & (
        df["consultation_fee"] > 0
    )


# ============================================================
# APPOINTMENT QUALITY RULES
# ============================================================

def check_appointment_id_unique(df):
    return ~df["appointment_id"].duplicated(keep=False)


def check_appointment_date(df):
    return df["appointment_date"].notna()


def check_patient_exists(df, valid_patient_ids):
    return df["patient_id"].isin(valid_patient_ids)


def check_doctor_exists(df, valid_doctor_ids):
    return df["doctor_id"].isin(valid_doctor_ids)


# ============================================================
# APPOINTMENT SERVICE QUALITY RULES
# ============================================================

def check_service_appointment_exists(df, valid_appointment_ids):
    return df["appointment_id"].isin(valid_appointment_ids)


def check_service_doctor_exists(df, valid_doctor_ids):
    return df["doctor_id"].isin(valid_doctor_ids)


def check_duration_positive(df):
    return df["duration_minutes"].notna() & (
        df["duration_minutes"] > 0
    )


def check_quantity_positive(df):
    return df["quantity"].notna() & (
        df["quantity"] > 0
    )


# ============================================================
# BILLING QUALITY RULES
# ============================================================

def check_billing_id_unique(df):
    return ~df["billing_id"].duplicated(keep=False)


def check_billing_appointment_exists(df, valid_appointment_ids):
    return df["appointment_id"].isin(valid_appointment_ids)


def check_billing_amount(df):
    return df["billing_amount"].notna() & (
        df["billing_amount"] > 0
    )


def check_payment_status(df):
    accepted_statuses = {
        "Successful",
        "Failed",
        "Pending"
    }

    return df["payment_status"].isin(accepted_statuses)