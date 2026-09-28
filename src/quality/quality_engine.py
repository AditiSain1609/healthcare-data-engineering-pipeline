import pandas as pd

from src.quality.quality_rules import (
    check_patient_id_not_null,
    check_patient_id_unique,
    check_patient_email,
    check_doctor_id_unique,
    check_consultation_fee,
    check_appointment_id_unique,
    check_appointment_date,
    check_patient_exists,
    check_doctor_exists,
    check_service_appointment_exists,
    check_service_doctor_exists,
    check_duration_positive,
    check_quantity_positive,
    check_billing_id_unique,
    check_billing_appointment_exists,
    check_billing_amount,
    check_payment_status
)


def run_rule(table_name, rule_name, result):
    """
    Convert a boolean validation result into
    a standard quality report record.
    """

    total_records = len(result)
    passed_records = int(result.sum())
    failed_records = total_records - passed_records

    pass_percentage = (
        round((passed_records / total_records) * 100, 2)
        if total_records > 0
        else 0
    )

    return {
        "table_name": table_name,
        "rule_name": rule_name,
        "total_records": total_records,
        "passed_records": passed_records,
        "failed_records": failed_records,
        "pass_percentage": pass_percentage
    }


def run_patient_quality_checks(df):
    results = []

    results.append(
        run_rule(
            "patients",
            "patient_id_not_null",
            check_patient_id_not_null(df)
        )
    )

    results.append(
        run_rule(
            "patients",
            "patient_id_unique",
            check_patient_id_unique(df)
        )
    )

    results.append(
        run_rule(
            "patients",
            "valid_email",
            check_patient_email(df)
        )
    )

    return results


def run_doctor_quality_checks(df):
    results = []

    results.append(
        run_rule(
            "doctors",
            "doctor_id_unique",
            check_doctor_id_unique(df)
        )
    )

    results.append(
        run_rule(
            "doctors",
            "consultation_fee_positive",
            check_consultation_fee(df)
        )
    )

    return results


def run_appointment_quality_checks(
    df,
    valid_patient_ids,
    valid_doctor_ids
):
    results = []

    results.append(
        run_rule(
            "appointments",
            "appointment_id_unique",
            check_appointment_id_unique(df)
        )
    )

    results.append(
        run_rule(
            "appointments",
            "appointment_date_valid",
            check_appointment_date(df)
        )
    )

    results.append(
        run_rule(
            "appointments",
            "patient_reference_valid",
            check_patient_exists(
                df,
                valid_patient_ids
            )
        )
    )

    results.append(
        run_rule(
            "appointments",
            "doctor_reference_valid",
            check_doctor_exists(
                df,
                valid_doctor_ids
            )
        )
    )

    return results


def run_service_quality_checks(
    df,
    valid_appointment_ids,
    valid_doctor_ids
):
    results = []

    results.append(
        run_rule(
            "appointment_services",
            "appointment_reference_valid",
            check_service_appointment_exists(
                df,
                valid_appointment_ids
            )
        )
    )

    results.append(
        run_rule(
            "appointment_services",
            "doctor_reference_valid",
            check_service_doctor_exists(
                df,
                valid_doctor_ids
            )
        )
    )

    results.append(
        run_rule(
            "appointment_services",
            "duration_positive",
            check_duration_positive(df)
        )
    )

    results.append(
        run_rule(
            "appointment_services",
            "quantity_positive",
            check_quantity_positive(df)
        )
    )

    return results


def run_billing_quality_checks(
    df,
    valid_appointment_ids
):
    results = []

    results.append(
        run_rule(
            "billing",
            "billing_id_unique",
            check_billing_id_unique(df)
        )
    )

    results.append(
        run_rule(
            "billing",
            "appointment_reference_valid",
            check_billing_appointment_exists(
                df,
                valid_appointment_ids
            )
        )
    )

    results.append(
        run_rule(
            "billing",
            "billing_amount_positive",
            check_billing_amount(df)
        )
    )

    results.append(
        run_rule(
            "billing",
            "payment_status_valid",
            check_payment_status(df)
        )
    )

    return results


def run_data_quality_engine(data):
    """
    Execute all healthcare data quality rules.

    Returns:
        pandas.DataFrame containing rule-level
        quality results.
    """

    patients = data["patients"]
    doctors = data["doctors"]
    appointments = data["appointments"]
    services = data["appointment_services"]
    billing = data["billing"]

    all_results = []

    # Patients
    all_results.extend(
        run_patient_quality_checks(patients)
    )

    # Doctors
    all_results.extend(
        run_doctor_quality_checks(doctors)
    )

    # Reference IDs
    valid_patient_ids = patients["patient_id"].dropna()
    valid_doctor_ids = doctors["doctor_id"].dropna()
    valid_appointment_ids = appointments["appointment_id"].dropna()

    # Appointments
    all_results.extend(
        run_appointment_quality_checks(
            appointments,
            valid_patient_ids,
            valid_doctor_ids
        )
    )

    # Appointment services
    all_results.extend(
        run_service_quality_checks(
            services,
            valid_appointment_ids,
            valid_doctor_ids
        )
    )

    # Billing
    all_results.extend(
        run_billing_quality_checks(
            billing,
            valid_appointment_ids
        )
    )

    return pd.DataFrame(all_results)


if __name__ == "__main__":
    from src.ingestion import load_all_data
    from src.cleaning import clean_all_data

    print("\nLoading healthcare data...")
    raw_data = load_all_data()

    print("Cleaning healthcare data...")
    cleaned_data = clean_all_data(raw_data)

    print("\nRunning Data Quality Engine...")

    quality_report = run_data_quality_engine(
        cleaned_data
    )

    print("\n" + "=" * 80)
    print("DATA QUALITY ENGINE REPORT")
    print("=" * 80)

    print(
        quality_report.to_string(index=False)
    )

    print("=" * 80)

    print(
        "\nData Quality Engine executed successfully!"
    )