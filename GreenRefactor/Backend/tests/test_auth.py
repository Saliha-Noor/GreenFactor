import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend modules can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from api import app
import db

@pytest.fixture(scope="module")
def client():
    # Initialize DB (which also creates the seed dev user)
    db.init_db()
    # Clean up any leftover test data from previous runs
    with db.get_connection() as conn:
        conn.execute("DELETE FROM users WHERE email = 'test@example.com'")
        conn.execute("DELETE FROM sessions WHERE email = 'test@example.com'")
        conn.commit()
        
    with TestClient(app) as c:
        yield c

def test_signup_success(client):
    # test signup succeeds, returns a token
    response = client.post("/api/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "institution": "Test Inst"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

def test_signup_duplicate(client):
    # duplicate signup (same email) returns 409
    response = client.post("/api/auth/signup", json={
        "name": "Test User 2",
        "email": "test@example.com",
        "password": "password123",
        "institution": "Test Inst"
    })
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_login_success(client):
    # login with correct password succeeds
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

def test_login_wrong_password(client):
    # wrong password returns 401
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_get_user_invalid_token(client):
    # an expired/invalid session token on /api/user returns 401
    response = client.get("/api/user", headers={"Authorization": "Bearer invalid_or_expired_token_12345"})
    assert response.status_code == 401
    assert "Session expired or invalid" in response.json()["detail"]

def test_persistence_across_connections():
    # a fresh db.py connection (simulating a server restart) can still find the user
    # this is the actual regression test for "in-memory dict -> SQLite"
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        assert user is not None
        assert dict(user)["email"] == "test@example.com"
