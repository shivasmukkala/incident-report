from app.core.security import hash_password
from app.models import Case, User
def test_get_existing_case(authenticated_client):
    create_response = authenticated_client.post(
        "/cases/",
        json={
            "title": "Retrieval test case",
            "description": "Testing retrieval of an existing case.",
        },
    )

    case_id = create_response.json()["id"]

    response = authenticated_client.get(f"/cases/{case_id}")

    assert response.status_code == 200
    assert response.json()["id"] == case_id
    assert response.json()["title"] == "Retrieval test case"
    assert response.json()["reference"] == create_response.json()["reference"]



def test_get_nonexistent_case(authenticated_client):
    response = authenticated_client.get("/cases/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"

def test_create_case_successfully(authenticated_client):
    response = authenticated_client.post(
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
    assert data["reference"].startswith("IR-")
    assert len(data["reference"]) == 19


def test_create_case_without_title(authenticated_client):
    response = authenticated_client.post(
        "/cases/",
        json={
            "description": "A loose cable was identified near the entrance.",
        },
    )

    assert response.status_code == 422


def test_create_case_without_description(authenticated_client):
    response = authenticated_client.post(
        "/cases/",
        json={
            "title": "Test safety concern",
        },
    )

    assert response.status_code == 422

def test_get_cases_empty_list(authenticated_client):
    response = authenticated_client.get("/cases/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_cases_returns_created_cases(authenticated_client):
    authenticated_client.post(
        "/cases/",
        json={
            "title": "First safety concern",
            "description": "A loose cable near the entrance.",
        },
    )

    authenticated_client.post(
        "/cases/",
        json={
            "title": "Second safety concern",
            "description": "A damaged handrail near the stairs.",
        },
    )

    response = authenticated_client.get("/cases/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "First safety concern"
    references = [case["reference"] for case in response.json()]

    assert len(set(references)) == 2
    assert all(reference.startswith("IR-") for reference in references)

def test_health_check(authenticated_client):
    response = authenticated_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_case_with_all_incident_fields(authenticated_client):
    response = authenticated_client.post(
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
    get_response = authenticated_client.get(f"/cases/{case_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["category"] == "slip_trip"
    assert data["incident_datetime"] == "2026-11-10T09:30:00"
    assert data["perceived_urgency"] == "high"
    assert data["location_description"] == "Near the main entrance"
def test_manager_can_list_all_cases(manager_client, test_db):
    db = test_db()

    try:
        reporter_one = User(
            name="Reporter One",
            email="one@example.com",
            hashed_password=hash_password("Password123!"),
            role="reporter",
            is_active=True,
        )

        reporter_two = User(
            name="Reporter Two",
            email="two@example.com",
            hashed_password=hash_password("Password123!"),
            role="reporter",
            is_active=True,
        )

        db.add_all([reporter_one, reporter_two])
        db.commit()
        db.refresh(reporter_one)
        db.refresh(reporter_two)

        db.add_all([
            Case(
                title="First case",
                description="First report",
                reporter_user_id=reporter_one.id,
            ),
            Case(
                title="Second case",
                description="Second report",
                reporter_user_id=reporter_two.id,
            ),
        ])
        db.commit()
    finally:
        db.close()

    response = manager_client.get("/cases/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_manager_can_retrieve_any_case(manager_client, test_db):
    db = test_db()

    try:
        reporter = User(
            name="Another Reporter",
            email="another@example.com",
            hashed_password=hash_password("Password123!"),
            role="reporter",
            is_active=True,
        )

        db.add(reporter)
        db.commit()
        db.refresh(reporter)

        case = Case(
            title="Restricted reporter case",
            description="Manager should be able to view this.",
            reporter_user_id=reporter.id,
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        case_id = case.id
    finally:
        db.close()

    response = manager_client.get(f"/cases/{case_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Restricted reporter case"



def test_anonymous_case_submission(client, test_db):
    response = client.post(
        "/cases/",
        json={
            "title": "Anonymous safety concern",
            "description": "A concern submitted without an account.",
        },
    )

    assert response.status_code == 201

    db = test_db()
    try:
        saved_case = db.get(Case, response.json()["id"])
        assert saved_case is not None
        assert saved_case.reporter_user_id is None
    finally:
        db.close()


def test_authenticated_case_submission_links_reporter(
    authenticated_client, test_db
):
    response = authenticated_client.post(
        "/cases/",
        json={
            "title": "Authenticated safety concern",
            "description": "A concern submitted by a logged-in user.",
        },
    )

    assert response.status_code == 201

    db = test_db()
    try:
        user = db.query(User).filter_by(
            email="reporter@example.com"
        ).first()

        saved_case = db.get(Case, response.json()["id"])

        assert saved_case is not None
        assert saved_case.reporter_user_id == user.id
    finally:
        db.close()


def test_reporter_can_only_list_own_cases(authenticated_client, test_db):
    own_response = authenticated_client.post(
        "/cases/",
        json={
            "title": "My safety concern",
            "description": "Submitted by the logged-in reporter.",
        },
    )
    assert own_response.status_code == 201

    db = test_db()
    try:
        other_user = User(
            name="Another Reporter",
            email="other@example.com",
            hashed_password=hash_password("OtherPassword123!"),
            role="reporter",
            is_active=True,
        )
        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        other_case = Case(
            title="Another person's concern",
            description="This belongs to another reporter.",
            reporter_user_id=other_user.id,
        )
        db.add(other_case)
        db.commit()
    finally:
        db.close()

    response = authenticated_client.get("/cases/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "My safety concern"


def test_reporter_cannot_retrieve_another_users_case(
    authenticated_client, test_db
):
    db = test_db()
    try:
        other_user = User(
            name="Another Reporter",
            email="other@example.com",
            hashed_password=hash_password("OtherPassword123!"),
            role="reporter",
            is_active=True,
        )
        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        other_case = Case(
            title="Private safety concern",
            description="Belongs to another reporter.",
            reporter_user_id=other_user.id,
        )
        db.add(other_case)
        db.commit()
        db.refresh(other_case)

        other_case_id = other_case.id
    finally:
        db.close()

    response = authenticated_client.get(f"/cases/{other_case_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"


def test_anonymous_user_cannot_list_cases(client):
    response = client.get("/cases/")

    assert response.status_code == 401


def test_anonymous_user_cannot_retrieve_case(client):
    response = client.get("/cases/1")

    assert response.status_code == 401


def test_invalid_token_cannot_submit_case(client):
    client.headers.update({"Authorization": "Bearer invalid-token"})

    response = client.post(
        "/cases/",
        json={
            "title": "Invalid token test",
            "description": "This submission must be rejected.",
        },
    )

    assert response.status_code == 401
def test_case_handler_can_list_only_assigned_cases(
    case_handler_client, test_db
):
    db = test_db()

    try:
        handler = db.query(User).filter_by(
            email="handler@example.com"
        ).first()

        other_handler = User(
            name="Other Handler",
            email="otherhandler@example.com",
            hashed_password=hash_password("OtherPassword123!"),
            role="case_handler",
            is_active=True,
        )

        db.add(other_handler)
        db.commit()
        db.refresh(other_handler)

        db.add_all([
            Case(
                title="Assigned case",
                description="Assigned to this handler.",
                assigned_to_user_id=handler.id,
            ),
            Case(
                title="Other handler case",
                description="Assigned to another handler.",
                assigned_to_user_id=other_handler.id,
            ),
            Case(
                title="Unassigned case",
                description="Not assigned to anyone.",
            ),
        ])

        db.commit()
    finally:
        db.close()

    response = case_handler_client.get("/cases/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Assigned case"


def test_case_handler_can_retrieve_assigned_case(
    case_handler_client, test_db
):
    db = test_db()

    try:
        handler = db.query(User).filter_by(
            email="handler@example.com"
        ).first()

        case = Case(
            title="Assigned investigation",
            description="This case belongs to the handler.",
            assigned_to_user_id=handler.id,
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        case_id = case.id
    finally:
        db.close()

    response = case_handler_client.get(f"/cases/{case_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Assigned investigation"


def test_case_handler_cannot_retrieve_unassigned_case(
    case_handler_client, test_db
):
    db = test_db()

    try:
        other_handler = User(
            name="Other Handler",
            email="otherhandler@example.com",
            hashed_password=hash_password("OtherPassword123!"),
            role="case_handler",
            is_active=True,
        )

        db.add(other_handler)
        db.commit()
        db.refresh(other_handler)

        case = Case(
            title="Another handler investigation",
            description="This case belongs to another handler.",
            assigned_to_user_id=other_handler.id,
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        case_id = case.id
    finally:
        db.close()

    response = case_handler_client.get(f"/cases/{case_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"
def test_admin_cannot_list_cases(admin_client):
    response = admin_client.get("/cases/")

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to access cases"
    )


def test_admin_cannot_retrieve_case(admin_client, test_db):
    db = test_db()

    try:
        case = Case(
            title="Confidential incident",
            description="Admin access must be denied by default.",
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        case_id = case.id
    finally:
        db.close()

    response = admin_client.get(f"/cases/{case_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to access cases"
    )
