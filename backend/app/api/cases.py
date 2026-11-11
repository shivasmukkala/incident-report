from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
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
            status_code=404,
            detail="Case not found",
        )

    return existing_case
