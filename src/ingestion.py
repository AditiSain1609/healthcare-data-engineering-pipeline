import pandas as pd
import json
import os


DATA_DIR = "data"


def load_patients():
    return pd.read_csv(
        os.path.join(DATA_DIR, "patients.csv")
    )


def load_doctors():
    return pd.read_csv(
        os.path.join(DATA_DIR, "doctors.csv")
    )


def load_appointments():
    return pd.read_csv(
        os.path.join(DATA_DIR, "appointments.csv")
    )


def load_appointment_services():
    return pd.read_csv(
        os.path.join(DATA_DIR, "appointment_services.csv")
    )


def load_billing():
    with open(
        os.path.join(DATA_DIR, "billing.json"),
        "r",
        encoding="utf-8"
    ) as file:
        return pd.DataFrame(json.load(file))


def load_all_data():

    patients = load_patients()
    doctors = load_doctors()
    appointments = load_appointments()
    appointment_services = load_appointment_services()
    billing = load_billing()

    return {
        "patients": patients,
        "doctors": doctors,
        "appointments": appointments,
        "appointment_services": appointment_services,
        "billing": billing
    }


if __name__ == "__main__":

    data = load_all_data()

    print("\nData Ingestion Successful!\n")

    for name, df in data.items():
        print(f"{name}: {len(df)} records")