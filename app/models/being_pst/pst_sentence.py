from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime

from core.db import AsyncSession
from models.base import Base

class PstSentence(Base):
    __tablename__ = "pst_sentence"

    sentence_id = mapped_column(Integer, primary_key=True, nullable=False)
    category_id = mapped_column(Integer, nullable=False)
    content = mapped_column(String(200), nullable=False, unique=True)

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )

    @classmethod
    async def create(cls, session: AsyncSession, category_id: int, content: str):
        new_sentence = PstSentence(
            category_id = category_id,
            content = content
        )
        session.add(new_sentence)
        return new_sentence
