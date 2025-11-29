from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "name": "Test User", "role": "patient"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user(client: TestClient):
    # Register first
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123", "name": "Login User", "role": "patient"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
