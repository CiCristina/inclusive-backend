from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    job_type: str = "full-time"   # 'full-time' | 'part-time' | 'contract' | 'internship'
    work_model: str = "hybrid"    # 'remote' | 'hybrid' | 'on-site'
    salary_range: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    is_accessible: bool = False
    is_internal: bool = True


class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_model: Optional[str] = None
    salary_range: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    is_accessible: Optional[bool] = None
    is_internal: Optional[bool] = None
    is_active: Optional[bool] = None


class JobOut(BaseModel):
    id: int
    title: str
    department: str
    location: str
    job_type: str
    work_model: str
    salary_range: Optional[str]
    description: str
    requirements: Optional[str]
    is_accessible: bool
    is_internal: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class JobApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None


class JobApplicationOut(BaseModel):
    id: int
    job: JobOut
    applicant_id: int
    cover_letter: Optional[str]
    status: str
    applied_at: datetime

    model_config = {"from_attributes": True}
