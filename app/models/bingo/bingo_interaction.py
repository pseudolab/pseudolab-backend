from datetime import datetime
from zoneinfo import ZoneInfo

from models.base import Base
from sqlalchemy import Integer, DateTime, String, select
from sqlalchemy.orm import mapped_column

from core.db import AsyncSession


class BingoInteraction(Base):
    __tablename__ = "bingo_interaction"

    interaction_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_id_list = mapped_column(String(200), nullable=False)
    send_user_id = mapped_column(Integer, nullable=False)
    receive_user_id = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )

    @classmethod
    async def create(cls, session: AsyncSession, word_id_list, send_user_id, receive_user_id):
        new_interaction = BingoInteraction(
            word_id_list=word_id_list, send_user_id=send_user_id, receive_user_id=receive_user_id
        )
        session.add(new_interaction)
        return new_interaction

    @classmethod
    async def get_user_latest_interaction(cls, session: AsyncSession, user_id: int):
        res = await session.execute(
            select(cls).where(cls.receive_user_id == user_id).order_by(cls.created_at.desc()).limit(1)
        )
        data = res.scalars().first()
        return data
