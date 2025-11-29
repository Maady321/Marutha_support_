from fastapi.testclient import TestClient

def test_read_users_unauthorized(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 401

def test_create_user_admin(client: TestClient):
    # Create admin
    client.post("/auth/register", json={"email": "admin@example.com", "password": "password", "name": "Admin", "role": "admin"})
    login_res = client.post("/auth/login", json={"email": "admin@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/users/", json={"email": "newuser@example.com", "password": "password", "name": "New User", "role": "patient"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"

def test_read_me(client: TestClient):
    # Register and login
    client.post("/auth/register", json={"email": "me@example.com", "password": "password", "name": "Me", "role": "patient"})
    login_res = client.post("/auth/login", json={"email": "me@example.com", "password": "password"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
