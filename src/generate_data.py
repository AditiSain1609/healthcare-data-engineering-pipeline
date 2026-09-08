import pandas as pd
import numpy as np
import random
import json
import os
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Helper Functions
# -----------------------------
def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def random_name():
    first_names = [
        "Aarav", "Vivaan", "Aditya", "Arjun", "Rahul",
        "Rohan", "Ananya", "Priya", "Sneha", "Neha",
        "Kavya", "Isha", "Pooja", "Simran", "Aditi"
    ]

    last_names = [
        "Sharma", "Verma", "Patel", "Reddy", "Kumar",
        "Singh", "Gupta", "Mehta", "Joshi", "Agarwal"
    ]

    return random.choice(first_names), random.choice(last_names)


# -----------------------------
# 1. Generate Patients
# -----------------------------
def generate_patients(n=500):

    cities = [
        "Hyderabad",
        "Bangalore",
        "Mumbai",
        "Delhi",
        "Chennai",
        "Pune"
    ]

    patients = []

    for patient_id in range(1, n + 1):

        first, last = random_name()

        patients.append({
            "patient_id": patient_id,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{patient_id}@email.com",
            "phone": f"9{random.randint(100000000, 999999999)}",
            "city": random.choice(cities),
            "date_of_birth": random_date(
                datetime(1950, 1, 1),
                datetime(2005, 12, 31)
            ).strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(patients)

    # Intentional missing value
    df.loc[10, "email"] = None

    # Intentional inconsistent city
    df.loc[20, "city"] = "hyderabad"
    df.loc[21, "city"] = "HYDERABAD"

    # Intentional duplicate
    df = pd.concat([df, df.iloc[[50]]], ignore_index=True)

    return df


# -----------------------------
# 2. Generate Doctors
# -----------------------------
def generate_doctors(n=100):

    specialties = [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Dermatology",
        "Pediatrics",
        "General Medicine",
        "ENT"
    ]

    doctors = []

    for doctor_id in range(1, n + 1):

        first, last = random_name()

        doctors.append({
            "doctor_id": doctor_id,
            "doctor_name": f"Dr. {first} {last}",
            "specialization": random.choice(specialties),
            "city": random.choice([
                "Hyderabad",
                "Bangalore",
                "Mumbai",
                "Delhi",
                "Chennai",
                "Pune"
            ]),
            "consultation_fee": random.choice(
                [500, 700, 800, 1000, 1200, 1500, 2000]
            )
        })

    df = pd.DataFrame(doctors)

    # Missing consultation fee
    df.loc[5, "consultation_fee"] = None

    # Negative fee
    df.loc[10, "consultation_fee"] = -500

    # Duplicate doctor
    df = pd.concat([df, df.iloc[[30]]], ignore_index=True)

    return df


# -----------------------------
# 3. Generate Appointments
# -----------------------------
def generate_appointments(n=2000, patient_count=500):

    appointment_types = [
        "Consultation",
        "Follow-up",
        "Emergency"
    ]

    statuses = [
        "Completed",
        "Cancelled",
        "Scheduled"
    ]

    appointments = []

    for appointment_id in range(1, n + 1):

        appointments.append({
            "appointment_id": appointment_id,
            "patient_id": random.randint(1, patient_count),
            "doctor_id": random.randint(1, 100),
            "appointment_date": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 8, 31)
            ).strftime("%Y-%m-%d"),
            "appointment_type": random.choice(appointment_types),
            "status": random.choice(statuses)
        })

    df = pd.DataFrame(appointments)

    # Missing appointment date
    df.loc[15, "appointment_date"] = None

    # Invalid patient ID
    df.loc[25, "patient_id"] = 9999

    # Invalid doctor ID
    df.loc[35, "doctor_id"] = 9999

    # Inconsistent appointment type
    df.loc[40, "appointment_type"] = " consultation "

    # Duplicate appointment
    df = pd.concat([df, df.iloc[[100]]], ignore_index=True)

    return df


# -----------------------------
# 4. Generate Appointment Services
# -----------------------------
def generate_appointment_services(n=4000, appointment_count=2000):

    services = [
        "Consultation",
        "Blood Test",
        "X-Ray",
        "MRI",
        "CT Scan",
        "ECG",
        "Physiotherapy",
        "Health Checkup"
    ]

    records = []

    for service_id in range(1, n + 1):

        records.append({
            "service_id": service_id,
            "appointment_id": random.randint(1, appointment_count),
            "doctor_id": random.randint(1, 100),
            "service_name": random.choice(services),
            "duration_minutes": random.choice(
                [15, 20, 30, 45, 60, 90]
            ),
            "quantity": random.randint(1, 3)
        })

    df = pd.DataFrame(records)

    # Negative duration
    df.loc[10, "duration_minutes"] = -30

    # Negative quantity
    df.loc[20, "quantity"] = -1

    # Invalid appointment ID
    df.loc[30, "appointment_id"] = 9999

    # Invalid doctor ID
    df.loc[40, "doctor_id"] = 9999

    return df


# -----------------------------
# 5. Generate Billing JSON
# -----------------------------
def generate_billing(n=2000, appointment_count=2000):

    payment_types = [
        "Cash",
        "Card",
        "Insurance",
        "UPI"
    ]

    payment_statuses = [
        "Successful",
        "Failed",
        "Pending"
    ]

    billing = []

    for billing_id in range(1, n + 1):

        billing.append({
            "billing_id": billing_id,
            "appointment_id": random.randint(1, appointment_count),
            "billing_amount": random.choice(
                [500, 700, 1000, 1500, 2000, 2500, 3000]
            ),
            "payment_type": random.choice(payment_types),
            "payment_status": random.choice(payment_statuses),
            "transaction_date": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 8, 31)
            ).strftime("%Y-%m-%d")
        })

    # Invalid payment status
    billing[10]["payment_status"] = "UNKNOWN"

    # Negative billing amount
    billing[20]["billing_amount"] = -1000

    # Inconsistent payment type
    billing[30]["payment_type"] = " insurance "

    # Invalid appointment ID
    billing[40]["appointment_id"] = 9999

    return billing


# -----------------------------
# Main Function
# -----------------------------
def main():

    print("Starting healthcare dataset generation...\n")

    # Generate datasets
    patients = generate_patients()
    doctors = generate_doctors()
    appointments = generate_appointments()
    appointment_services = generate_appointment_services()
    billing = generate_billing()

    # Save CSV files
    patients.to_csv(
        os.path.join(OUTPUT_DIR, "patients.csv"),
        index=False
    )

    doctors.to_csv(
        os.path.join(OUTPUT_DIR, "doctors.csv"),
        index=False
    )

    appointments.to_csv(
        os.path.join(OUTPUT_DIR, "appointments.csv"),
        index=False
    )

    appointment_services.to_csv(
        os.path.join(OUTPUT_DIR, "appointment_services.csv"),
        index=False
    )

    # Save billing JSON
    with open(
        os.path.join(OUTPUT_DIR, "billing.json"),
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            billing,
            file,
            indent=4
        )

    # Print summary
    print("Dataset generation completed!\n")

    print(f"Patients: {len(patients)} records")
    print(f"Doctors: {len(doctors)} records")
    print(f"Appointments: {len(appointments)} records")
    print(
        f"Appointment Services: "
        f"{len(appointment_services)} records"
    )
    print(f"Billing: {len(billing)} records")

    print("\nFiles created inside data/ folder.")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()