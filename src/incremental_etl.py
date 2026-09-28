import json
import os
from datetime import datetime


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

STATE_FILE = os.path.join(
    PROJECT_ROOT,
    "output",
    "etl_state.json"
)


def load_etl_state():
    """
    Load the latest successful ETL state.

    If no state file exists, return initial state.
    """

    if not os.path.exists(STATE_FILE):
        return {
            "appointments": {
                "last_processed_date": None
            },
            "billing": {
                "last_processed_date": None
            }
        }

    with open(STATE_FILE, "r") as file:
        return json.load(file)


def save_etl_state(
    appointment_date,
    billing_date
):
    """
    Save ETL state only after a successful load.
    """

    state = {
        "appointments": {
            "last_processed_date": appointment_date
        },
        "billing": {
            "last_processed_date": billing_date
        }
    }

    with open(STATE_FILE, "w") as file:
        json.dump(
            state,
            file,
            indent=4
        )

    print(
        f"ETL state saved: {STATE_FILE}"
    )

import pandas as pd


def get_incremental_records(
    df,
    date_column,
    last_processed_date
):
    """
    Return only records newer than the
    last successfully processed date.

    If no previous date exists, return all records.
    """

    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    if last_processed_date is None:
        return data

    last_date = pd.to_datetime(
        last_processed_date
    )

    incremental_data = data[
        data[date_column] > last_date
    ].copy()

    return incremental_data

def get_current_timestamp():
    """
    Return current timestamp.
    """

    return datetime.now().isoformat()


def start_incremental_run():
    """
    Start a new ETL run.
    """

    state = load_etl_state()

    print("\nCurrent ETL state:")
    print(json.dumps(state, indent=4))

    return state


def complete_incremental_run(
    appointment_date,
    billing_date
):
    """
    Mark an ETL run as successfully completed.
    """

    save_etl_state(
        appointment_date,
        billing_date
    )

    print(
        "\nIncremental ETL run completed successfully."
    )


if __name__ == "__main__":

    print("Testing Incremental ETL State Manager...")

    state = load_etl_state()

    print("\nCurrent state:")
    print(json.dumps(state, indent=4))

    print("\nState manager is working correctly.")