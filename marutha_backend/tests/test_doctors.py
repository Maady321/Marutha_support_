from fastapi.testclient import TestClient

def test_create_doctor(client: TestClient):
    # 1. Create Admin
    client.post("/auth/register", json={"email": "admin_doc@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin_doc@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create User for Doctor
    user_res = client.post("/users/", json={"email": "doctor@example.com", "password": "password", "name": "Dr. House", "role": "doctor"}, headers=headers)
    user_id = user_res.json()["id"]

    # 3. Create Doctor Profile
    doc_payload = {
        "user_id": user_id,
        "specialization": "Diagnostician",
        "license_number": "MD12345",
        "years_of_experience": 15,
        "education": "Johns Hopkins",
        "bio": "It's never lupus."
    }
    response = client.post("/doctors/", json=doc_payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["specialization"] == "Diagnostician"
    assert data["user_id"] == user_id

def test_list_doctors(client: TestClient):
    # Just need any auth
    client.post("/auth/register", json={"email": "patient_doc@example.com", "password": "password", "name": "Patient", "role": "patient"})
    login_res = client.post("/auth/login", json={"email": "patient_doc@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/doctors/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
