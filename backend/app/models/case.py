from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.case_reference import generate_case_reference
from app.db.base import Base


class Case(Base):
    __tablename__ = "cases"
    __table_args__ = (
        UniqueConstraint("reference", name="uq_cases_reference"),
    )
    reference: Mapped[str] = mapped_column(
        String(19),
        nullable=False,
        default=generate_case_reference,
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    incident_datetime: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    perceived_urgency: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    location_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location_precision: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="submitted",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
