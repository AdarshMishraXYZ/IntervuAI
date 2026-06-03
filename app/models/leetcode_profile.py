import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class LeetCodeProfile(Base):
    __tablename__ = "leetcode_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    username: Mapped[str] = mapped_column(
        String(100)
    )

    total_solved: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    easy_solved: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    medium_solved: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    hard_solved: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    leetcode_score: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )