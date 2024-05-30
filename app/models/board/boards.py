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
        board = await session.get(cls, board_id)
        if board:
            raise ValueError(f"{board_id} 게시판 이미 존재.")
        new_status = Boards(user_id=board_id, title=title, content=content, password=password)
        session.add(new_status)
        created_status = await cls.get_board_by_board_id(session, board_id, password)
        return created_status

    @classmethod
    async def get_board_by_board_id(cls, session: AsyncSession, board_id: int, password: int):
        res = await session.get(cls, board_id, password)
        if not res:
            raise ValueError(f"{board_id} 게시판이 존재하지 않습니다.")

        return res

    # 게시판 글 수정시에는 패스워드 다시 입력받지 않는 것으로?
    @classmethod
    async def update_board_by_board_id(
        cls, session: AsyncSession, board_id: int, title: str, content: str, password: int
    ):
        board = await cls.get_board_by_board_id(session, board_id, password)
        board.board_data.update(title, content)

        return board
