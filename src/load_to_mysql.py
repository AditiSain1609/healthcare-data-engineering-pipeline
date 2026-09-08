import mysql.connector
import pandas as pd


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "healthcare_db"
}


# --------------------------------------------------
# VALUE CONVERTER
# --------------------------------------------------

def convert_value(value):

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    return value


# --------------------------------------------------
# RESET TABLES
# --------------------------------------------------

def reset_tables(cursor):
    print("\nResetting MySQL tables...")

    try:
        # Foreign key checks temporarily disable
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        tables = [
            "billing",
            "appointment_services",
            "appointments",
            "doctors",
            "patients"
        ]

        for table in tables:

            print(f"Clearing table: {table}...")

            cursor.execute(
                f"DELETE FROM {table}"
            )

            print(
                f"Cleared table: {table}"
            )

        # Foreign key checks enable again
        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )

        print(
            "All tables cleared successfully!"
        )

    except Exception as error:

        # Always restore FK checks
        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )

        raise error

# --------------------------------------------------
# LOAD PATIENTS
# --------------------------------------------------

def load_patients(cursor, df):

    query = """
        INSERT INTO patients
        (
            patient_id,
            first_name,
            last_name,
            email,
            phone,
            city,
            date_of_birth
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                convert_value(row["patient_id"]),
                convert_value(row["first_name"]),
                convert_value(row["last_name"]),
                convert_value(row["email"]),
                convert_value(row["phone"]),
                convert_value(row["city"]),
                convert_value(row["date_of_birth"])
            )
        )

    cursor.executemany(query, records)

    print(
        f"Patients loaded: {len(records)}"
    )


# --------------------------------------------------
# LOAD DOCTORS
# --------------------------------------------------

def load_doctors(cursor, df):

    query = """
        INSERT INTO doctors
        (
            doctor_id,
            doctor_name,
            specialization,
            city,
            consultation_fee
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                convert_value(row["doctor_id"]),
                convert_value(row["doctor_name"]),
                convert_value(row["specialization"]),
                convert_value(row["city"]),
                convert_value(row["consultation_fee"])
            )
        )

    cursor.executemany(query, records)

    print(
        f"Doctors loaded: {len(records)}"
    )


# --------------------------------------------------
# LOAD APPOINTMENTS
# --------------------------------------------------

def load_appointments(cursor, df):

    query = """
        INSERT INTO appointments
        (
            appointment_id,
            patient_id,
            doctor_id,
            appointment_date,
            appointment_type,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                convert_value(row["appointment_id"]),
                convert_value(row["patient_id"]),
                convert_value(row["doctor_id"]),
                convert_value(row["appointment_date"]),
                convert_value(row["appointment_type"]),
                convert_value(row["status"])
            )
        )

    cursor.executemany(query, records)

    print(
        f"Appointments loaded: {len(records)}"
    )


# --------------------------------------------------
# LOAD SERVICES
# --------------------------------------------------

def load_appointment_services(cursor, df):

    query = """
        INSERT INTO appointment_services
        (
            service_id,
            appointment_id,
            doctor_id,
            service_name,
            duration_minutes,
            quantity
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                convert_value(row["service_id"]),
                convert_value(row["appointment_id"]),
                convert_value(row["doctor_id"]),
                convert_value(row["service_name"]),
                convert_value(row["duration_minutes"]),
                convert_value(row["quantity"])
            )
        )

    cursor.executemany(query, records)

    print(
        f"Appointment services loaded: {len(records)}"
    )


# --------------------------------------------------
# LOAD BILLING
# --------------------------------------------------

def load_billing(cursor, df):

    query = """
        INSERT INTO billing
        (
            billing_id,
            appointment_id,
            billing_amount,
            payment_type,
            payment_status,
            transaction_date
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                convert_value(row["billing_id"]),
                convert_value(row["appointment_id"]),
                convert_value(row["billing_amount"]),
                convert_value(row["payment_type"]),
                convert_value(row["payment_status"]),
                convert_value(row["transaction_date"])
            )
        )

    cursor.executemany(query, records)

    print(
        f"Billing records loaded: {len(records)}"
    )


# --------------------------------------------------
# VERIFY DATABASE
# --------------------------------------------------

def verify_database(cursor):

    print("\n" + "=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)

    tables = [
        "patients",
        "doctors",
        "appointments",
        "appointment_services",
        "billing"
    ]

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table}: {count}"
        )

    print("=" * 60)


# --------------------------------------------------
# MAIN MYSQL LOAD FUNCTION
# --------------------------------------------------

def load_valid_data_to_mysql(valid_data):

    print("\nConnecting to MySQL...")

    password = input(
        "Enter MySQL password: "
    )

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=password,
        database=DB_CONFIG["database"]
    )

    cursor = connection.cursor()

    print("MySQL connection successful!")

    try:

        # Clear previous data
        reset_tables(cursor)

        print("\nLoading patients...")
        load_patients(
            cursor,
            valid_data["patients"]
        )

        print("\nLoading doctors...")
        load_doctors(
            cursor,
            valid_data["doctors"]
        )

        print("\nLoading appointments...")
        load_appointments(
            cursor,
            valid_data["appointments"]
        )

        print("\nLoading appointment services...")
        load_appointment_services(
            cursor,
            valid_data["appointment_services"]
        )

        print("\nLoading billing...")
        load_billing(
            cursor,
            valid_data["billing"]
        )

        connection.commit()

        print(
            "\nDATA SUCCESSFULLY LOADED INTO MYSQL!"
        )

        verify_database(cursor)

    except Exception as e:

        connection.rollback()

        print(
            "\nMySQL loading failed!"
        )

        print(
            f"Error: {e}"
        )

        raise

    finally:

        cursor.close()
        connection.close()

        print(
            "\nMySQL connection closed."
        )