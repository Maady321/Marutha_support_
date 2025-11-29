from fastapi.testclient import TestClient
from datetime import datetime

def test_create_consultation(client: TestClient):
    # Setup: Admin, Doctor, Patient
    client.post("/auth/register", json={"email": "admin_cons@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin_cons@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Doctor User & Profile
    doc_user = client.post("/users/", json={"email": "doc_cons@example.com", "password": "password", "name": "Dr. Cons", "role": "doctor"}, headers=headers).json()
    client.post("/doctors/", json={"user_id": doc_user["id"], "specialization": "General", "license_number": "LIC1", "years_of_experience": 5, "education": "Med School", "bio": "Bio"}, headers=headers).json()
    doc_id = client.get(f"/doctors/?user_id={doc_user['id']}", headers=headers).json()[0]["id"] # Assuming list returns doctors and we can filter or just pick first

    # Create Patient User & Record
    pat_user = client.post("/users/", json={"email": "pat_cons@example.com", "password": "password", "name": "Pat Cons", "role": "patient"}, headers=headers).json()
    pat_id = client.post("/patients/", json={"user_id": pat_user["id"], "medical_history": "None", "dob": "1990-01-01", "gender": "Male", "address": "Addr"}, headers=headers).json()["id"]

    # Create Consultation
    cons_payload = {
        "patient_id": pat_id,
        "doctor_id": doc_id,
        "scheduled_time": datetime.now().isoformat(),
        "reason": "Checkup"
    }
    response = client.post("/consultations/", json=cons_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["reason"] == "Checkup"
