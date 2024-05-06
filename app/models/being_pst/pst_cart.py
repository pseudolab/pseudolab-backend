from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime

from models.base import Base

class PstCart(Base):
    __tablename__ = "pst_cart"

    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    sentence_id = mapped_column(Integer, nullable=False)

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )