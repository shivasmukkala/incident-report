from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Case
from app.schemas.case import CaseCreate, CaseResponse


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.post(
    "/",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
):
    new_case = Case(
        title=case_data.title,
        description=case_data.description,
        category=case_data.category,
        incident_datetime=case_data.incident_datetime,
        perceived_urgency=case_data.perceived_urgency,
        location_description=case_data.location_description,
        location_precision=case_data.location_precision,
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case


@router.get("/", response_model=list[CaseResponse])
def get_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).all()
    return cases


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    existing_case = db.get(Case, case_id)

    if existing_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return existing_case
