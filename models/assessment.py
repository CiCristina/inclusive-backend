from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.user import User


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # 'performance' | 'skills' | 'culture' | 'leadership'
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    submissions: Mapped[List["AssessmentSubmission"]] = relationship(
        "AssessmentSubmission", back_populates="assessment"
    )


class AssessmentSubmission(Base):
    __tablename__ = "assessment_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    answers: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    score: Mapped[Optional[int]] = mapped_column(Integer)  # 0-100
    # 'pending' | 'submitted' | 'reviewed'
    status: Mapped[str] = mapped_column(String(20), default="submitted")

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="submissions")
    user: Mapped["User"] = relationship("User", back_populates="assessment_submissions")
