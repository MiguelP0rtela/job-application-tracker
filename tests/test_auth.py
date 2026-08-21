from app.core.security import hash_password
from app.models.user import User


def test_login_success(client, db):
    user = User(
        username="testuser",
        email="test@example.com",
        password=hash_password("Password123!"),
        name="Test User",
        phone_number="910000000",
        role="candidate",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/login",
        params={
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["user_id"] == user.id


def test_login_wrong_password(client, db):
    user = User(
        username="testuser2",
        email="test2@example.com",
        password=hash_password("Password123!"),
        name="Test User",
        phone_number="910000001",
        role="candidate",
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        params={
            "email": "test2@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_nonexistent_email(client):
    response = client.post(
        "/auth/login",
        params={
            "email": "doesnotexist@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."