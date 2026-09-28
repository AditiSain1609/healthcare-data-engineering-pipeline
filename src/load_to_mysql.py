import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_mysql_connection():
    """
    Create MySQL connection using environment variables.
    """

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "healthcare_db")
    )


def get_connection_with_prompt():
    """
    Create MySQL connection.
    If MYSQL_PASSWORD is not configured, ask the user.
    """

    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        password = input("Enter MySQL password: ")

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=password,
        database=os.getenv("MYSQL_DATABASE", "healthcare_db")
    )


def reset_tables(cursor):
    """
    Reset tables for a complete/full load.
    """

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    tables = [
        "appointment_services",
        "billing",
        "appointments",
        "doctors",
        "patients"
    ]

    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table}")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def insert_dataframe(cursor, df, table_name):
    """
    Insert a pandas DataFrame into MySQL.
    """

    if df.empty:
        print(f"No records to insert into {table_name}")
        return

    columns = list(df.columns)

    column_string = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = f"""
        INSERT INTO {table_name}
        ({column_string})
        VALUES ({placeholders})
    """

    records = []

    for row in df.itertuples(index=False, name=None):
        cleaned_row = []

        for value in row:
            if pd.isna(value):
                cleaned_row.append(None)
            elif isinstance(value, pd.Timestamp):
                cleaned_row.append(value.to_pydatetime())
            else:
                cleaned_row.append(value)

        records.append(tuple(cleaned_row))

    cursor.executemany(query, records)

    print(f"Inserted {len(records)} records into {table_name}")


def load_valid_data_to_mysql(valid_data):
    """
    Complete/full load.

    Existing MySQL tables are reset and valid records
    are loaded in parent-to-child order.
    """

    connection = get_connection_with_prompt()
    cursor = connection.cursor()

    try:
        print("\nResetting MySQL tables...")
        reset_tables(cursor)

        insert_dataframe(
            cursor,
            valid_data["patients"],
            "patients"
        )

        insert_dataframe(
            cursor,
            valid_data["doctors"],
            "doctors"
        )

        insert_dataframe(
            cursor,
            valid_data["appointments"],
            "appointments"
        )

        insert_dataframe(
            cursor,
            valid_data["appointment_services"],
            "appointment_services"
        )

        insert_dataframe(
            cursor,
            valid_data["billing"],
            "billing"
        )

        connection.commit()

        print("\nFull MySQL load completed successfully.")

        verify_mysql_counts(cursor)

    except Exception as error:
        connection.rollback()
        print("\nMySQL load failed:")
        print(error)
        raise

    finally:
        cursor.close()
        connection.close()


def load_incremental_data_to_mysql(
    appointments=None,
    appointment_services=None,
    billing=None
):
    """
    Incremental load.

    Only new appointment, service and billing records
    are inserted. Existing data is NOT deleted.
    """

    connection = get_connection_with_prompt()
    cursor = connection.cursor()

    try:
        print("\nStarting incremental MySQL load...")

        if appointments is not None:
            insert_dataframe(
                cursor,
                appointments,
                "appointments"
            )

        if appointment_services is not None:
            insert_dataframe(
                cursor,
                appointment_services,
                "appointment_services"
            )

        if billing is not None:
            insert_dataframe(
                cursor,
                billing,
                "billing"
            )

        connection.commit()

        print("\nIncremental MySQL load completed successfully.")

        verify_mysql_counts(cursor)

    except Exception as error:
        connection.rollback()

        print("\nIncremental MySQL load failed:")
        print(error)

        raise

    finally:
        cursor.close()
        connection.close()


def verify_mysql_counts(cursor):
    """
    Verify current record counts in MySQL.
    """

    tables = [
        "patients",
        "doctors",
        "appointments",
        "appointment_services",
        "billing"
    ]

    print("\nMySQL record counts:")

    for table in tables:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{table}: {count}")


if __name__ == "__main__":

    print("Testing MySQL loader module...")

    print("""
This module supports:

1. Full load
   load_valid_data_to_mysql()

2. Incremental load
   load_incremental_data_to_mysql()

No database operation is executed automatically here.
""")
