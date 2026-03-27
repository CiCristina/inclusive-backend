from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    recipient_id: int
    feedback_type: str  # 'positive' | 'constructive' | 'development' | 'recognition'
    input_mode: str = "text"  # 'text' | 'voice' | 'video'
    content: str
    media_url: Optional[str] = None


class FeedbackUpdate(BaseModel):
    status: str  # 'pending' | 'read' | 'acknowledged'


class AuthorOut(BaseModel):
    id: int
    name: str
    role: Optional[str]
    department: Optional[str]
    avatar_url: Optional[str]

    model_config = {"from_attributes": True}


class FeedbackOut(BaseModel):
    id: int
    author: AuthorOut
    recipient: AuthorOut
    feedback_type: str
    input_mode: str
    content: str
    media_url: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
