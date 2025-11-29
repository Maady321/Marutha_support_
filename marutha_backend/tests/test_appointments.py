from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_appointment(client: TestClient):
    # Setup: Admin, Doctor, Patient
    client.post("/auth/register", json={"email": "admin_appt@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin_appt@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Doctor
    doc_user = client.post("/users/", json={"email": "doc_appt@example.com", "password": "password", "name": "Dr. Appt", "role": "doctor"}, headers=headers).json()
    client.post("/doctors/", json={"user_id": doc_user["id"], "specialization": "General", "license_number": "LIC2", "years_of_experience": 5, "education": "Med School", "bio": "Bio"}, headers=headers).json()
    doc_id = client.get(f"/doctors/?user_id={doc_user['id']}", headers=headers).json()[0]["id"]

    # Create Patient
    pat_user = client.post("/users/", json={"email": "pat_appt@example.com", "password": "password", "name": "Pat Appt", "role": "patient"}, headers=headers).json()
    pat_id = client.post("/patients/", json={"user_id": pat_user["id"], "medical_history": "None", "dob": "1990-01-01", "gender": "Male", "address": "Addr"}, headers=headers).json()["id"]

    # Create Appointment
    start = datetime.now() + timedelta(days=1)
    end = start + timedelta(hours=1)
    appt_payload = {
        "patient_id": pat_id,
        "doctor_id": doc_id,
        "datetime_start": start.isoformat(),
        "datetime_end": end.isoformat(),
        "visit_type": "in_person",
        "reason": "Checkup"
    }
    response = client.post("/appointments/", json=appt_payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["reason"] == "Checkup"
