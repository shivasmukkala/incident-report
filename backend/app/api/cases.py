from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    get_optional_current_user,
    require_roles,
)
from app.core.roles import (
    REPORTER,
    CASE_HANDLER,
    MANAGER,
)
from app.db.session import get_db
from app.models import Case, User
from app.schemas.case import (
     CaseCreate,
     CaseResponse,
     CaseAssignRequest,
     CaseAssignmentResponse,
)
from app.services.case_service import assign_case as assign_case_service

router = APIRouter(prefix="/cases", tags=["Cases"])


def get_case_query(db: Session, current_user: User):
    query = db.query(Case)

    if current_user.role == MANAGER:
        return query

    if current_user.role == REPORTER:
        return query.filter(
            Case.reporter_user_id == current_user.id
        )

    if current_user.role == CASE_HANDLER:
        return query.filter(
            Case.assigned_to_user_id == current_user.id
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access cases",
    )


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    new_case = Case(
        title=case_data.title,
        description=case_data.description,
        category=case_data.category,
        incident_datetime=case_data.incident_datetime,
        perceived_urgency=case_data.perceived_urgency,
        location_description=case_data.location_description,
        location_precision=case_data.location_precision,
        reporter_user_id=current_user.id if current_user else None,
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case


@router.get("/", response_model=list[CaseResponse])
def get_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_case_query(db, current_user).all()


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_case = get_case_query(
        db, current_user
    ).filter(Case.id == case_id).first()

    if existing_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return existing_case
@router.put(
    "/{case_id}/assign",
    response_model=CaseAssignmentResponse,
)
def assign_case_endpoint(
    case_id: int,
    assignment_data: CaseAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(MANAGER)),
):
    try:
        assigned_case = assign_case_service(
            db=db,
            case_id=case_id,
            assignee_id=assignment_data.assigned_to_user_id,
            assigned_by=current_user,
            reason=assignment_data.reason,
        )

        return CaseAssignmentResponse(
            case_id=assigned_case.id,
            assigned_to_user_id=assigned_case.assigned_to_user_id,
            message="Case assigned successfully.",
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        )
