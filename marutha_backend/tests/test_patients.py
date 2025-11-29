from fastapi.testclient import TestClient
from datetime import date

def test_create_patient(client: TestClient):
    # 1. Create Admin
    client.post("/auth/register", json={"email": "admin_pat@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin_pat@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create User for Patient
    user_res = client.post("/users/", json={"email": "patient@example.com", "password": "password", "name": "John Doe", "role": "patient"}, headers=headers)
    user_id = user_res.json()["id"]

    # 3. Create Patient Record
    pat_payload = {
        "user_id": user_id,
        "medical_history": "None",
        "dob": "1990-01-01",
        "gender": "Male",
        "address": "123 Main St"
    }
    response = client.post("/patients/", json=pat_payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["medical_history"] == "None"

def test_add_stage(client: TestClient):
    # Setup: Admin, User, Patient
    client.post("/auth/register", json={"email": "admin_stage@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin_stage@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    user_res = client.post("/users/", json={"email": "patient_stage@example.com", "password": "password", "name": "Jane Doe", "role": "patient"}, headers=headers)
    user_id = user_res.json()["id"]
    
    pat_res = client.post("/patients/", json={"user_id": user_id, "medical_history": "None", "dob": "1990-01-01", "gender": "Female", "address": "456 St"}, headers=headers)
    patient_id = pat_res.json()["id"]

    # Add Stage
    stage_payload = {
        "stage_name": "Stage 1",
        "notes": "Initial diagnosis"
    }
    response = client.post(f"/patients/{patient_id}/stages", json=stage_payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["stage_name"] == "Stage 1"
