# Healthcare Data Engineering & Analytics Platform

An end-to-end healthcare data engineering and analytics platform built using Python, Pandas, NumPy, MySQL, SQL, FastAPI, Apache Airflow, Docker, Streamlit, and Power BI/Fabric.

The project demonstrates a complete data engineering workflow:

**Raw Data → Ingestion → Cleaning → Validation → Data Quality → Transformation → MySQL → Data Warehouse → Analytics → API → Dashboard → Orchestration**

---

## 📌 Project Overview

This project processes healthcare-related data from multiple CSV and JSON sources and transforms it into a reliable analytics-ready system.

The platform handles:

- Patient data
- Doctor data
- Appointment data
- Appointment services
- Billing and payment data

It includes data quality validation, invalid-record handling, ETL processing, incremental loading, MySQL storage, star-schema data warehousing, SQL analytics, REST APIs, dashboards, automated orchestration, and testing.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     Raw CSV / JSON   │
                    │                      │
                    │ patients.csv         │
                    │ doctors.csv          │
                    │ appointments.csv     │
                    │ appointment_services │
                    │ billing.json         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Python ETL Pipeline  │
                    │                      │
                    │ 1. Ingestion        │
                    │ 2. Cleaning         │
                    │ 3. Validation       │
                    │ 4. Data Quality     │
                    │ 5. Transformation   │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌────────────────┐          ┌─────────────────┐
        │ Valid Data     │          │ Invalid Data    │
        │                │          │                 │
        │ Cleaned Data   │          │ invalid_*.csv   │
        └───────┬────────┘          └─────────────────┘
                │
                ▼
        ┌─────────────────────┐
        │       MySQL         │
        │   healthcare_db     │
        └──────────┬──────────┘
                   │
          ┌────────┴─────────┐
          │                  │
          ▼                  ▼
 ┌──────────────────┐  ┌─────────────────┐
 │ Star Schema /    │  │ SQL Analytics   │
 │ Data Warehouse   │  │                 │
 └────────┬─────────┘  └─────────────────┘
          │
          ├───────────────┐
          │               │
          ▼               ▼
 ┌────────────────┐ ┌────────────────┐
 │ Power BI /     │ │ FastAPI REST   │
 │ Microsoft      │ │ API            │
 │ Fabric         │ └────────────────┘
 └────────────────┘

              Apache Airflow
                    +
                  Docker
              for orchestration
🛠️ Tech Stack
Technology	Purpose
Python	ETL and backend development
Pandas	Data processing
NumPy	Numerical transformations
MySQL	Relational database
SQL	Data analysis
SQLAlchemy	Database ORM
PyMySQL	MySQL connectivity
FastAPI	REST API
Streamlit	Interactive dashboard
Apache Airflow	Workflow orchestration
Docker	Airflow containerization
PostgreSQL	Airflow metadata database
Power BI / Microsoft Fabric	Business intelligence
Git	Version control
GitHub	Source code hosting
📂 Source Datasets

The project uses five healthcare datasets:

Dataset	Raw Records	Valid Records
patients.csv	501	499
doctors.csv	101	98
appointments.csv	2,001	1,940
appointment_services.csv	4,000	3,797
billing.json	2,000	1,937

The raw data intentionally contains realistic data-quality issues such as duplicates, missing values, invalid references, inconsistent text, and invalid numeric values.

🧹 Data Cleaning

The cleaning stage performs:

Duplicate removal
Text normalization
Email normalization
City normalization
Date conversion
Numeric conversion
Missing-value handling
Standardization of categorical fields
✅ Data Validation

The validation framework checks healthcare records against business rules.

Patients
Patient ID validation
Duplicate patient IDs
Email validation
Missing values
Doctors
Doctor ID validation
Positive consultation fees
Missing values
Appointments
Appointment ID validation
Valid appointment dates
Patient foreign-key validation
Doctor foreign-key validation
Valid appointment status/type
Appointment Services
Appointment reference validation
Doctor reference validation
Positive duration
Positive quantity
Billing
Billing ID validation
Appointment reference validation
Positive billing amount
Valid payment status

Invalid records are stored separately:

output/
├── invalid_patients.csv
├── invalid_doctors.csv
├── invalid_appointments.csv
├── invalid_appointment_services.csv
└── invalid_billing.csv
🔎 Data Quality Engine

The project includes a dedicated rule-based Data Quality Engine.

Location:

src/quality/
├── __init__.py
├── quality_rules.py
└── quality_engine.py

The engine evaluates rules such as:

ID uniqueness
Required fields
Email validity
Positive numeric values
Foreign-key references
Valid appointment dates
Valid payment statuses

The results are generated as rule-level quality reports.

📊 Data Transformations

The transformation layer generates:

Patient-level metrics
Doctor-level metrics
Daily revenue
Monthly revenue
Average appointment value
Cancellation percentage

The transformation logic uses Pandas and NumPy.

🗄️ MySQL Database

Database:

healthcare_db

Main tables:

patients
doctors
appointments
appointment_services
billing

Current validated dataset:

Table	Records
Patients	499
Doctors	98
Appointments	1,940
Appointment Services	3,797
Billing	1,937
🔄 Incremental ETL

The project supports incremental processing using ETL state tracking.

State file:

output/etl_state.json

The incremental pipeline tracks:

Appointment date watermark
Billing transaction date watermark

This allows new appointment and billing records to be processed without unnecessarily reprocessing the complete dataset.

⭐ Data Warehouse / Star Schema

A dimensional data warehouse layer is included for analytics.

Dimension Tables
dim_patient
dim_doctor
dim_date
dim_service
Fact Tables
fact_appointments
fact_billing

Warehouse SQL files:

sql/star_schema.sql
sql/warehouse_analysis.sql

Current warehouse counts:

Table	Records
dim_patient	499
dim_doctor	98
dim_date	243
dim_service	8
fact_appointments	1,940
fact_billing	1,937
📈 SQL Analytics

sql/analysis.sql contains 18 analytical queries covering:

WHERE
ORDER BY
LIMIT
COUNT
SUM
AVG
GROUP BY
HAVING
INNER JOIN
LEFT JOIN
Multi-table JOIN
Subqueries

Business questions include:

Top 10 patients by billing
Highest-revenue doctors
Patients with no appointments
Doctors with no services
Average appointment value by city
Patients with more than five appointments
Revenue by city
Doctors above average revenue
Patients with successful and failed payments
Appointment cancellation percentage
Monthly revenue trends
Service performance analysis
🌐 FastAPI REST API

The project exposes healthcare data and analytics through FastAPI.

Structure:

api/
├── main.py
├── database.py
├── models.py
└── routes/
    ├── patients.py
    ├── doctors.py
    ├── appointments.py
    ├── billing.py
    └── analytics.py

Run:

python3 -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

Swagger documentation:

http://127.0.0.1:8000/docs
API Endpoints
GET /patients/
GET /patients/{patient_id}

GET /doctors/
GET /doctors/{doctor_id}

GET /appointments/
GET /appointments/{appointment_id}

GET /billing/
GET /billing/{billing_id}

GET /analytics/summary
GET /analytics/top-patients
GET /analytics/top-doctors
GET /analytics/revenue-by-city
GET /analytics/cancellation-rate
📊 Streamlit Dashboard

An interactive Streamlit dashboard is included.

Run:

python3 -m streamlit run app/dashboard.py

Dashboard sections:

Overview
Patients
Doctors
Appointments
Billing
Data Quality
📊 Power BI / Microsoft Fabric

The project includes a business intelligence layer using Microsoft Fabric / Power BI Service.

Page 1 — Business Analytics

Includes:

Total Revenue
Total Patients
Total Appointments
Total Doctors
Monthly Revenue Trend
Top Doctors by Revenue
Revenue by City
Average Appointment Value
Appointment Status Distribution
Cancellation Analysis
Patient Analysis
Doctor Services Analysis
Billing / Revenue Analysis
Page 2 — Data Quality

Includes:

Overall Data Quality Score
Invalid Records by Table
Data Quality Rule Analysis
Invalid Patients
Invalid Doctors
Invalid Appointments
Invalid Services
Invalid Billing
⚙️ Apache Airflow

Apache Airflow is used to orchestrate the ETL pipeline.

DAG:

healthcare_etl_pipeline

Location:

airflow/dags/healthcare_etl_dag.py

The DAG executes the healthcare ETL pipeline on a scheduled basis.

🐳 Docker

Airflow is containerized using Docker Compose.

Configuration:

docker-compose.airflow.yaml

Docker is used to provide a consistent local Airflow environment on macOS.

🧪 Testing

Validation tests are included in:

tests/test_validation.py

The tests cover important validation behavior and data-quality checks.

📁 Project Structure
healthcare-data-engineering/
│
├── .gitignore
├── README.md
├── ER_Diagram.png
├── requirements.txt
├── docker-compose.airflow.yaml
│
├── data/
│   ├── patients.csv
│   ├── doctors.csv
│   ├── appointments.csv
│   ├── appointment_services.csv
│   └── billing.json
│
├── output/
│   ├── invalid_patients.csv
│   ├── invalid_doctors.csv
│   ├── invalid_appointments.csv
│   ├── invalid_appointment_services.csv
│   ├── invalid_billing.csv
│   ├── etl_state.json
│   └── data_quality_rules_report.csv
│
├── src/
│   ├── main.py
│   ├── ingestion.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── transformation.py
│   ├── load_to_mysql.py
│   ├── quality_report.py
│   ├── generate_data.py
│   ├── incremental_etl.py
│   │
│   └── quality/
│       ├── __init__.py
│       ├── quality_rules.py
│       └── quality_engine.py
│
├── sql/
│   ├── schema.sql
│   ├── analysis.sql
│   ├── star_schema.sql
│   └── warehouse_analysis.sql
│
├── app/
│   └── dashboard.py
│
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes/
│       ├── patients.py
│       ├── doctors.py
│       ├── appointments.py
│       ├── billing.py
│       └── analytics.py
│
├── airflow/
│   └── dags/
│       └── healthcare_etl_dag.py
│
└── tests/
    └── test_validation.py
🔐 Security

Sensitive configuration is stored using environment variables.

Do not commit:

MySQL passwords
API keys
.env files containing secrets
Personal credentials

Use .gitignore and environment variables for local configuration.

▶️ How to Run
1. Install dependencies
pip install -r requirements.txt
2. Configure environment variables

Create a local .env file:

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=healthcare_db
3. Run ETL
python3 -m src.main
4. Run Streamlit
python3 -m streamlit run app/dashboard.py
5. Run FastAPI
python3 -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
6. Run Airflow with Docker
docker compose -f docker-compose.airflow.yaml up -d

Airflow UI:

http://localhost:8080
🚀 Future Improvements

Potential production-level improvements include:

Cloud deployment using AWS/Azure/GCP
Apache Spark for large-scale processing
Kafka for real-time streaming
dbt for analytics engineering
Data lake integration
API authentication
API pagination and advanced filtering
Data lineage
Monitoring and alerting
CI/CD with GitHub Actions
Production-grade secrets management
Idempotent upsert strategy for incremental loads
