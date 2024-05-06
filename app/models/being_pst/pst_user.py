from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime

from models.base import Base

class PstUser(Base):
    __tablename__ = "pst_user"

    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    budget = mapped_column(Integer, default=1000, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        nullable=False,
    )