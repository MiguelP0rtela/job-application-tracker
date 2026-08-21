from fastapi import status


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "miguel",
            "email": "miguel@example.com",
            "password": "Password123!",
            "name": "Miguel Portela",
            "phone_number": "912345678",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["username"] == "miguel"
    assert data["email"] == "miguel@example.com"
    assert data["name"] == "Miguel Portela"
    assert data["role"] == "candidate"


def test_create_user_invalid_password(client):
    response = client.post(
        "/users/",
        json={
            "username": "miguel",
            "email": "miguel@example.com",
            "password": "abc",
            "name": "Miguel Portela",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_invalid_email(client):
    response = client.post(
        "/users/",
        json={
            "username": "miguel",
            "email": "isto-nao-e-um-email",
            "password": "Password123!",
            "name": "Miguel Portela",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_duplicate_username(client):
    user = {
        "username": "miguel",
        "email": "miguel@example.com",
        "password": "Password123!",
        "name": "Miguel Portela",
    }

    first_response = client.post("/users/", json=user)

    assert first_response.status_code == status.HTTP_201_CREATED

    duplicate_user = {
        "username": "miguel",
        "email": "outro@example.com",
        "password": "Password123!",
        "name": "Outro User",
    }

    second_response = client.post(
        "/users/",
        json=duplicate_user,
    )

    assert second_response.status_code == status.HTTP_409_CONFLICT


def test_create_user_duplicate_email(client):
    user = {
        "username": "miguel",
        "email": "miguel@example.com",
        "password": "Password123!",
        "name": "Miguel Portela",
    }

    first_response = client.post("/users/", json=user)

    assert first_response.status_code == status.HTTP_201_CREATED

    duplicate_user = {
        "username": "outro",
        "email": "miguel@example.com",
        "password": "Password123!",
        "name": "Outro User",
    }

    second_response = client.post(
        "/users/",
        json=duplicate_user,
    )

    assert second_response.status_code == status.HTTP_409_CONFLICT


def test_password_is_hashed(client, db):
    password = "Password123!"

    response = client.post(
        "/users/",
        json={
            "username": "miguel",
            "email": "miguel@example.com",
            "password": password,
            "name": "Miguel Portela",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    from app.models.user import User

    user = db.query(User).filter(
        User.email == "miguel@example.com"
    ).first()

    assert user is not None
    assert user.password != password
