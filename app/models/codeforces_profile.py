import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CodeforcesProfile(Base):
    __tablename__ = "codeforces_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    username: Mapped[str] = mapped_column(String(100))

    rating: Mapped[int] = mapped_column(Integer, default=0)

    max_rating: Mapped[int] = mapped_column(Integer, default=0)

    rank: Mapped[str] = mapped_column(String(100), default="unrated")

    max_rank: Mapped[str] = mapped_column(String(100), default="unrated")

    contribution: Mapped[int] = mapped_column(Integer, default=0)

    friend_count: Mapped[int] = mapped_column(Integer, default=0)

    codeforces_score: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )