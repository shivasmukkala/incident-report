from app.core.security import hash_password
from app.core.tokens import create_access_token
from app.models import User


def create_test_user(test_db, email="admin@example.com", active=True):
    db = test_db()
    user = User(
        name="Test Administrator",
        email=email,
        hashed_password=hash_password("TestPassword123!"),
        role="admin",
        is_active=active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return user_id


def test_login_success(client, test_db):
    create_test_user(test_db)

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_accepts_uppercase_email(client, test_db):
    create_test_user(test_db)

    response = client.post(
        "/auth/login",
        json={
            "email": "ADMIN@EXAMPLE.COM",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200


def test_login_rejects_wrong_password(client, test_db):
    create_test_user(test_db)

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_login_rejects_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401


def test_login_rejects_inactive_user(client, test_db):
    create_test_user(test_db, active=False)

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_rejects_missing_token(client):
    response = client.get("/cases/")

    assert response.status_code == 401


def test_protected_endpoint_rejects_invalid_token(client):
    client.headers.update({
        "Authorization": "Bearer invalid-token"
    })

    response = client.get("/cases/")

    assert response.status_code == 401


def test_protected_endpoint_rejects_inactive_user_token(
    client, test_db
):
    user_id = create_test_user(test_db, active=False)
    token = create_access_token(user_id=user_id, role="admin")

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    response = client.get("/cases/")

    assert response.status_code == 401
