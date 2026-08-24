from jose import jwt
from starlette import status

from app.core.config import settings
from app.core.security import hash_password, create_access_token
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


def test_get_current_user(client, db):
    user = User(
        username="currentuser",
        email="current@example.com",
        password=hash_password("Password123!"),
        name="Current User",
        phone_number="910000002",
        role="candidate",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "current@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["name"] == user.name
    assert "password" not in data


def test_get_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"


def test_get_current_user_token_without_sub(client):
    token = create_access_token(
        data={"something": "else"}
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"


def test_get_current_user_nonexistent_user(client):
    token = create_access_token(
        data={"sub": "nonexistent@example.com"}
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"

def test_admin_route_without_token(client):
    response = client.get("/users/admin")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_route_as_candidate(client, db):
    user = User(
        username="candidateadmin",
        email="candidateadmin@example.com",
        password=hash_password("Password123!"),
        name="Candidate Admin",
        phone_number="910000003",
        role="candidate",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "candidateadmin@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Admin privileges required."


def test_admin_route_as_admin(client, db):
    user = User(
        username="adminuser",
        email="admin@example.com",
        password=hash_password("Password123!"),
        name="Admin User",
        phone_number="910000004",
        role="admin",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == status.HTTP_200_OK

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == user.id
    assert data["email"] == user.email
    assert data["role"] == "admin"
    assert "password" not in data