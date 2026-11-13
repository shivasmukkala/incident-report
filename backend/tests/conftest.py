import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models import User
from app.core.security import hash_password


@pytest.fixture
def test_db():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    yield TestingSessionLocal

    test_engine.dispose()


@pytest.fixture
def client(test_db):
    def override_get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
@pytest.fixture
def manager_client(client, test_db):
    db = test_db()

    user = User(
        name="Test Manager",
        email="manager@example.com",
        hashed_password=hash_password("ManagerPassword123!"),
        role="manager",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "email": "manager@example.com",
            "password": "ManagerPassword123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })
    return client

@pytest.fixture
def admin_client(client, test_db):
    db = test_db()

    user = User(
        name="Test Admin",
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123!"),
        role="admin",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "AdminPassword123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


@pytest.fixture
def case_handler_client(client, test_db):
    db = test_db()

    user = User(
        name="Test Case Handler",
        email="handler@example.com",
        hashed_password=hash_password("HandlerPassword123!"),
        role="case_handler",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "email": "handler@example.com",
            "password": "HandlerPassword123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client

@pytest.fixture
def authenticated_client(client, test_db):
    db = test_db()

    user = User(
        name="Test Reporter",
        email="reporter@example.com",
        hashed_password=hash_password("TestPassword123!"),
        role="reporter",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "email": "reporter@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client
