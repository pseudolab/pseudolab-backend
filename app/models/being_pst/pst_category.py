from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime

from core.db import AsyncSession
from models.base import Base

class PstCategory(Base):
    __tablename__ = "pst_category"

    category_id = mapped_column(Integer, primary_key=True, nullable=True, autoincrement=True)
    category_name = mapped_column(String(200), nullable=False, unique=True)

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )

    @classmethod
    async def create(cls, session: AsyncSession, category):
        new_category = cls(category)
        session.add(new_category)
        return new_category