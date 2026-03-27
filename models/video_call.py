from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.user import User


class VideoCall(Base):
    __tablename__ = "video_calls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    participant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)

    requires_libras: Mapped[bool] = mapped_column(Boolean, default=False)
    # 'libras' | 'asl' | 'lsf' | 'bsl'
    sign_language: Mapped[str] = mapped_column(String(10), default="libras")

    # 'scheduled' | 'in-progress' | 'completed' | 'cancelled'
    status: Mapped[str] = mapped_column(String(20), default="scheduled")

    # 'employee' | 'manager'
    created_by_role: Mapped[str] = mapped_column(String(20), default="employee")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    created_by: Mapped["User"] = relationship(
        "User", foreign_keys=[created_by_id], back_populates="video_calls_created"
    )
    participant: Mapped["User"] = relationship(
        "User", foreign_keys=[participant_id]
    )
