import pytest

from fastapi import HTTPException

from app.api.dependencies import require_roles
from app.core.roles import (
    REPORTER,
    CASE_HANDLER,
    MANAGER,
    ADMIN,
    ALL_ROLES,
)
from app.models import User


def make_user(role):
    return User(
        id=1,
        name="Test User",
        email="test@example.com",
        hashed_password="test-hash",
        role=role,
        is_active=True,
    )


def test_all_four_roles_are_defined():
    assert ALL_ROLES == {
        REPORTER,
        CASE_HANDLER,
        MANAGER,
        ADMIN,
    }


@pytest.mark.parametrize(
    "role",
    [REPORTER, CASE_HANDLER, MANAGER, ADMIN],
)
def test_allowed_role_is_accepted(role):
    user = make_user(role)
    checker = require_roles(role)

    assert checker(current_user=user) is user


def test_disallowed_role_is_rejected():
    user = make_user(REPORTER)
    checker = require_roles(ADMIN)

    with pytest.raises(HTTPException) as exc:
        checker(current_user=user)

    assert exc.value.status_code == 403


def test_multiple_allowed_roles():
    user = make_user(CASE_HANDLER)
    checker = require_roles(CASE_HANDLER, MANAGER)

    assert checker(current_user=user) is user
