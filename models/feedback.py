from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.user import User


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # 'positive' | 'constructive' | 'development' | 'recognition'
    feedback_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # 'text' | 'voice' | 'video'
    input_mode: Mapped[str] = mapped_column(String(10), default="text")
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Optional audio/video URL when submitted via voice/video
    media_url: Mapped[Optional[str]] = mapped_column(String(500))

    # 'pending' | 'read' | 'acknowledged'
    status: Mapped[str] = mapped_column(String(20), default="pending")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    author: Mapped["User"] = relationship(
        "User", foreign_keys=[author_id], back_populates="feedbacks_given"
    )
    recipient: Mapped["User"] = relationship(
        "User", foreign_keys=[recipient_id], back_populates="feedbacks_received"
    )
