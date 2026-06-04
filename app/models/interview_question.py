import uuid
from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_sessions.id")
    )

    question_number: Mapped[int] = mapped_column(
        Integer
    )

    question_text: Mapped[str] = mapped_column(
        Text
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    focus_area: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )