from app.core.case_status import CaseStatus
from app.core.case_transitions import can_transition


def test_normal_lifecycle_transitions():
    assert can_transition(
        CaseStatus.SUBMITTED,
        CaseStatus.UNDER_REVIEW,
    )

    assert can_transition(
        CaseStatus.UNDER_REVIEW,
        CaseStatus.INVESTIGATING,
    )

    assert can_transition(
        CaseStatus.INVESTIGATING,
        CaseStatus.ACTION_IN_PROGRESS,
    )

    assert can_transition(
        CaseStatus.ACTION_IN_PROGRESS,
        CaseStatus.RESOLVED,
    )

    assert can_transition(
        CaseStatus.RESOLVED,
        CaseStatus.VERIFIED,
    )

    assert can_transition(
        CaseStatus.VERIFIED,
        CaseStatus.CLOSED,
    )


def test_direct_closure_from_under_review():
    assert can_transition(
        CaseStatus.UNDER_REVIEW,
        CaseStatus.CLOSED,
    )


def test_invalid_transitions_are_rejected():
    assert not can_transition(
        CaseStatus.SUBMITTED,
        CaseStatus.CLOSED,
    )

    assert not can_transition(
        CaseStatus.CLOSED,
        CaseStatus.INVESTIGATING,
    )

    assert not can_transition(
        CaseStatus.RESOLVED,
        CaseStatus.CLOSED,
    )
