import pandas as pd
import pytest

from src.validation import (
    is_valid_email,
    validate_patients,
    validate_doctors,
    validate_appointments,
    validate_appointment_services,
    validate_billing,
    validate_all_data,
)


@pytest.fixture(autouse=True)
def _skip_invalid_csv_writes(monkeypatch):
    monkeypatch.setattr(
        "src.validation.save_invalid_records",
        lambda name, df: None,
    )


class TestIsValidEmail:
    @pytest.mark.parametrize(
        "email,expected",
        [
            ("alice@example.com", True),
            ("bob.smith@hospital.org", True),
            ("not-an-email", False),
            ("missing@domain", False),
            ("", False),
            (None, False),
        ],
    )
    def test_email_validation(self, email, expected):
        assert is_valid_email(email) is expected


class TestValidatePatients:
    def test_valid_patients_pass(self):
        df = pd.DataFrame(
            {
                "patient_id": [1, 2],
                "email": ["alice@example.com", "bob@example.com"],
            }
        )

        valid_df, invalid_df = validate_patients(df)

        assert len(valid_df) == 2
        assert invalid_df.empty

    def test_duplicate_patient_id_fails(self):
        df = pd.DataFrame(
            {
                "patient_id": [1, 1],
                "email": ["alice@example.com", "bob@example.com"],
            }
        )

        valid_df, invalid_df = validate_patients(df)

        assert valid_df.empty
        assert len(invalid_df) == 2

    def test_null_patient_id_fails(self):
        df = pd.DataFrame(
            {
                "patient_id": [None],
                "email": ["alice@example.com"],
            }
        )

        valid_df, invalid_df = validate_patients(df)

        assert valid_df.empty
        assert len(invalid_df) == 1

    def test_invalid_email_fails(self):
        df = pd.DataFrame(
            {
                "patient_id": [1],
                "email": ["not-an-email"],
            }
        )

        valid_df, invalid_df = validate_patients(df)

        assert valid_df.empty
        assert len(invalid_df) == 1


class TestValidateDoctors:
    def test_valid_doctors_pass(self):
        df = pd.DataFrame(
            {
                "doctor_id": [10, 20],
                "consultation_fee": [500.0, 750.0],
            }
        )

        valid_df, invalid_df = validate_doctors(df)

        assert len(valid_df) == 2
        assert invalid_df.empty

    def test_duplicate_doctor_id_fails(self):
        df = pd.DataFrame(
            {
                "doctor_id": [10, 10],
                "consultation_fee": [500.0, 750.0],
            }
        )

        valid_df, invalid_df = validate_doctors(df)

        assert valid_df.empty
        assert len(invalid_df) == 2

    @pytest.mark.parametrize("fee", [0, -100, None])
    def test_invalid_consultation_fee_fails(self, fee):
        df = pd.DataFrame(
            {
                "doctor_id": [10],
                "consultation_fee": [fee],
            }
        )

        valid_df, invalid_df = validate_doctors(df)

        assert valid_df.empty
        assert len(invalid_df) == 1


class TestValidateAppointments:
    @pytest.fixture
    def reference_ids(self):
        return pd.Series([1, 2]), pd.Series([10, 20])

    def test_valid_appointments_pass(self, reference_ids):
        valid_patient_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [100],
                "patient_id": [1],
                "doctor_id": [10],
                "appointment_date": [pd.Timestamp("2024-01-15")],
            }
        )

        valid_df, invalid_df = validate_appointments(
            df,
            valid_patient_ids,
            valid_doctor_ids,
        )

        assert len(valid_df) == 1
        assert invalid_df.empty

    def test_invalid_patient_reference_fails(self, reference_ids):
        valid_patient_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [100],
                "patient_id": [999],
                "doctor_id": [10],
                "appointment_date": [pd.Timestamp("2024-01-15")],
            }
        )

        valid_df, invalid_df = validate_appointments(
            df,
            valid_patient_ids,
            valid_doctor_ids,
        )

        assert valid_df.empty
        assert len(invalid_df) == 1

    def test_null_appointment_date_fails(self, reference_ids):
        valid_patient_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [100],
                "patient_id": [1],
                "doctor_id": [10],
                "appointment_date": [None],
            }
        )

        valid_df, invalid_df = validate_appointments(
            df,
            valid_patient_ids,
            valid_doctor_ids,
        )

        assert valid_df.empty
        assert len(invalid_df) == 1


class TestValidateAppointmentServices:
    @pytest.fixture
    def reference_ids(self):
        return pd.Series([100, 200]), pd.Series([10, 20])

    def test_valid_services_pass(self, reference_ids):
        valid_appointment_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [100],
                "doctor_id": [10],
                "duration_minutes": [30],
                "quantity": [1],
            }
        )

        valid_df, invalid_df = validate_appointment_services(
            df,
            valid_appointment_ids,
            valid_doctor_ids,
        )

        assert len(valid_df) == 1
        assert invalid_df.empty

    def test_invalid_appointment_reference_fails(self, reference_ids):
        valid_appointment_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [999],
                "doctor_id": [10],
                "duration_minutes": [30],
                "quantity": [1],
            }
        )

        valid_df, invalid_df = validate_appointment_services(
            df,
            valid_appointment_ids,
            valid_doctor_ids,
        )

        assert valid_df.empty
        assert len(invalid_df) == 1

    @pytest.mark.parametrize("duration,quantity", [(0, 1), (30, 0), (-5, 1)])
    def test_non_positive_duration_or_quantity_fails(
        self, reference_ids, duration, quantity
    ):
        valid_appointment_ids, valid_doctor_ids = reference_ids

        df = pd.DataFrame(
            {
                "appointment_id": [100],
                "doctor_id": [10],
                "duration_minutes": [duration],
                "quantity": [quantity],
            }
        )

        valid_df, invalid_df = validate_appointment_services(
            df,
            valid_appointment_ids,
            valid_doctor_ids,
        )

        assert valid_df.empty
        assert len(invalid_df) == 1


class TestValidateBilling:
    @pytest.fixture
    def valid_appointment_ids(self):
        return pd.Series([100, 200])

    def test_valid_billing_passes(self, valid_appointment_ids):
        df = pd.DataFrame(
            {
                "billing_id": [1],
                "appointment_id": [100],
                "billing_amount": [1500.0],
                "payment_status": ["Successful"],
            }
        )

        valid_df, invalid_df = validate_billing(df, valid_appointment_ids)

        assert len(valid_df) == 1
        assert invalid_df.empty

    def test_invalid_appointment_reference_fails(self, valid_appointment_ids):
        df = pd.DataFrame(
            {
                "billing_id": [1],
                "appointment_id": [999],
                "billing_amount": [1500.0],
                "payment_status": ["Successful"],
            }
        )

        valid_df, invalid_df = validate_billing(df, valid_appointment_ids)

        assert valid_df.empty
        assert len(invalid_df) == 1

    def test_invalid_payment_status_fails(self, valid_appointment_ids):
        df = pd.DataFrame(
            {
                "billing_id": [1],
                "appointment_id": [100],
                "billing_amount": [1500.0],
                "payment_status": ["Refunded"],
            }
        )

        valid_df, invalid_df = validate_billing(df, valid_appointment_ids)

        assert valid_df.empty
        assert len(invalid_df) == 1

    @pytest.mark.parametrize("amount", [0, -50, None])
    def test_invalid_billing_amount_fails(self, valid_appointment_ids, amount):
        df = pd.DataFrame(
            {
                "billing_id": [1],
                "appointment_id": [100],
                "billing_amount": [amount],
                "payment_status": ["Successful"],
            }
        )

        valid_df, invalid_df = validate_billing(df, valid_appointment_ids)

        assert valid_df.empty
        assert len(invalid_df) == 1


class TestValidateAllData:
    def test_end_to_end_validation_filters_invalid_records(self):
        data = {
            "patients": pd.DataFrame(
                {
                    "patient_id": [1, 2],
                    "email": ["alice@example.com", "bad-email"],
                }
            ),
            "doctors": pd.DataFrame(
                {
                    "doctor_id": [10],
                    "consultation_fee": [500.0],
                }
            ),
            "appointments": pd.DataFrame(
                {
                    "appointment_id": [100, 101],
                    "patient_id": [1, 999],
                    "doctor_id": [10, 10],
                    "appointment_date": [
                        pd.Timestamp("2024-01-15"),
                        pd.Timestamp("2024-01-16"),
                    ],
                }
            ),
            "appointment_services": pd.DataFrame(
                {
                    "appointment_id": [100],
                    "doctor_id": [10],
                    "duration_minutes": [30],
                    "quantity": [1],
                }
            ),
            "billing": pd.DataFrame(
                {
                    "billing_id": [1],
                    "appointment_id": [100],
                    "billing_amount": [1500.0],
                    "payment_status": ["Successful"],
                }
            ),
        }

        valid_data = validate_all_data(data)

        assert len(valid_data["patients"]) == 1
        assert len(valid_data["doctors"]) == 1
        assert len(valid_data["appointments"]) == 1
        assert len(valid_data["appointment_services"]) == 1
        assert len(valid_data["billing"]) == 1
