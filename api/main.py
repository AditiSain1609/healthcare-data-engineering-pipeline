from fastapi import FastAPI

from api.routes import patients, doctors, appointments, billing, analytics

app = FastAPI(
    title="Healthcare Data Engineering API",
    description="REST API for the Healthcare Data Engineering & Analytics Platform",
    version="1.0.0",
)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(billing.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {
        "message": "Healthcare Data Engineering API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }