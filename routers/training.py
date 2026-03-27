from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.training import Training, TrainingEnrollment
from models.user import User
from schemas.training import EnrollRequest, ProgressUpdate, TrainingEnrollmentOut, TrainingOut

router = APIRouter(prefix="/training", tags=["training"])


@router.get("", response_model=list[TrainingOut])
def list_trainings(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Training).filter(Training.is_active == True).all()


@router.get("/my", response_model=list[TrainingEnrollmentOut])
def my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(TrainingEnrollment)
        .filter(TrainingEnrollment.user_id == current_user.id)
        .all()
    )


@router.get("/{training_id}", response_model=TrainingOut)
def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    training = db.get(Training, training_id)
    if not training or not training.is_active:
        raise HTTPException(status_code=404, detail="Training not found")
    return training


@router.post("/enroll", response_model=TrainingEnrollmentOut, status_code=201)
def enroll(
    body: EnrollRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    training = db.get(Training, body.training_id)
    if not training or not training.is_active:
        raise HTTPException(status_code=404, detail="Training not found")

    existing = (
        db.query(TrainingEnrollment)
        .filter(
            TrainingEnrollment.training_id == body.training_id,
            TrainingEnrollment.user_id == current_user.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this training")

    enrollment = TrainingEnrollment(training_id=body.training_id, user_id=current_user.id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.patch("/{training_id}/progress", response_model=TrainingEnrollmentOut)
def update_progress(
    training_id: int,
    body: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    enrollment = (
        db.query(TrainingEnrollment)
        .filter(
            TrainingEnrollment.training_id == training_id,
            TrainingEnrollment.user_id == current_user.id,
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    enrollment.progress_pct = max(0, min(100, body.progress_pct))
    if enrollment.progress_pct == 100 and not enrollment.is_completed:
        enrollment.is_completed = True
        enrollment.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(enrollment)
    return enrollment
