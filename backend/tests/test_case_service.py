import pytest

from app.core.case_status import CaseStatus
from app.core.roles import MANAGER, CASE_HANDLER, REPORTER
from app.models import Case, User, CaseAssignmentHistory
from app.services.case_service import (
    validate_case_transition,
    assign_case,
)
from app.core.security import hash_password

def test_authorised_transition_is_valid():
    validate_case_transition(
        CaseStatus.SUBMITTED,
        CaseStatus.UNDER_REVIEW,
        authorised=True,
    )


def test_unauthorised_transition_is_rejected():
    with pytest.raises(PermissionError):
        validate_case_transition(
            CaseStatus.SUBMITTED,
            CaseStatus.UNDER_REVIEW,
            authorised=False,
        )


def test_closure_requires_reason():
    with pytest.raises(ValueError, match="closure reason"):
        validate_case_transition(
            CaseStatus.UNDER_REVIEW,
            CaseStatus.CLOSED,
            authorised=True,
        )


def test_closure_rejects_blank_reason():
    with pytest.raises(ValueError, match="closure reason"):
        validate_case_transition(
            CaseStatus.UNDER_REVIEW,
            CaseStatus.CLOSED,
            closure_reason="   ",
            authorised=True,
        )


def test_closure_with_reason_is_valid():
    validate_case_transition(
        CaseStatus.UNDER_REVIEW,
        CaseStatus.CLOSED,
        closure_reason="Duplicate report",
        authorised=True,
    )


def test_invalid_transition_is_rejected():
    with pytest.raises(ValueError, match="not permitted"):
        validate_case_transition(
            CaseStatus.SUBMITTED,
            CaseStatus.CLOSED,
            closure_reason="Not eligible for investigation",
            authorised=True,
        )

def create_user(db, name, email, role, is_active=True):
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password("TestPassword123!"),
        role=role,
        is_active=is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_case(db):
    case = Case(
        title="Test incident",
        description="Test incident description",
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def test_manager_can_assign_active_case_handler(test_db):
    db = test_db()

    manager = create_user(
        db, "Manager", "manager@test.com", MANAGER
    )
    handler = create_user(
        db, "Handler", "handler@test.com", CASE_HANDLER
    )
    case = create_case(db)

    result = assign_case(
        db, case.id, handler.id, manager, "Initial assignment"
    )

    assert result.assigned_to_user_id == handler.id

    history = db.query(CaseAssignmentHistory).all()
    assert len(history) == 1
    assert history[0].previous_assignee_id is None
    assert history[0].new_assignee_id == handler.id
    assert history[0].assigned_by == manager.id

    db.close()


def test_manager_can_reassign_case_and_history_is_preserved(test_db):
    db = test_db()

    manager = create_user(
        db, "Manager", "manager@test.com", MANAGER
    )
    first_handler = create_user(
        db, "Handler One", "handler1@test.com", CASE_HANDLER
    )
    second_handler = create_user(
        db, "Handler Two", "handler2@test.com", CASE_HANDLER
    )
    case = create_case(db)

    assign_case(db, case.id, first_handler.id, manager)
    result = assign_case(db, case.id, second_handler.id, manager)

    assert result.assigned_to_user_id == second_handler.id

    history = (
        db.query(CaseAssignmentHistory)
        .filter(CaseAssignmentHistory.case_id == case.id)
        .order_by(CaseAssignmentHistory.id)
        .all()
    )

    assert len(history) == 2
    assert history[1].previous_assignee_id == first_handler.id
    assert history[1].new_assignee_id == second_handler.id

    db.close()


def test_non_manager_cannot_assign_case(test_db):
    db = test_db()

    reporter = create_user(
        db, "Reporter", "reporter@test.com", REPORTER
    )
    handler = create_user(
        db, "Handler", "handler@test.com", CASE_HANDLER
    )
    case = create_case(db)

    with pytest.raises(PermissionError):
        assign_case(db, case.id, handler.id, reporter)

    assert db.get(Case, case.id).assigned_to_user_id is None
    assert db.query(CaseAssignmentHistory).count() == 0

    db.close()


def test_inactive_handler_cannot_be_assigned(test_db):
    db = test_db()

    manager = create_user(
        db, "Manager", "manager@test.com", MANAGER
    )
    handler = create_user(
        db, "Inactive Handler", "inactive@test.com",
        CASE_HANDLER, is_active=False
    )
    case = create_case(db)

    with pytest.raises(ValueError, match="active case handlers"):
        assign_case(db, case.id, handler.id, manager)

    assert db.get(Case, case.id).assigned_to_user_id is None
    assert db.query(CaseAssignmentHistory).count() == 0

    db.close()


def test_reporter_cannot_be_assigned_as_handler(test_db):
    db = test_db()

    manager = create_user(
        db, "Manager", "manager@test.com", MANAGER
    )
    reporter = create_user(
        db, "Reporter", "reporter@test.com", REPORTER
    )
    case = create_case(db)

    with pytest.raises(ValueError, match="active case handlers"):
        assign_case(db, case.id, reporter.id, manager)

    assert db.query(CaseAssignmentHistory).count() == 0

    db.close()


def test_same_handler_cannot_be_assigned_twice(test_db):
    db = test_db()

    manager = create_user(
        db, "Manager", "manager@test.com", MANAGER
    )
    handler = create_user(
        db, "Handler", "handler@test.com", CASE_HANDLER
    )
    case = create_case(db)

    assign_case(db, case.id, handler.id, manager)

    with pytest.raises(ValueError, match="already assigned"):
        assign_case(db, case.id, handler.id, manager)

    assert db.query(CaseAssignmentHistory).count() == 1

    db.close()
