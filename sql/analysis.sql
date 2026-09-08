USE healthcare_db;


-- =====================================================
-- HEALTHCARE DATA ENGINEERING
-- SQL ANALYSIS
-- =====================================================


-- =====================================================
-- Q1. WHERE
-- Find all successful payments
-- =====================================================

SELECT *
FROM billing
WHERE payment_status = 'Successful';


-- =====================================================
-- Q2. ORDER BY + LIMIT
-- Top 10 patients by total billing
-- =====================================================

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    SUM(b.billing_amount) AS total_billing
FROM patients p
INNER JOIN appointments a
    ON p.patient_id = a.patient_id
INNER JOIN billing b
    ON a.appointment_id = b.appointment_id
GROUP BY
    p.patient_id,
    p.first_name,
    p.last_name
ORDER BY total_billing DESC
LIMIT 10;


-- =====================================================
-- Q3. Highest revenue doctors
-- =====================================================

SELECT
    d.doctor_id,
    d.doctor_name,
    SUM(b.billing_amount) AS total_revenue
FROM doctors d
INNER JOIN appointment_services s
    ON d.doctor_id = s.doctor_id
INNER JOIN billing b
    ON s.appointment_id = b.appointment_id
GROUP BY
    d.doctor_id,
    d.doctor_name
ORDER BY total_revenue DESC;


-- =====================================================
-- Q4. Patients with NO appointments
-- LEFT JOIN
-- =====================================================

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name
FROM patients p
LEFT JOIN appointments a
    ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;


-- =====================================================
-- Q5. Doctors with NO services
-- LEFT JOIN
-- =====================================================

SELECT
    d.doctor_id,
    d.doctor_name
FROM doctors d
LEFT JOIN appointment_services s
    ON d.doctor_id = s.doctor_id
WHERE s.service_id IS NULL;


-- =====================================================
-- Q6. Average appointment value by city
-- =====================================================

SELECT
    p.city,
    AVG(b.billing_amount) AS avg_appointment_value
FROM patients p
INNER JOIN appointments a
    ON p.patient_id = a.patient_id
INNER JOIN billing b
    ON a.appointment_id = b.appointment_id
GROUP BY p.city
ORDER BY avg_appointment_value DESC;


-- =====================================================
-- Q7. Patients with more than 5 appointments
-- GROUP BY + HAVING
-- =====================================================

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    COUNT(a.appointment_id) AS total_appointments
FROM patients p
INNER JOIN appointments a
    ON p.patient_id = a.patient_id
GROUP BY
    p.patient_id,
    p.first_name,
    p.last_name
HAVING COUNT(a.appointment_id) > 5
ORDER BY total_appointments DESC;


-- =====================================================
-- Q8. Highest revenue city
-- =====================================================

SELECT
    p.city,
    SUM(b.billing_amount) AS total_revenue
FROM patients p
INNER JOIN appointments a
    ON p.patient_id = a.patient_id
INNER JOIN billing b
    ON a.appointment_id = b.appointment_id
GROUP BY p.city
ORDER BY total_revenue DESC
LIMIT 1;


-- =====================================================
-- Q9. Doctors above average revenue
-- SUBQUERY
-- =====================================================

SELECT
    d.doctor_id,
    d.doctor_name,
    SUM(b.billing_amount) AS total_revenue
FROM doctors d
INNER JOIN appointment_services s
    ON d.doctor_id = s.doctor_id
INNER JOIN billing b
    ON s.appointment_id = b.appointment_id
GROUP BY
    d.doctor_id,
    d.doctor_name
HAVING SUM(b.billing_amount) >
(
    SELECT AVG(doctor_revenue)
    FROM
    (
        SELECT
            SUM(b2.billing_amount) AS doctor_revenue
        FROM appointment_services s2
        INNER JOIN billing b2
            ON s2.appointment_id = b2.appointment_id
        GROUP BY s2.doctor_id
    ) AS revenue_table
)
ORDER BY total_revenue DESC;


-- =====================================================
-- Q10. Patients with BOTH successful and failed payments
-- =====================================================

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name
FROM patients p
INNER JOIN appointments a
    ON p.patient_id = a.patient_id
INNER JOIN billing b
    ON a.appointment_id = b.appointment_id
GROUP BY
    p.patient_id,
    p.first_name,
    p.last_name
HAVING
    SUM(
        CASE
            WHEN b.payment_status = 'Successful'
            THEN 1
            ELSE 0
        END
    ) > 0
AND
    SUM(
        CASE
            WHEN b.payment_status = 'Failed'
            THEN 1
            ELSE 0
        END
    ) > 0;


-- =====================================================
-- Q11. Cancellation percentage
-- =====================================================

SELECT
    COUNT(
        CASE
            WHEN status = 'Cancelled'
            THEN 1
        END
    ) * 100.0 / COUNT(*) AS cancellation_percentage
FROM appointments;


-- =====================================================
-- Q12. Total appointments by status
-- =====================================================

SELECT
    status,
    COUNT(*) AS total_appointments
FROM appointments
GROUP BY status
ORDER BY total_appointments DESC;


-- =====================================================
-- Q13. Average consultation fee by specialization
-- AVG
-- =====================================================

SELECT
    specialization,
    AVG(consultation_fee) AS avg_consultation_fee
FROM doctors
GROUP BY specialization
ORDER BY avg_consultation_fee DESC;


-- =====================================================
-- Q14. Most expensive doctor consultation fee
-- MAX
-- =====================================================

SELECT
    doctor_id,
    doctor_name,
    consultation_fee
FROM doctors
WHERE consultation_fee =
(
    SELECT MAX(consultation_fee)
    FROM doctors
);


-- =====================================================
-- Q15. Minimum, maximum and average billing amount
-- MIN / MAX / AVG
-- =====================================================

SELECT
    MIN(billing_amount) AS minimum_bill,
    MAX(billing_amount) AS maximum_bill,
    AVG(billing_amount) AS average_bill
FROM billing;


-- =====================================================
-- Q16. Monthly revenue
-- =====================================================

SELECT
    DATE_FORMAT(transaction_date, '%Y-%m') AS month,
    SUM(billing_amount) AS monthly_revenue
FROM billing
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month;


-- =====================================================
-- Q17. Doctor-wise appointment count and revenue
-- Multi-table JOIN
-- =====================================================

SELECT
    d.doctor_id,
    d.doctor_name,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COALESCE(SUM(b.billing_amount), 0) AS total_revenue
FROM doctors d
LEFT JOIN appointments a
    ON d.doctor_id = a.doctor_id
LEFT JOIN billing b
    ON a.appointment_id = b.appointment_id
GROUP BY
    d.doctor_id,
    d.doctor_name
ORDER BY total_revenue DESC;


-- =====================================================
-- Q18. Service popularity
-- =====================================================

SELECT
    service_name,
    COUNT(*) AS times_used,
    SUM(quantity) AS total_quantity
FROM appointment_services
GROUP BY service_name
ORDER BY times_used DESC
LIMIT 10;