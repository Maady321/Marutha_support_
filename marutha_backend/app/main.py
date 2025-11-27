from fastapi import FastAPI

from app.routers import auth, users, doctors, patients, consultations
from app.routers import appointments
from app.routers import volunteers
from app.routers import medications
app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(consultations.router)
app.include_router(appointments.router)
app.include_router(volunteers.router)
app.include_router(medications.router)

@app.get("/")
def root():
    return {"message": "Marutha backend working"}
