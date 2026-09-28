from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String

from api.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(50))
    city = Column(String(100))
    date_of_birth = Column(Date)


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True)
    doctor_name = Column(String(255))
    specialization = Column(String(255))
    city = Column(String(100))
    consultation_fee = Column(Numeric(10, 2))


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    doctor_id = Column(Integer)
    appointment_date = Column(DateTime)
    appointment_type = Column(String(100))
    status = Column(String(100))


class AppointmentService(Base):
    __tablename__ = "appointment_services"

    service_id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer)
    doctor_id = Column(Integer)
    service_name = Column(String(255))
    duration_minutes = Column(Integer)
    quantity = Column(Integer)


class Billing(Base):
    __tablename__ = "billing"

    billing_id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer)
    billing_amount = Column(Numeric(12, 2))
    payment_type = Column(String(100))
    payment_status = Column(String(100))
    transaction_date = Column(DateTime)