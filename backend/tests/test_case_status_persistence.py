import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models import Case, CaseStatusHistory
from app.core.case_status import CaseStatus
from app.services.case_service import change_case_status


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSession = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSession()

    yield session

    session.close()
    engine.dispose()


def test_status_change_saves_case_and_history(db_session):
    case = Case(
        title="Test incident",
        description="Testing status history.",
    )

    db_session.add(case)
    db_session.commit()

    updated_case = change_case_status(
        db=db_session,
        case_id=case.id,
        new_status=CaseStatus.UNDER_REVIEW,
        reason="Initial triage",
        authorised=True,
    )

    history = db_session.query(CaseStatusHistory).first()

    assert updated_case.status == "under_review"
    assert history is not None
    assert history.previous_status == "submitted"
    assert history.new_status == "under_review"
    assert history.reason == "Initial triage"
    assert history.created_at is not None


def test_status_change_rejects_missing_case(db_session):
    with pytest.raises(LookupError, match="Case not found"):
        change_case_status(
            db=db_session,
            case_id=999,
            new_status=CaseStatus.UNDER_REVIEW,
            authorised=True,
        )
