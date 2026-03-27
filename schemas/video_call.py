from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VideoCallCreate(BaseModel):
    participant_id: int
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 30
    requires_libras: bool = False
    sign_language: str = "libras"  # 'libras' | 'asl' | 'lsf' | 'bsl'
    created_by_role: str = "employee"  # 'employee' | 'manager'


class VideoCallUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    requires_libras: Optional[bool] = None
    sign_language: Optional[str] = None
    status: Optional[str] = None  # 'scheduled' | 'in-progress' | 'completed' | 'cancelled'


class ParticipantOut(BaseModel):
    id: int
    name: str
    role: Optional[str]
    avatar_url: Optional[str]

    model_config = {"from_attributes": True}


class VideoCallOut(BaseModel):
    id: int
    created_by: ParticipantOut
    participant: ParticipantOut
    title: str
    description: Optional[str]
    scheduled_at: datetime
    duration_minutes: int
    requires_libras: bool
    sign_language: str
    status: str
    created_by_role: str
    created_at: datetime

    model_config = {"from_attributes": True}
