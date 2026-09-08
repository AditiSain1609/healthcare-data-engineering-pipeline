-- =====================================================
-- HEALTHCARE DATA ENGINEERING PROJECT
-- DATABASE SCHEMA
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS healthcare_db;

USE healthcare_db;


-- =====================================================
-- 1. PATIENTS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS patients (
    patient_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(30),
    city VARCHAR(100),
    date_of_birth DATE
);

-- =====================================================
-- 2. DOCTORS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    city VARCHAR(100),
    consultation_fee DECIMAL(10,2)
);


-- =====================================================
-- 3. APPOINTMENTS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT,
    appointment_date DATETIME,
    appointment_type VARCHAR(50),
    status VARCHAR(50),

    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id)
);


-- =====================================================
-- 4. APPOINTMENT SERVICES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS appointment_services (
    service_id INT PRIMARY KEY,
    appointment_id INT NOT NULL,
    doctor_id INT NOT NULL,
    service_name VARCHAR(100),
    duration_minutes INT,
    quantity INT,

    CONSTRAINT fk_service_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(appointment_id),

    CONSTRAINT fk_service_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id)
);


-- =====================================================
-- 5. BILLING TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS billing (
    billing_id INT PRIMARY KEY,
    appointment_id INT NOT NULL,
    billing_amount DECIMAL(10,2),
    payment_type VARCHAR(50),
    payment_status VARCHAR(50),
    transaction_date DATETIME,

    CONSTRAINT fk_billing_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(appointment_id)
);


-- =====================================================
-- VERIFY TABLES
-- =====================================================

SHOW TABLES;