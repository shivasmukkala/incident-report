from app.core.case_status import CaseStatus


ALLOWED_TRANSITIONS = {
    CaseStatus.SUBMITTED: {
        CaseStatus.UNDER_REVIEW,
    },
    CaseStatus.UNDER_REVIEW: {
        CaseStatus.INVESTIGATING,
        CaseStatus.CLOSED,
    },
    CaseStatus.INVESTIGATING: {
        CaseStatus.ACTION_IN_PROGRESS,
    },
    CaseStatus.ACTION_IN_PROGRESS: {
        CaseStatus.RESOLVED,
    },
    CaseStatus.RESOLVED: {
        CaseStatus.VERIFIED,
    },
    CaseStatus.VERIFIED: {
        CaseStatus.CLOSED,
    },
    CaseStatus.CLOSED: set(),
}


def can_transition(
    current_status: CaseStatus,
    new_status: CaseStatus,
) -> bool:
    return new_status in ALLOWED_TRANSITIONS.get(
        current_status,
        set(),
    )
