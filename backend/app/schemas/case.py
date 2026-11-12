from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)

    category: str | None = None
    incident_datetime: datetime | None = None
    perceived_urgency: str | None = None
    location_description: str | None = None
    location_precision: str | None = None


class CaseResponse(BaseModel):
    id: int
    reference: str
    title: str
    description: str
    status: str
    created_at: datetime

    category: str | None
    incident_datetime: datetime | None
    perceived_urgency: str | None
    location_description: str | None
    location_precision: str | None

    model_config = ConfigDict(from_attributes=True)
