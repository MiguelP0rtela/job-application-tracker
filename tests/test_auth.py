from jose import jwt
from starlette import status

from app.core.config import settings
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
        data={
            "username": "test@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    payload = jwt.decode(
        data["access_token"],
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    assert payload["sub"] == user.email
    assert "exp" in payload


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
        data={
            "username": "test2@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."


def test_login_nonexistent_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."
