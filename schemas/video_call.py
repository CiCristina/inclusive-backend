from datetime import datetime

from pydantic import BaseModel


class VideoCallCreate(BaseModel):
    participant_id: int
    title: str
    description: str | None = None
    scheduled_at: datetime
    duration_minutes: int = 30
    requires_libras: bool = False
    sign_language: str = "libras"  # 'libras' | 'asl' | 'lsf' | 'bsl'
    created_by_role: str = "employee"  # 'employee' | 'manager'


class VideoCallUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    requires_libras: bool | None = None
    sign_language: str | None = None
    status: str | None = None  # 'scheduled' | 'in-progress' | 'completed' | 'cancelled'


class ParticipantOut(BaseModel):
    id: int
    name: str
    role: str | None
    avatar_url: str | None

    model_config = {"from_attributes": True}


class VideoCallOut(BaseModel):
    id: int
    created_by: ParticipantOut
    participant: ParticipantOut
    title: str
    description: str | None
    scheduled_at: datetime
    duration_minutes: int
    requires_libras: bool
    sign_language: str
    status: str
    created_by_role: str
    created_at: datetime

    model_config = {"from_attributes": True}
