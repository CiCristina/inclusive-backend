import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.assessment import Assessment, AssessmentSubmission
from models.user import User
from schemas.assessment import AssessmentOut, AssessmentSubmissionCreate, AssessmentSubmissionOut

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("", response_model=list[AssessmentOut])
def list_assessments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Assessment).order_by(Assessment.due_date.asc()).all()


@router.get("/{assessment_id}", response_model=AssessmentOut)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("/{assessment_id}/submit", response_model=AssessmentSubmissionOut, status_code=201)
def submit_assessment(
    assessment_id: int,
    body: AssessmentSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    existing = (
        db.query(AssessmentSubmission)
        .filter(
            AssessmentSubmission.assessment_id == assessment_id,
            AssessmentSubmission.user_id == current_user.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Assessment already submitted")

    submission = AssessmentSubmission(
        assessment_id=assessment_id,
        user_id=current_user.id,
        answers=json.dumps(body.answers),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/my/submissions", response_model=list[AssessmentSubmissionOut])
def my_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(AssessmentSubmission)
        .filter(AssessmentSubmission.user_id == current_user.id)
        .all()
    )
