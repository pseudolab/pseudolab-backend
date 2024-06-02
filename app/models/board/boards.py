from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, BigInteger

from core.db import AsyncSession
from models.base import Base


class Boards(Base):
    __tablename__ = "boards"

    board_id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = mapped_column(String(255), nullable=False)
    content = mapped_column(String(1024), nullable=False)
    password = mapped_column(String(4), nullable=False)
    created_at = mapped_column(
        BigInteger, default=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000), nullable=False
    )
    updated_at = mapped_column(
        BigInteger,
        default=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000),
        onupdate=lambda: int(datetime.now(ZoneInfo("Asia/Seoul")).timestamp() * 1000),
        nullable=False,
    )
    comments = relationship("Comments", back_populates="board", cascade="all, delete-orphan")

    @classmethod
    async def create(cls, session: AsyncSession, title: str, content: str, password: str):
        new_board = Boards(title=title, content=content, password=password)
        session.add(new_board)
        await session.commit()
        await session.refresh(new_board)
        return new_board

    @classmethod
    async def get_board_by_board_id_with_password(cls, session: AsyncSession, board_id: int, password: str):
        board = await session.get(cls, board_id)
        return board

    @classmethod
    async def update_board_by_board_id(
        cls, session: AsyncSession, board_id: int, title: str, content: str, password: str
    ):
        board = await cls.get_board_by_board_id_with_password(session, board_id, password)
        board.title = title
        board.content = content
        await session.commit()
        await session.refresh(board)
        return board

    @classmethod
    async def delete_board_by_board_id(cls, session: AsyncSession, board_id: int, password: str):
        board = await cls.get_board_by_board_id_with_password(session, board_id, password)
        await session.delete(board)
        await session.commit()
        return board
