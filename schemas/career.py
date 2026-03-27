from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CareerMilestoneCreate(BaseModel):
    title: str
    description: Optional[str] = None


class CareerMilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class CareerMilestoneOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class CareerGoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    milestones: List[CareerMilestoneCreate] = []


class CareerGoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    is_achieved: Optional[bool] = None


class CareerGoalOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    target_date: Optional[datetime]
    is_achieved: bool
    milestones: List[CareerMilestoneOut]
    created_at: datetime

    model_config = {"from_attributes": True}
