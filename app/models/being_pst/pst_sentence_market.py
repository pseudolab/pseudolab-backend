from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime

from models.base import Base

class PstSentenceMarket(Base):
    __tablename__ = "pst_sentence_market"

    sentence_id = mapped_column(Integer, primary_key=True, nullable=False)
    price = mapped_column(Integer, nullable=False)

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        nullable=False,
    )