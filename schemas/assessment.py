from datetime import datetime

from pydantic import BaseModel


class AssessmentOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    due_date: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AssessmentSubmissionCreate(BaseModel):
    answers: dict  # Free-form key/value pairs per question


class AssessmentSubmissionOut(BaseModel):
    id: int
    assessment: AssessmentOut
    user_id: int
    answers: str  # Stored as JSON string in DB
    score: int | None
    status: str
    submitted_at: datetime

    model_config = {"from_attributes": True}
