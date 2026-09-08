# Healthcare Network Data Engineering Pipeline

An end-to-end healthcare data engineering project that ingests CSV/JSON data, cleans and validates records with Python/Pandas, transforms the data, loads valid records into MySQL, and performs business analysis with SQL. A Streamlit dashboard is also included for interactive exploration.

## Project Overview

Healthcare networks receive operational data from multiple systems. Raw data can contain duplicates, missing values, inconsistent text, incorrect data types, invalid values, and invalid patient/doctor/appointment references.

This project builds a modular ETL pipeline to turn those raw files into clean, validated, relational data that can be queried for business insights.

The pipeline follows:

**Raw CSV / JSON → Python Ingestion → Cleaning → Validation → Valid/Invalid Separation → Transformation → MySQL → SQL Analysis → Business Insights**

## Business Scenario

The project represents a multi-city hospital network containing:

- Patients
- Doctors
- Appointments
- Appointment services
- Billing and payment transactions

Operations analysts need reliable data for reporting, revenue analysis, appointment analysis, patient activity analysis, and data-quality monitoring.

## Architecture

```text
patients.csv
doctors.csv
appointments.csv
appointment_services.csv
billing.json
        │
        ▼
┌──────────────────────┐
│ Python Data Ingestion│
│      Pandas          │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│    Data Cleaning     │
│ duplicates / formats │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│   Data Validation    │
│ business-rule checks │
└───────┬────────┬─────┘
        │        │
        ▼        ▼
   Valid Data   Invalid CSVs
        │
        ▼
┌──────────────────────┐
│   Transformation     │
│ Pandas + NumPy       │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│       MySQL          │
│ relational database  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│     SQL Analysis     │
│ 18 analytical queries│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  Business Insights   │
│ + Streamlit Dashboard│
└──────────────────────┘
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL orchestration and modular pipeline |
| Pandas | Data ingestion, cleaning, validation, transformation |
| NumPy | Numerical transformation and metric calculations |
| MySQL | Relational storage and integrity constraints |
| mysql-connector-python | Python-to-MySQL connection and loading |
| SQL | Business analysis |
| Streamlit | Interactive dashboard |
| Git/GitHub | Version control and project documentation |

## Dataset

The project contains five source datasets:

| Dataset | Raw Records | Valid Records |
|---|---:|---:|
| patients.csv | 501 | 499 |
| doctors.csv | 101 | 98 |
| appointments.csv | 2,001 | 1,940 |
| appointment_services.csv | 4,000 | 3,797 |
| billing.json | 2,000 | 1,937 |

The raw data intentionally contains realistic data-quality issues so that the pipeline demonstrates actual cleaning and validation rather than processing an already-clean dataset.

## Data Quality Issues

The raw data includes:

- Missing patient email
- Missing doctor consultation fee
- Missing appointment date
- Duplicate patient records
- Duplicate doctor records
- Duplicate appointment records
- Inconsistent city/text formatting
- Inconsistent payment/appointment text
- Numeric values represented in incorrect formats
- Negative consultation fees
- Negative service duration/quantity
- Invalid payment statuses
- Invalid patient IDs
- Invalid doctor IDs
- Invalid appointment references

## Cleaning Strategy

Cleaning is performed before business validation.

### Patients
- Remove duplicate `patient_id` records
- Strip and standardize city names
- Normalize email text to lowercase
- Convert date of birth to a date type

### Doctors
- Remove duplicate `doctor_id` records
- Strip doctor names
- Standardize specialization and city text
- Convert consultation fee to numeric

### Appointments
- Remove duplicate `appointment_id` records
- Convert patient/doctor IDs to numeric
- Convert appointment date to datetime
- Standardize appointment type and status text

### Appointment Services
- Convert IDs, duration, and quantity to numeric
- Standardize service names

### Billing
- Convert appointment ID and billing amount to numeric
- Standardize payment type and payment status
- Convert transaction date to datetime

## Validation Rules

Invalid records are not silently discarded. They are written to separate CSV files under `output/`.

### Patients
- Patient ID must be non-null
- Patient ID must be unique
- Email must follow a reasonable email pattern

### Doctors
- Doctor ID must be unique and non-null
- Consultation fee must be greater than zero

### Appointments
- Appointment ID must be unique and non-null
- Patient ID must exist in the valid patients dataset
- Doctor ID must exist in the valid doctors dataset
- Appointment date must be non-null

### Appointment Services
- Appointment ID must exist in valid appointments
- Doctor ID must exist in valid doctors
- Duration must be greater than zero
- Quantity must be greater than zero

### Billing
- Billing ID must be unique and non-null
- Appointment ID must exist in valid appointments
- Billing amount must be greater than zero
- Payment status must be one of `Successful`, `Failed`, or `Pending`

## Invalid Records

The latest pipeline run produced:

| Dataset | Invalid Records |
|---|---:|
| Patients | 1 |
| Doctors | 2 |
| Appointments | 60 |
| Appointment Services | 203 |
| Billing | 63 |

Generated files:

```text
output/
├── invalid_patients.csv
├── invalid_doctors.csv
├── invalid_appointments.csv
├── invalid_appointment_services.csv
└── invalid_billing.csv
```

## Database Design

The MySQL database is named `healthcare_db`.

Tables:

- `patients`
- `doctors`
- `appointments`
- `appointment_services`
- `billing`

### Relationships

- `patients.patient_id` → `appointments.patient_id`
- `doctors.doctor_id` → `appointment_services.doctor_id`
- `appointments.appointment_id` → `appointment_services.appointment_id`
- `appointments.appointment_id` → `billing.appointment_id`

Parent tables are loaded before child tables so foreign-key relationships remain valid.

See `ER_Diagram.png` for the database relationship diagram.

## ETL Process

The complete pipeline is executed through:

```bash
python3 src/main.py
```

Pipeline stages:

1. Load raw CSV/JSON data
2. Clean the datasets
3. Validate records
4. Separate valid and invalid records
5. Transform the valid data
6. Generate the data-quality report
7. Connect to MySQL
8. Clear previous pipeline data
9. Load valid records in dependency order
10. Verify MySQL record counts
11. Write pipeline logs

### Latest Successful Load

```text
patients                     499
doctors                       98
appointments                1940
appointment_services        3797
billing                     1937
```

## Transformations

The Pandas/NumPy transformation layer produces:

### Patient Metrics
- Total appointments per patient
- Total billing amount per patient
- Average appointment value
- Last appointment date

### Doctor Metrics
- Total appointment services
- Total revenue
- Number of appointments
- Consultation fee information

### Business Metrics
- Daily revenue
- Monthly revenue
- Average appointment value
- Cancellation percentage

Generated files include:

```text
output/
├── patient_metrics.csv
├── doctor_metrics.csv
├── daily_revenue.csv
├── monthly_revenue.csv
└── data_quality_report.csv
```

## Data Quality Report

The project includes an automated data-quality score.

The latest report tracks:

- Total records
- Cleaned records
- Valid records
- Invalid records
- Duplicate records
- Missing values
- Quality score

Approximate latest quality scores from the pipeline's scoring method:

| Dataset | Quality Score |
|---|---:|
| Patients | 99.60 |
| Doctors | 97.03 |
| Appointments | 96.95 |
| Appointment Services | 94.92 |
| Billing | 96.85 |

## SQL Analysis

`sql/analysis.sql` contains 18 analytical queries demonstrating:

- `WHERE`
- `ORDER BY`
- `LIMIT`
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `GROUP BY`
- `HAVING`
- `INNER JOIN`
- `LEFT JOIN`
- Multiple-table joins
- Subqueries

Required business questions include:

1. Top 10 patients by total billing
2. Highest-revenue doctors
3. Patients with no appointments
4. Doctors with no appointment services
5. Average appointment value by city
6. Patients with more than five appointments
7. Highest-revenue city
8. Doctors earning above average revenue
9. Patients with both successful and failed payments
10. Appointment cancellation percentage

### Additional Business Questions

The analysis also includes additional operational questions such as:

- How are appointments distributed by status?
- What is the average consultation fee by specialization?
- Which services are used most frequently?

## Streamlit Dashboard

A Streamlit dashboard is included for interactive use.

Run:

```bash
python3 -m streamlit run app/dashboard.py
```

Then open:

```text
http://localhost:8501
```

Dashboard sections:

- Overview
- Patients
- Doctors
- Appointments
- Billing
- Data Quality

The dashboard connects to MySQL and presents operational and data-quality information without exposing database credentials in source code.

## Project Structure

```text
healthcare-data-engineering/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── patients.csv
│   ├── doctors.csv
│   ├── appointments.csv
│   ├── appointment_services.csv
│   └── billing.json
│
├── logs/
│   └── pipeline.log
│
├── output/
│   ├── invalid_patients.csv
│   ├── invalid_doctors.csv
│   ├── invalid_appointments.csv
│   ├── invalid_appointment_services.csv
│   ├── invalid_billing.csv
│   ├── patient_metrics.csv
│   ├── doctor_metrics.csv
│   ├── daily_revenue.csv
│   ├── monthly_revenue.csv
│   └── data_quality_report.csv
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
├── src/
│   ├── generate_data.py
│   ├── ingestion.py
│   ├── cleaning.py
│   ├── validation.py
│   ├── transformation.py
│   ├── quality_report.py
│   ├── load_to_mysql.py
│   └── main.py
│
├── requirements.txt
├── ER_Diagram.png
└── README.md
```

## Error Handling and Logging

The pipeline writes execution information to:

```text
logs/pipeline.log
```

The log records important events such as:

- Files loaded
- Record counts
- Validation results
- Transformation completion
- MySQL connection status
- Database loading
- Errors

## Original Feature

### Automated Data Quality Score

An automated data-quality scoring feature was added beyond the core ETL requirements.

The score considers invalid records and missing values and produces a dataset-level quality score in `data_quality_report.csv`.

This gives the team a quick way to identify which source dataset needs the most attention.

## Challenges

One practical challenge was handling MySQL table locks during repeated ETL runs. Previous pipeline sessions were holding locks on the `billing` table, causing `TRUNCATE`/`DELETE` operations to wait.

The issue was diagnosed through MySQL process inspection and resolved by terminating the stale sessions. The reset logic was then changed to use ordered `DELETE` operations with foreign-key checks temporarily disabled.

This demonstrates an important real-world database troubleshooting scenario.

## Security

Do **not** commit:

- MySQL passwords
- API keys
- Personal credentials
- `.env` files containing secrets

Use environment variables or a local configuration that is excluded from Git.

Example:

```text
.env
```

should be included in `.gitignore` if used.

## Future Improvements

For a production-grade version, the pipeline could be extended with:

- Environment-based configuration
- Retry logic for transient database failures
- Incremental loading instead of full refresh
- Data lineage tracking
- Automated unit tests
- CI/CD with GitHub Actions
- Airflow or another workflow orchestrator
- Cloud object storage
- Monitoring and alerting
- More advanced data-quality rules
- Containerization with Docker

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate sample data

```bash
python3 src/generate_data.py
```

### 3. Create the MySQL schema

Run:

```text
sql/schema.sql
```

inside MySQL/DBeaver.

### 4. Run the ETL pipeline

```bash
python3 src/main.py
```

Enter the MySQL password when prompted.

### 5. Run the dashboard

```bash
python3 -m streamlit run app/dashboard.py
```

## Deliverables

This repository contains the required project components:

- Python source code
- Dataset generator and raw datasets
- MySQL `schema.sql`
- SQL `analysis.sql`
- ER diagram
- Data-quality report
- Pipeline log
- README
- Invalid-record output files
- Transformation outputs
- Streamlit dashboard

---

**Project:** Healthcare Network Data Engineering Pipeline  
**Focus:** Python → Pandas/NumPy → MySQL → SQL Analysis → Dashboard
