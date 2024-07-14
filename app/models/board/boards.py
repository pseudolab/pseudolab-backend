from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column, relationship, joinedload
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, BigInteger, select, desc

from core.db import AsyncSession, AsyncSessionDepends
from models.base import Base


class Boards(Base):
    __tablename__ = "boards"

    board_id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    author = mapped_column(String(255), default="anonymous", nullable=False)
    title = mapped_column(String(255), nullable=False)
    contents = mapped_column(String(1024), nullable=False)
    password = mapped_column(String(4), nullable=False)
    view_count = mapped_column(Integer, default=0, nullable=False)
    like_count = mapped_column(Integer, default=0, nullable=False)
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
    async def create(cls, session: AsyncSession, title: str, author: str, contents: str, password: str):
        new_board = Boards(title=title, author=author, contents=contents, password=password)
        session.add(new_board)
        await session.commit()
        await session.refresh(new_board)
        return new_board

    @classmethod
    async def get_board_by_board_id(cls, session: AsyncSession, board_id: int, view_update=True) -> "Boards":
        result = await session.execute(select(cls).where(cls.board_id == board_id))
        board = result.scalars().first()
        if not board:
            raise ValueError(f"Board with ID {board_id} does not exist.")
        # FIXME : 수정 시에는 view count update 안되도록 설정
        if view_update:
            board.view_count += 1
        await session.commit()
        await session.refresh(board)
        return board

    @classmethod
    async def get_board_by_board_id_with_password(
        cls, session: AsyncSession, board_id: int, password: str, view_update=True
    ):
        # board = await session.get(cls, board_id)
        # return board
        board = await cls.get_board_by_board_id(session, board_id, view_update)
        if board.password != password:
            raise ValueError("Incorrect password")
        return board

    @classmethod
    async def update_board_by_board_id(
        cls, session: AsyncSession, board_id: int, title: str, contents: str, password: str
    ):
        board = await cls.get_board_by_board_id_with_password(session, board_id, password, view_update=False)
        board.title = title
        board.contents = contents
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
        result = await session.execute(select(cls).options(joinedload(cls.comments)).distinct())
        boards = result.unique().scalars().all()
        return boards

    @classmethod
    async def get_page_boards(cls, session: AsyncSession, offset: int, limit: int):
        result = await session.execute(
            select(cls).order_by(desc(cls.board_id)).options(joinedload(cls.comments)).offset(offset).limit(limit)
        )
        boards = result.unique().scalars().all()
        return boards

    @classmethod
    async def update_like_count(cls, session: AsyncSession, board_id: int, increment: bool = True):
        board = await session.get(cls, board_id)
        if not board:
            raise ValueError(f"Board with ID {board_id} does not exist.")
        board.like_count = board.like_count + 1 if increment else max(0, board.like_count - 1)
        await session.commit()
        await session.refresh(board)
        return board
