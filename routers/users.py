from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.deps import get_current_user
from database import get_db
from models.user import User
from schemas.user import AccessibilitySettings, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.put("/me", response_model=UserOut)
def update_me(
    body: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    simple_fields = ["name", "department", "role", "company_name", "avatar_url", "bio", "phone"]
    for field in simple_fields:
        value = getattr(body, field)
        if value is not None:
            setattr(current_user, field, value)

    if body.accessibility is not None:
        _apply_accessibility(current_user, body.accessibility)

    db.commit()
    db.refresh(current_user)
    return UserOut.model_validate(current_user)


@router.put("/me/accessibility", response_model=UserOut)
def update_accessibility(
    body: AccessibilitySettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _apply_accessibility(current_user, body)
    db.commit()
    db.refresh(current_user)
    return UserOut.model_validate(current_user)


def _apply_accessibility(user: User, settings: AccessibilitySettings) -> None:
    user.accessibility_libras = settings.libras
    user.accessibility_captions = settings.captions
    user.accessibility_high_contrast = settings.high_contrast
    user.accessibility_screen_reader = settings.screen_reader
    user.accessibility_font_size = settings.font_size
    user.preferred_language = settings.preferred_language
