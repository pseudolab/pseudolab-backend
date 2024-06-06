from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, BigInteger, select

from core.db import AsyncSession
from models.base import Base


class Boards(Base):
    __tablename__ = "boards"

    board_id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    author = mapped_column(String(255), default="anonymous", nullable=False)
    title = mapped_column(String(255), nullable=False)
    content = mapped_column(String(1024), nullable=False)
    password = mapped_column(String(4), nullable=False)
    view_count = mapped_column(Integer, default=0, nullable=False)
    like_count = mapped_column(Integer, nullable=False)
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
    async def create(cls, session: AsyncSession, title: str, author: str, content: str, password: str):
        new_board = Boards(title=title, author=author, content=content, password=password)
        session.add(new_board)
        await session.commit()
        await session.refresh(new_board)
        return new_board

    @classmethod
    async def get_board_by_board_id(cls, session: AsyncSession, board_id: int) -> "Boards":
        result = await session.execute(select(cls).where(cls.board_id == board_id))
        board = result.scalars().first()
        if not board:
            raise ValueError(f"Board with ID {board_id} does not exist.")
        board.view_count += 1
        await session.commit()
        await session.refresh(board)
        return board

    @classmethod
    async def get_board_by_board_id_with_password(cls, session: AsyncSession, board_id: int, password: str):
        # board = await session.get(cls, board_id)
        # return board
        board = await cls.get_board_by_board_id(session, board_id)
        if board.password != password:
            raise ValueError("Incorrect password")
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

    @classmethod
    async def get_all_boards(cls, session: AsyncSession):
        result = await session.execute(select(Boards))
        boards = result.scalars().all()
        return boards
