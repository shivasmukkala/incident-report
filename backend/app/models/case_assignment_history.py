from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CaseAssignmentHistory(Base):
    __tablename__ = "case_assignment_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    case_id: Mapped[int] = mapped_column(
        ForeignKey("cases.id"),
        nullable=False,
        index=True,
    )

    previous_assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    new_assignee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    assigned_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
