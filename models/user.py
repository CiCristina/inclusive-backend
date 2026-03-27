from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.feedback import Feedback
    from models.video_call import VideoCall
    from models.job import JobApplication
    from models.training import TrainingEnrollment
    from models.assessment import AssessmentSubmission
    from models.career import CareerGoal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'employee' | 'company'
    department: Mapped[str | None] = mapped_column(String(100))
    role: Mapped[str | None] = mapped_column(String(100))
    company_name: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    bio: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(String(30))

    # Accessibility settings (stored as simple flags)
    accessibility_libras: Mapped[bool] = mapped_column(Boolean, default=False)
    accessibility_captions: Mapped[bool] = mapped_column(Boolean, default=False)
    accessibility_high_contrast: Mapped[bool] = mapped_column(Boolean, default=False)
    accessibility_screen_reader: Mapped[bool] = mapped_column(Boolean, default=False)
    accessibility_font_size: Mapped[str] = mapped_column(String(10), default="medium")  # small|medium|large
    preferred_language: Mapped[str] = mapped_column(String(5), default="pt")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    feedbacks_given: Mapped[list["Feedback"]] = relationship(
        "Feedback", foreign_keys="Feedback.author_id", back_populates="author"
    )
    feedbacks_received: Mapped[list["Feedback"]] = relationship(
        "Feedback", foreign_keys="Feedback.recipient_id", back_populates="recipient"
    )
    video_calls_created: Mapped[list["VideoCall"]] = relationship(
        "VideoCall", foreign_keys="VideoCall.created_by_id", back_populates="created_by"
    )
    job_applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication", back_populates="applicant"
    )
    training_enrollments: Mapped[list["TrainingEnrollment"]] = relationship(
        "TrainingEnrollment", back_populates="user"
    )
    assessment_submissions: Mapped[list["AssessmentSubmission"]] = relationship(
        "AssessmentSubmission", back_populates="user"
    )
    career_goals: Mapped[list["CareerGoal"]] = relationship(
        "CareerGoal", back_populates="user"
    )
