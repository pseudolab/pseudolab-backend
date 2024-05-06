from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime

from models.base import Base

class PstCategory(Base):
    __tablename__ = "pst_category"

    category_id = mapped_column(Integer, primary_key=True, nullable=False)
    category_name = mapped_column(String(200), nullable=False, unique=True)

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )