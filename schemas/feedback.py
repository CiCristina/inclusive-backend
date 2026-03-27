from datetime import datetime

from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    recipient_id: int
    feedback_type: str  # 'positive' | 'constructive' | 'development' | 'recognition'
    input_mode: str = "text"  # 'text' | 'voice' | 'video'
    content: str
    media_url: str | None = None


class FeedbackUpdate(BaseModel):
    status: str  # 'pending' | 'read' | 'acknowledged'


class AuthorOut(BaseModel):
    id: int
    name: str
    role: str | None
    department: str | None
    avatar_url: str | None

    model_config = {"from_attributes": True}


class FeedbackOut(BaseModel):
    id: int
    author: AuthorOut
    recipient: AuthorOut
    feedback_type: str
    input_mode: str
    content: str
    media_url: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
