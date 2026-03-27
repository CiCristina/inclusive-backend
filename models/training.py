from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.user import User


class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_hours: Mapped[int] = mapped_column(Integer, default=1)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    enrollments: Mapped[List["TrainingEnrollment"]] = relationship(
        "TrainingEnrollment", back_populates="training"
    )


class TrainingEnrollment(Base):
    __tablename__ = "training_enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    progress_pct: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    training: Mapped["Training"] = relationship("Training", back_populates="enrollments")
    user: Mapped["User"] = relationship("User", back_populates="training_enrollments")
