import os
import sys
import mysql.connector
import pandas as pd
import streamlit as st

# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="Healthcare Network Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Network Dashboard")
st.caption(
    "Healthcare Data Engineering Pipeline | "
    "Python + Pandas + MySQL + SQL"
)


# =========================================================
# MYSQL CONNECTION
# =========================================================

st.sidebar.header("🔐 MySQL Connection")

host = st.sidebar.text_input(
    "Host",
    value="localhost"
)

port = st.sidebar.number_input(
    "Port",
    value=3306,
    min_value=1
)

username = st.sidebar.text_input(
    "Username",
    value="root"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

database = st.sidebar.text_input(
    "Database",
    value="healthcare_db"
)


@st.cache_resource
def create_connection(host, port, username, password, database):

    return mysql.connector.connect(
        host=host,
        port=int(port),
        user=username,
        password=password,
        database=database
    )


def run_query(query, params=None):

    connection = create_connection(
        host,
        port,
        username,
        password,
        database
    )

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            query,
            params or ()
        )

        data = cursor.fetchall()

        return pd.DataFrame(data)

    finally:

        cursor.close()


# =========================================================
# CHECK CONNECTION
# =========================================================

if not password:

    st.info(
        "👈 Sidebar me MySQL password enter karo."
    )

    st.stop()


try:

    connection = create_connection(
        host,
        port,
        username,
        password,
        database
    )

    if connection.is_connected():

        st.sidebar.success(
            "✅ MySQL Connected"
        )

except Exception as error:

    st.error(
        f"MySQL connection failed: {error}"
    )

    st.stop()


# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.divider()

page = st.sidebar.radio(
    "📂 Dashboard Menu",

    [
        "📊 Overview",
        "👤 Patients",
        "👨‍⚕️ Doctors",
        "📅 Appointments",
        "💳 Billing",
        "🧪 Data Quality"
    ]
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "📊 Overview":

    st.header("📊 Healthcare Overview")

    # ---------------------------------------------
    # COUNTS
    # ---------------------------------------------

    patients = run_query(
        "SELECT COUNT(*) AS total FROM patients"
    )

    doctors = run_query(
        "SELECT COUNT(*) AS total FROM doctors"
    )

    appointments = run_query(
        "SELECT COUNT(*) AS total FROM appointments"
    )

    services = run_query(
        "SELECT COUNT(*) AS total FROM appointment_services"
    )

    billing = run_query(
        "SELECT COUNT(*) AS total FROM billing"
    )

    revenue = run_query(
        """
        SELECT
            COALESCE(
                SUM(billing_amount),
                0
            ) AS revenue

        FROM billing

        WHERE payment_status = 'Successful'
        """
    )

    # ---------------------------------------------
    # VALUES
    # ---------------------------------------------

    total_patients = int(
        patients.iloc[0]["total"]
    )

    total_doctors = int(
        doctors.iloc[0]["total"]
    )

    total_appointments = int(
        appointments.iloc[0]["total"]
    )

    total_services = int(
        services.iloc[0]["total"]
    )

    total_billing = int(
        billing.iloc[0]["total"]
    )

    total_revenue = float(
        revenue.iloc[0]["revenue"]
    )

    # ---------------------------------------------
    # KPI CARDS
    # ---------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👤 Patients",
        f"{total_patients:,}"
    )

    col2.metric(
        "👨‍⚕️ Doctors",
        f"{total_doctors:,}"
    )

    col3.metric(
        "📅 Appointments",
        f"{total_appointments:,}"
    )

    col4.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.2f}"
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "🩺 Services",
        f"{total_services:,}"
    )

    col6.metric(
        "💳 Billing Records",
        f"{total_billing:,}"
    )

    st.divider()

    # =====================================================
    # APPOINTMENT STATUS
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📅 Appointments by Status"
        )

        status_data = run_query(
            """
            SELECT
                status,
                COUNT(*) AS total

            FROM appointments

            GROUP BY status

            ORDER BY total DESC
            """
        )

        if not status_data.empty:

            st.bar_chart(
                status_data.set_index("status")
            )

    # =====================================================
    # MONTHLY REVENUE
    # =====================================================

    with right:

        st.subheader(
            "💰 Monthly Revenue"
        )

        monthly_revenue = run_query(
            """
            SELECT

                DATE_FORMAT(
                    transaction_date,
                    '%Y-%m'
                ) AS month,

                SUM(
                    billing_amount
                ) AS revenue

            FROM billing

            WHERE payment_status = 'Successful'

            GROUP BY
                DATE_FORMAT(
                    transaction_date,
                    '%Y-%m'
                )

            ORDER BY month
            """
        )

        if not monthly_revenue.empty:

            monthly_revenue["month"] = pd.to_datetime(
                monthly_revenue["month"]
            )

            monthly_revenue = monthly_revenue.set_index(
                "month"
            )

            st.line_chart(
                monthly_revenue["revenue"]
            )

    # =====================================================
    # TOP PATIENTS
    # =====================================================

    st.subheader(
        "🏆 Top 10 Patients by Billing"
    )

    top_patients = run_query(
        """
        SELECT

            p.patient_id,

            CONCAT(
                p.first_name,
                ' ',
                p.last_name
            ) AS patient_name,

            p.city,

            ROUND(
                SUM(
                    b.billing_amount
                ),
                2
            ) AS total_billing

        FROM patients p

        INNER JOIN appointments a
            ON p.patient_id = a.patient_id

        INNER JOIN billing b
            ON a.appointment_id = b.appointment_id

        WHERE b.payment_status = 'Successful'

        GROUP BY
            p.patient_id,
            p.first_name,
            p.last_name,
            p.city

        ORDER BY total_billing DESC

        LIMIT 10
        """
    )

    st.dataframe(
        top_patients,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PATIENTS
# =========================================================

elif page == "👤 Patients":

    st.header("👤 Patient Management")

    search = st.text_input(
        "🔎 Search Patient",
        placeholder="Name / Email / City / Patient ID"
    )

    if search:

        search_value = f"%{search}%"

        patient_data = run_query(
            """
            SELECT

                patient_id,
                first_name,
                last_name,
                email,
                phone,
                city,
                date_of_birth

            FROM patients

            WHERE
                CAST(patient_id AS CHAR)
                    LIKE %s

                OR first_name LIKE %s

                OR last_name LIKE %s

                OR email LIKE %s

                OR city LIKE %s

            ORDER BY patient_id

            LIMIT 50
            """,

            (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            )
        )

    else:

        patient_data = run_query(
            """
            SELECT

                patient_id,
                first_name,
                last_name,
                email,
                phone,
                city,
                date_of_birth

            FROM patients

            ORDER BY patient_id

            LIMIT 50
            """
        )

    st.dataframe(
        patient_data,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # PATIENT DETAILS
    # =====================================================

    if not patient_data.empty:

        selected_patient = st.selectbox(
            "Select Patient",
            patient_data["patient_id"].tolist()
        )

        patient_metrics = run_query(
            """
            SELECT

                COUNT(
                    DISTINCT a.appointment_id
                ) AS appointments,

                COALESCE(
                    SUM(
                        CASE

                            WHEN
                                b.payment_status
                                = 'Successful'

                            THEN
                                b.billing_amount

                            ELSE 0

                        END
                    ),
                    0
                ) AS billing,

                MAX(
                    a.appointment_date
                ) AS last_appointment

            FROM patients p

            LEFT JOIN appointments a

                ON p.patient_id
                = a.patient_id

            LEFT JOIN billing b

                ON a.appointment_id
                = b.appointment_id

            WHERE p.patient_id = %s
            """,

            (int(selected_patient),)
        )

        data = patient_metrics.iloc[0]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Appointments",
            int(data["appointments"])
        )

        c2.metric(
            "Total Billing",
            f"₹{float(data['billing']):,.2f}"
        )

        c3.metric(
            "Last Appointment",
            str(data["last_appointment"])
        )


# =========================================================
# DOCTORS
# =========================================================

elif page == "👨‍⚕️ Doctors":

    st.header("👨‍⚕️ Doctor Analytics")

    doctor_data = run_query(
        """
        SELECT

            d.doctor_id,

            d.doctor_name,

            d.specialization,

            d.city,

            d.consultation_fee,

            COUNT(
                DISTINCT a.appointment_id
            ) AS appointments,

            COUNT(
                DISTINCT s.service_name
            ) AS services,

            COALESCE(
                SUM(
                    CASE

                        WHEN
                            b.payment_status
                            = 'Successful'

                        THEN
                            b.billing_amount

                        ELSE 0

                    END
                ),
                0
            ) AS revenue

        FROM doctors d

        LEFT JOIN appointments a
            ON d.doctor_id
            = a.doctor_id

        LEFT JOIN appointment_services s
            ON d.doctor_id
            = s.doctor_id

        LEFT JOIN billing b
            ON a.appointment_id
            = b.appointment_id

        GROUP BY

            d.doctor_id,
            d.doctor_name,
            d.specialization,
            d.city,
            d.consultation_fee

        ORDER BY revenue DESC
        """
    )

    st.dataframe(
        doctor_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "🏆 Top 10 Doctors by Revenue"
    )

    top_doctors = doctor_data.head(10)

    if not top_doctors.empty:

        st.bar_chart(
            top_doctors.set_index(
                "doctor_name"
            )["revenue"]
        )


# =========================================================
# APPOINTMENTS
# =========================================================

elif page == "📅 Appointments":

    st.header("📅 Appointment Management")

    statuses = run_query(
        """
        SELECT DISTINCT status
        FROM appointments
        ORDER BY status
        """
    )

    status_list = ["All"] + statuses[
        "status"
    ].tolist()

    selected_status = st.selectbox(
        "Filter by Status",
        status_list
    )

    if selected_status == "All":

        appointment_data = run_query(
            """
            SELECT

                a.appointment_id,

                a.patient_id,

                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS patient_name,

                a.doctor_id,

                d.doctor_name,

                a.appointment_date,

                a.appointment_type,

                a.status

            FROM appointments a

            INNER JOIN patients p
                ON a.patient_id
                = p.patient_id

            INNER JOIN doctors d
                ON a.doctor_id
                = d.doctor_id

            ORDER BY
                a.appointment_date DESC

            LIMIT 500
            """
        )

    else:

        appointment_data = run_query(
            """
            SELECT

                a.appointment_id,

                a.patient_id,

                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS patient_name,

                a.doctor_id,

                d.doctor_name,

                a.appointment_date,

                a.appointment_type,

                a.status

            FROM appointments a

            INNER JOIN patients p
                ON a.patient_id
                = p.patient_id

            INNER JOIN doctors d
                ON a.doctor_id
                = d.doctor_id

            WHERE a.status = %s

            ORDER BY
                a.appointment_date DESC

            LIMIT 500
            """,

            (selected_status,)
        )

    st.metric(
        "Records",
        len(appointment_data)
    )

    st.dataframe(
        appointment_data,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# BILLING
# =========================================================

elif page == "💳 Billing":

    st.header("💳 Billing & Payments")

    payment_status = st.selectbox(
        "Payment Status",
        [
            "All",
            "Successful",
            "Failed",
            "Pending"
        ]
    )

    if payment_status == "All":

        billing_data = run_query(
            """
            SELECT

                billing_id,
                appointment_id,
                billing_amount,
                payment_type,
                payment_status,
                transaction_date

            FROM billing

            ORDER BY transaction_date DESC

            LIMIT 500
            """
        )

    else:

        billing_data = run_query(
            """
            SELECT

                billing_id,
                appointment_id,
                billing_amount,
                payment_type,
                payment_status,
                transaction_date

            FROM billing

            WHERE payment_status = %s

            ORDER BY transaction_date DESC

            LIMIT 500
            """,

            (payment_status,)
        )

    st.dataframe(
        billing_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "💰 Payment Summary"
    )

    payment_summary = run_query(
        """
        SELECT

            payment_status,

            COUNT(*) AS transactions,

            ROUND(
                SUM(billing_amount),
                2
            ) AS amount

        FROM billing

        GROUP BY payment_status

        ORDER BY amount DESC
        """
    )

    st.dataframe(
        payment_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DATA QUALITY
# =========================================================

elif page == "🧪 Data Quality":

    st.header("🧪 Data Quality Dashboard")

    report_path = os.path.join(
        PROJECT_ROOT,
        "output",
        "data_quality_report.csv"
    )

    if os.path.exists(report_path):

        report = pd.read_csv(
            report_path
        )

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "📊 Quality Score"
        )

        quality_chart = report[
            [
                "table_name",
                "quality_score"
            ]
        ].set_index(
            "table_name"
        )

        st.bar_chart(
            quality_chart
        )

        st.subheader(
            "❌ Invalid Records"
        )

        invalid_chart = report[
            [
                "table_name",
                "invalid_records"
            ]
        ].set_index(
            "table_name"
        )

        st.bar_chart(
            invalid_chart
        )

    else:

        st.warning(
            "Quality report nahi mila."
        )

        st.code(
            "python src/quality_report.py"
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "Healthcare Network Data Engineering Project"
)

st.sidebar.caption(
    "ETL → MySQL → SQL → Dashboard"
)