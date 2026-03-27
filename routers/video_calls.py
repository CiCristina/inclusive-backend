from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.user import User
from models.video_call import VideoCall
from schemas.video_call import VideoCallCreate, VideoCallOut, VideoCallUpdate

router = APIRouter(prefix="/video-calls", tags=["video-calls"])


@router.get("", response_model=list[VideoCallOut])
def list_video_calls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(VideoCall)
        .filter(
            or_(
                VideoCall.created_by_id == current_user.id,
                VideoCall.participant_id == current_user.id,
            )
        )
        .order_by(VideoCall.scheduled_at.asc())
        .all()
    )


@router.post("", response_model=VideoCallOut, status_code=201)
def schedule_video_call(
    body: VideoCallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    participant = db.get(User, body.participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    call = VideoCall(
        created_by_id=current_user.id,
        **body.model_dump(),
    )
    db.add(call)
    db.commit()
    db.refresh(call)
    return call


@router.get("/{call_id}", response_model=VideoCallOut)
def get_video_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    call = db.get(VideoCall, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Video call not found")
    if call.created_by_id != current_user.id and call.participant_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return call


@router.patch("/{call_id}", response_model=VideoCallOut)
def update_video_call(
    call_id: int,
    body: VideoCallUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    call = db.get(VideoCall, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Video call not found")
    if call.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can update this call")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(call, field, value)

    db.commit()
    db.refresh(call)
    return call


@router.delete("/{call_id}", status_code=204)
def cancel_video_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    call = db.get(VideoCall, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Video call not found")
    if call.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can cancel this call")

    call.status = "cancelled"
    db.commit()
