from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.feedback import Feedback
from models.user import User
from schemas.feedback import FeedbackCreate, FeedbackOut, FeedbackUpdate

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/received", response_model=list[FeedbackOut])
def get_received(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Feedback)
        .filter(Feedback.recipient_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .all()
    )


@router.get("/given", response_model=list[FeedbackOut])
def get_given(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Feedback)
        .filter(Feedback.author_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .all()
    )


@router.post("", response_model=FeedbackOut, status_code=201)
def create_feedback(
    body: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if body.recipient_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send feedback to yourself")

    recipient = db.get(User, body.recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    feedback = Feedback(
        author_id=current_user.id,
        recipient_id=body.recipient_id,
        feedback_type=body.feedback_type,
        input_mode=body.input_mode,
        content=body.content,
        media_url=body.media_url,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/{feedback_id}", response_model=FeedbackOut)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    feedback = db.get(Feedback, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.author_id != current_user.id and feedback.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return feedback


@router.patch("/{feedback_id}", response_model=FeedbackOut)
def update_feedback_status(
    feedback_id: int,
    body: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    feedback = db.get(Feedback, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the recipient can update status")

    feedback.status = body.status
    db.commit()
    db.refresh(feedback)
    return feedback
