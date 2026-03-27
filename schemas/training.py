from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TrainingOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    duration_hours: int
    thumbnail_url: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TrainingEnrollmentOut(BaseModel):
    id: int
    training: TrainingOut
    user_id: int
    progress_pct: int
    is_completed: bool
    enrolled_at: datetime
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class EnrollRequest(BaseModel):
    training_id: int


class ProgressUpdate(BaseModel):
    progress_pct: int  # 0-100
