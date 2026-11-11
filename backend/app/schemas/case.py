from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)


class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
