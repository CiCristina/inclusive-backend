from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.career import CareerGoal, CareerMilestone
from models.user import User
from schemas.career import (
    CareerGoalCreate,
    CareerGoalOut,
    CareerGoalUpdate,
    CareerMilestoneCreate,
    CareerMilestoneOut,
    CareerMilestoneUpdate,
)

router = APIRouter(prefix="/career", tags=["career"])


@router.get("/goals", response_model=list[CareerGoalOut])
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(CareerGoal)
        .filter(CareerGoal.user_id == current_user.id)
        .order_by(CareerGoal.created_at.desc())
        .all()
    )


@router.post("/goals", response_model=CareerGoalOut, status_code=201)
def create_goal(
    body: CareerGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = CareerGoal(
        user_id=current_user.id,
        title=body.title,
        description=body.description,
        target_date=body.target_date,
    )
    for m in body.milestones:
        goal.milestones.append(CareerMilestone(title=m.title, description=m.description))

    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.patch("/goals/{goal_id}", response_model=CareerGoalOut)
def update_goal(
    goal_id: int,
    body: CareerGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = _get_own_goal(goal_id, current_user.id, db)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/goals/{goal_id}", status_code=204)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = _get_own_goal(goal_id, current_user.id, db)
    db.delete(goal)
    db.commit()


@router.post("/goals/{goal_id}/milestones", response_model=CareerMilestoneOut, status_code=201)
def add_milestone(
    goal_id: int,
    body: CareerMilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = _get_own_goal(goal_id, current_user.id, db)
    milestone = CareerMilestone(goal_id=goal.id, title=body.title, description=body.description)
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone


@router.patch("/milestones/{milestone_id}", response_model=CareerMilestoneOut)
def update_milestone(
    milestone_id: int,
    body: CareerMilestoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    milestone = _get_own_milestone(milestone_id, current_user.id, db)

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(milestone, field, value)

    if body.is_completed and not milestone.completed_at:
        milestone.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(milestone)
    return milestone


# ── helpers ──────────────────────────────────────────────────────────────────

def _get_own_goal(goal_id: int, user_id: int, db: Session) -> CareerGoal:
    goal = db.get(CareerGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return goal


def _get_own_milestone(milestone_id: int, user_id: int, db: Session) -> CareerMilestone:
    milestone = db.get(CareerMilestone, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    if milestone.goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return milestone
