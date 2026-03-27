from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.deps import get_current_user, require_company
from database import get_db
from models.job import Job, JobApplication
from models.user import User
from schemas.job import JobApplicationCreate, JobApplicationOut, JobCreate, JobOut, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobOut])
def list_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Job).filter(Job.is_active == True).order_by(Job.created_at.desc()).all()


@router.post("", response_model=JobOut, status_code=201)
def create_job(
    body: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    job = Job(posted_by_id=current_user.id, **body.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    job = db.get(Job, job_id)
    if not job or not job.is_active:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.patch("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    body: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_company),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.posted_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own job postings")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job


@router.post("/{job_id}/apply", response_model=JobApplicationOut, status_code=201)
def apply_to_job(
    job_id: int,
    body: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.get(Job, job_id)
    if not job or not job.is_active:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = (
        db.query(JobApplication)
        .filter(JobApplication.job_id == job_id, JobApplication.applicant_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="You have already applied to this job")

    application = JobApplication(
        job_id=job_id,
        applicant_id=current_user.id,
        cover_letter=body.cover_letter,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/my/applications", response_model=list[JobApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(JobApplication)
        .filter(JobApplication.applicant_id == current_user.id)
        .order_by(JobApplication.applied_at.desc())
        .all()
    )
