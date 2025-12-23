from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .db import Base

class Settings(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    total_slots: Mapped[int] = mapped_column(Integer, nullable=False)
    slots_remaining: Mapped[int] = mapped_column(Integer, nullable=False)
    queue_seq: Mapped[int] = mapped_column(Integer, nullable=False)

class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # priority | insider
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    queue_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True)
