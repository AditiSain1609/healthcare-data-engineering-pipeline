USE healthcare_db;

-- ============================================
-- WAREHOUSE ANALYSIS
-- ============================================

-- 1. Revenue by Month
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.billing_amount) AS total_revenue
FROM fact_billing f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;

-- 2. Top 10 Doctors by Revenue

SELECT
    d.doctor_id,
    d.doctor_name,
    d.specialization,
    SUM(f.billing_amount) AS total_revenue
FROM fact_billing f
JOIN fact_appointments fa
    ON f.appointment_id = fa.appointment_id
JOIN dim_doctor d
    ON fa.doctor_key = d.doctor_key
GROUP BY
    d.doctor_id,
    d.doctor_name,
    d.specialization
ORDER BY
    total_revenue DESC
LIMIT 10;

-- 3. Revenue by City

SELECT
    d.city,
    SUM(f.billing_amount) AS total_revenue
FROM fact_billing f
JOIN fact_appointments fa
    ON f.appointment_id = fa.appointment_id
JOIN dim_doctor d
    ON fa.doctor_key = d.doctor_key
GROUP BY
    d.city
ORDER BY
    total_revenue DESC;

-- 4. Average Appointment Value by City

SELECT
    d.city,
    COUNT(f.billing_id) AS total_bills,
    SUM(f.billing_amount) AS total_revenue,
    ROUND(AVG(f.billing_amount), 2) AS average_appointment_value
FROM fact_billing f
JOIN fact_appointments fa
    ON f.appointment_id = fa.appointment_id
JOIN dim_doctor d
    ON fa.doctor_key = d.doctor_key
GROUP BY
    d.city
ORDER BY
    average_appointment_value DESC;

-- 5. Cancellation Rate

SELECT
    COUNT(*) AS total_appointments,
    SUM(
        CASE
            WHEN LOWER(status) = 'cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_appointments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN LOWER(status) = 'cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate_percentage
FROM fact_appointments;