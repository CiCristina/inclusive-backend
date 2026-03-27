from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    job_type: str = "full-time"   # 'full-time' | 'part-time' | 'contract' | 'internship'
    work_model: str = "hybrid"    # 'remote' | 'hybrid' | 'on-site'
    salary_range: str | None = None
    description: str
    requirements: str | None = None
    is_accessible: bool = False
    is_internal: bool = True


class JobUpdate(BaseModel):
    title: str | None = None
    department: str | None = None
    location: str | None = None
    job_type: str | None = None
    work_model: str | None = None
    salary_range: str | None = None
    description: str | None = None
    requirements: str | None = None
    is_accessible: bool | None = None
    is_internal: bool | None = None
    is_active: bool | None = None


class JobOut(BaseModel):
    id: int
    title: str
    department: str
    location: str
    job_type: str
    work_model: str
    salary_range: str | None
    description: str
    requirements: str | None
    is_accessible: bool
    is_internal: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class JobApplicationCreate(BaseModel):
    cover_letter: str | None = None


class JobApplicationOut(BaseModel):
    id: int
    job: JobOut
    applicant_id: int
    cover_letter: str | None
    status: str
    applied_at: datetime

    model_config = {"from_attributes": True}
