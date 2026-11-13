from sqlalchemy.orm import Session
from app.core.roles import CASE_HANDLER, MANAGER
from app.models import CaseAssignmentHistory, User
from app.core.case_status import CaseStatus
from app.core.case_transitions import can_transition
from app.models import Case, CaseStatusHistory


def validate_case_transition(
    current_status: CaseStatus,
    new_status: CaseStatus,
    closure_reason: str | None = None,
    authorised: bool = False,
) -> None:
    if not authorised:
        raise PermissionError(
            "You are not authorised to change this case status."
        )

    if not can_transition(current_status, new_status):
        raise ValueError(
            f"Transition from {current_status.value} "
            f"to {new_status.value} is not permitted."
        )

    if new_status == CaseStatus.CLOSED:
        if not closure_reason or not closure_reason.strip():
            raise ValueError(
                "A closure reason is required when closing a case."
            )


def change_case_status(
    db: Session,
    case_id: int,
    new_status: CaseStatus,
    reason: str | None = None,
    changed_by: int | None = None,
    authorised: bool = False,
) -> Case:

    # 1. Find the existing case.
    existing_case = db.get(Case, case_id)

    if existing_case is None:
        raise LookupError("Case not found.")

    # 2. Validate the requested transition.
    current_status = CaseStatus(existing_case.status)

    validate_case_transition(
        current_status=current_status,
        new_status=new_status,
        closure_reason=reason,
        authorised=authorised,
    )

    # 3. Prepare the history record.
    history_record = CaseStatusHistory(
        case_id=existing_case.id,
        previous_status=current_status.value,
        new_status=new_status.value,
        reason=reason,
        changed_by=changed_by,
    )

    try:
        # 4. Update the case.
        existing_case.status = new_status.value

        # 5. Save the history record.
        db.add(history_record)

        # 6. Save both changes in one transaction.
        db.commit()
        db.refresh(existing_case)

        return existing_case

    except Exception:
        db.rollback()
        raise

def assign_case(
    db: Session,
    case_id: int,
    assignee_id: int,
    assigned_by: User,
    reason: str | None = None,
) -> Case:

    if assigned_by.role != MANAGER:
        raise PermissionError(
            "Only managers can assign cases."
        )

    # 1. Find the case.
    existing_case = db.get(Case, case_id)

    if existing_case is None:
        raise LookupError("Case not found.")

    # 2. Find the proposed assignee.
    assignee = db.get(User, assignee_id)

    if assignee is None:
        raise LookupError("Assigned user not found.")

    # 3. Validate the proposed assignee.
    if assignee.role != CASE_HANDLER or not assignee.is_active:
        raise ValueError(
            "Cases can only be assigned to active case handlers."
        )

    # 4. Prevent duplicate assignments.
    if existing_case.assigned_to_user_id == assignee.id:
        raise ValueError(
            "Case is already assigned to this handler."
        )

    # 5. Record the assignment history.
    history_record = CaseAssignmentHistory(
        case_id=existing_case.id,
        previous_assignee_id=existing_case.assigned_to_user_id,
        new_assignee_id=assignee.id,
        assigned_by=assigned_by.id,
        reason=reason,
    )

    # 6. Save assignment and history atomically.
    try:
        existing_case.assigned_to_user_id = assignee.id
        db.add(history_record)
        db.commit()
        db.refresh(existing_case)

        return existing_case

    except Exception:
        db.rollback()
        raise
