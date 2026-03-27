from datetime import datetime

from pydantic import BaseModel


class CareerMilestoneCreate(BaseModel):
    title: str
    description: str | None = None


class CareerMilestoneUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None


class CareerMilestoneOut(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CareerGoalCreate(BaseModel):
    title: str
    description: str | None = None
    target_date: datetime | None = None
    milestones: list[CareerMilestoneCreate] = []


class CareerGoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_date: datetime | None = None
    is_achieved: bool | None = None


class CareerGoalOut(BaseModel):
    id: int
    title: str
    description: str | None
    target_date: datetime | None
    is_achieved: bool
    milestones: list[CareerMilestoneOut]
    created_at: datetime

    model_config = {"from_attributes": True}
