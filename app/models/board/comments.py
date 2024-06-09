from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, BigInteger, ForeignKey, select, desc

from core.db import AsyncSession
from models.base import Base
from models.board import Boards

from fastapi import HTTPException


class Comments(Base):
    __tablename__ = "comments"

    comment_id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    author = mapped_column(String(255), default="anonymous", nullable=False)
    board_id = mapped_column(Integer, ForeignKey("boards.board_id"), nullable=False)
    contents = mapped_column(String(1024), nullable=False)
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
    board = relationship("Boards", back_populates="comments")

    @classmethod
    async def create(cls, session: AsyncSession, board_id: str, author: str, contents: str, password: str):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        new_comment = Comments(board_id=board_id, author=author, contents=contents, password=password)
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return new_comment

    @classmethod
    async def get_comment_by_comment_id(cls, session: AsyncSession, board_id: int, comment_id: int):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        comment = await session.get(cls, comment_id)
        return comment

    @classmethod
    async def get_comment_by_comment_id_with_password(
        cls, session: AsyncSession, board_id: int, comment_id: int, password: str
    ):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        comment = await session.get(cls, comment_id)
        if comment.password != password:
            raise ValueError("Incorrect password")
        return comment

    @classmethod
    async def update_comment_by_comment_id(
        cls, session: AsyncSession, board_id: int, comment_id: int, contents: str, password: str
    ):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        comment = await cls.get_comment_by_comment_id_with_password(session, board_id, comment_id, password)
        comment.contents = contents
        await session.commit()
        await session.refresh(comment)
        return comment

    @classmethod
    async def delete_comment_by_comment_id(cls, session: AsyncSession, board_id: int, comment_id: int, password: str):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        comment = await cls.get_comment_by_comment_id_with_password(session, board_id, comment_id, password)
        await session.delete(comment)
        await session.commit()
        return comment

    @classmethod
    async def get_board_all_comments(cls, session: AsyncSession, board_id: int):
        board = await session.get(Boards, board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        result = await session.execute(select(cls).order_by(desc(cls.comment_id)).where(cls.board_id == board_id))
        comments = result.scalars().all()
        return comments
