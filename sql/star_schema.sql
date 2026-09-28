USE healthcare_db;

-- ============================================
-- DATA WAREHOUSE - DIMENSION TABLES
-- ============================================

-- Patient Dimension
CREATE TABLE IF NOT EXISTS dim_patient (
    patient_key INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    date_of_birth DATE,
    UNIQUE (patient_id)
);

-- Doctor Dimension
CREATE TABLE IF NOT EXISTS dim_doctor (
    doctor_key INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    doctor_name VARCHAR(255),
    specialization VARCHAR(255),
    city VARCHAR(100),
    consultation_fee DECIMAL(10,2),
    UNIQUE (doctor_id)
);

-- Date Dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    day_name VARCHAR(20),
    UNIQUE (full_date)
);

-- Service Dimension
CREATE TABLE IF NOT EXISTS dim_service (
    service_key INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    UNIQUE (service_name)
);

-- ============================================
-- FACT TABLES
-- ============================================

-- Appointment Fact
CREATE TABLE IF NOT EXISTS fact_appointments (
    appointment_key INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    patient_key INT NOT NULL,
    doctor_key INT NOT NULL,
    date_key INT NOT NULL,
    appointment_type VARCHAR(100),
    status VARCHAR(100),

    FOREIGN KEY (patient_key) REFERENCES dim_patient(patient_key),
    FOREIGN KEY (doctor_key) REFERENCES dim_doctor(doctor_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),

    UNIQUE (appointment_id)
);

-- Billing Fact
CREATE TABLE IF NOT EXISTS fact_billing (
    billing_key INT AUTO_INCREMENT PRIMARY KEY,
    billing_id INT NOT NULL,
    appointment_id INT NOT NULL,
    date_key INT NOT NULL,
    billing_amount DECIMAL(12,2),
    payment_type VARCHAR(100),
    payment_status VARCHAR(100),

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),

    UNIQUE (billing_id)
);

-- ============================================
-- LOAD DIMENSION TABLES
-- ============================================

INSERT INTO dim_patient
(
    patient_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    date_of_birth
)
SELECT
    patient_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    date_of_birth
FROM patients;


INSERT INTO dim_doctor
(
    doctor_id,
    doctor_name,
    specialization,
    city,
    consultation_fee
)
SELECT
    doctor_id,
    doctor_name,
    specialization,
    city,
    consultation_fee
FROM doctors;


INSERT INTO dim_service
(
    service_name
)
SELECT DISTINCT
    service_name
FROM appointment_services
WHERE service_name IS NOT NULL;

INSERT INTO fact_appointments
(
    appointment_id,
    patient_key,
    doctor_key,
    date_key,
    appointment_type,
    status
)
SELECT
    a.appointment_id,
    p.patient_key,
    d.doctor_key,
    dt.date_key,
    a.appointment_type,
    a.status
FROM appointments a
INNER JOIN dim_patient p
    ON a.patient_id = p.patient_id
INNER JOIN dim_doctor d
    ON a.doctor_id = d.doctor_id
INNER JOIN dim_date dt
    ON DATE(a.appointment_date) = dt.full_date;

    INSERT INTO fact_billing
(
    billing_id,
    appointment_id,
    date_key,
    billing_amount,
    payment_type,
    payment_status
)
SELECT
    b.billing_id,
    b.appointment_id,
    dt.date_key,
    b.billing_amount,
    b.payment_type,
    b.payment_status
FROM billing b
INNER JOIN dim_date dt
    ON DATE(b.transaction_date) = dt.full_date;

SELECT 'dim_patient' AS table_name, COUNT(*) AS total FROM dim_patient
UNION ALL
SELECT 'dim_doctor', COUNT(*) FROM dim_doctor
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'dim_service', COUNT(*) FROM dim_service
UNION ALL
SELECT 'fact_appointments', COUNT(*) FROM fact_appointments
UNION ALL
SELECT 'fact_billing', COUNT(*) FROM fact_billing;