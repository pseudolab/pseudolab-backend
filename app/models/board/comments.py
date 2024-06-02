from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, BigInteger, ForeignKey

from core.db import AsyncSession
from models.base import Base


class Comments(Base):
    __tablename__ = "comments"

    comment_id = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    board_id = mapped_column(Integer, ForeignKey("boards.board_id"), nullable=False)
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
    board = relationship("Boards", back_populates="comments")

    @classmethod
    async def create(cls, session: AsyncSession, board_id: str, content: str, password: str):
        new_comment = Comments(board_id=board_id, content=content, password=password)
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return new_comment

    @classmethod
    async def get_comment_by_comment_id_with_password(
        cls, session: AsyncSession, board_id: int, comment_id: int, password: str
    ):
        comment = await session.get(cls, board_id, comment_id, password)
        return comment

    @classmethod
    async def update_comment_by_comment_id(
        cls, session: AsyncSession, board_id: int, comment_id: int, content: str, password: str
    ):
        comment = await cls.get_comment_by_comment_id_with_password(session, board_id, comment_id, password)
        comment.content = content
        await session.commit()
        await session.refresh(comment)
        return comment

    @classmethod
    async def delete_comment_by_comment_id(cls, session: AsyncSession, board_id: int, comment_id: int, password: str):
        comment = await cls.get_comment_by_comment_id_with_password(session, board_id, comment_id, password)
        await session.delete(comment)
        await session.commit()
        return comment
