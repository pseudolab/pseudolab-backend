from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

from core.db import AsyncSession
from models.base import Base


class Boards(Base):
    __tablename__ = "boards"

    board_id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    password = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        Integer, default=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000), nullable=False
    )
    updated_at = mapped_column(
        Integer,
        default=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000),
        onupdate=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000),
        nullable=False,
    )

    @classmethod
    async def create(cls, session: AsyncSession, board_id: int, title: str, content: str, password: int):
        pass

    @classmethod
    async def get_board_by_board_id(cls, session: AsyncSession, board_id: int, title: str, content: str, password: int):
        pass

    @classmethod
    async def update_board_by_board_id(
        cls, session: AsyncSession, board_id: int, title: str, content: str, password: int
    ):
        pass
