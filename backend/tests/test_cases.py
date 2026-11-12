import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db



@pytest.fixture
def client():
    # Create a separate in-memory database for testing.
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

    # Create the database tables.
    Base.metadata.create_all(bind=test_engine)

    # Override the application's database dependency.
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up after testing.
    app.dependency_overrides.clear()
    test_engine.dispose()

def test_get_existing_case(client):
    create_response = client.post(
        "/cases/",
        json={
            "title": "Retrieval test case",
            "description": "Testing retrieval of an existing case.",
        },
    )

    case_id = create_response.json()["id"]

    response = client.get(f"/cases/{case_id}")

    assert response.status_code == 200
    assert response.json()["id"] == case_id
    assert response.json()["title"] == "Retrieval test case"


def test_get_nonexistent_case(client):
    response = client.get("/cases/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"

def test_create_case_successfully(client):
    response = client.post(
        "/cases/",
        json={
            "title": "Test safety concern",
            "description": "A loose cable was identified near the entrance.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Test safety concern"
    assert data["status"] == "submitted"


def test_create_case_without_title(client):
    response = client.post(
        "/cases/",
        json={
            "description": "A loose cable was identified near the entrance.",
        },
    )

    assert response.status_code == 422


def test_create_case_without_description(client):
    response = client.post(
        "/cases/",
        json={
            "title": "Test safety concern",
        },
    )

    assert response.status_code == 422

def test_get_cases_empty_list(client):
    response = client.get("/cases/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_cases_returns_created_cases(client):
    client.post(
        "/cases/",
        json={
            "title": "First safety concern",
            "description": "A loose cable near the entrance.",
        },
    )

    client.post(
        "/cases/",
        json={
            "title": "Second safety concern",
            "description": "A damaged handrail near the stairs.",
        },
    )

    response = client.get("/cases/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "First safety concern"

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_case_with_all_incident_fields(client):
    response = client.post(
        "/cases/",
        json={
            "title": "Slip incident near entrance",
            "description": "A visitor slipped near the main entrance.",
            "category": "slip_trip",
            "incident_datetime": "2026-11-10T09:30:00",
            "perceived_urgency": "high",
            "location_description": "Near the main entrance",
            "location_precision": "approximate",
        },
    )

    assert response.status_code == 201

    created_case = response.json()
    case_id = created_case["id"]

    # Retrieve the saved case from the database.
    get_response = client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["category"] == "slip_trip"
    assert data["incident_datetime"] == "2026-11-10T09:30:00"
    assert data["perceived_urgency"] == "high"
    assert data["location_description"] == "Near the main entrance"
    assert data["location_precision"] == "approximate"
