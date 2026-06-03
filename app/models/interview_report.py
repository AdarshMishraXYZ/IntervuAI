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


class InterviewReport(Base):
    __tablename__ = "interview_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_sessions.id")
    )

    technical_score: Mapped[int] = mapped_column(Integer)

    communication_score: Mapped[int] = mapped_column(Integer)

    problem_solving_score: Mapped[int] = mapped_column(Integer)

    overall_score: Mapped[int] = mapped_column(Integer)

    readiness_level: Mapped[str] = mapped_column(String(100))

    strengths: Mapped[str] = mapped_column(Text)

    areas_to_improve: Mapped[str] = mapped_column(Text)

    next_steps: Mapped[str] = mapped_column(Text)

    feedback: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )