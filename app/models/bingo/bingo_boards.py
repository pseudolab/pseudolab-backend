from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime, JSON

from core.db import AsyncSession
from models.base import Base


class BingoBoards(Base):
    __tablename__ = "bingo_boards"

    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    board_data = mapped_column(JSON, nullable=False)
    bingo_count = mapped_column(Integer, default=0, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Seoul")),
        nullable=False,
    )

    @classmethod
    async def create(cls, session: AsyncSession, user_id: int, board_data: dict):
        user = await session.get(cls, user_id)
        if user:
            raise ValueError(f"{user_id} 의 빙고판은 이미 존재합니다.")
        new_status = BingoBoards(user_id=user_id, board_data=board_data)
        session.add(new_status)
        await session.flush()
        created_status = await cls.get_board_by_userid(session, user_id)
        return created_status

    @classmethod
    async def get_board_by_userid(cls, session: AsyncSession, user_id: int):
        res = await session.get(cls, user_id)
        if not res:
            raise ValueError(f"{user_id} 의 빙고판이 존재하지 않습니다.")

        return res

    @classmethod
    async def update_board_by_userid(cls, session: AsyncSession, user_id: int, board_data: dict):
        board = await cls.get_board_by_userid(session, user_id)

        board = await cls.get_board_by_userid(session, user_id)
        board.board_data = board_data
        await session.flush()

        return board

    @classmethod
    async def update_bingo_count(cls, session: AsyncSession, user_id: int):
        board = await cls.get_board_by_userid(session, user_id)

        board_data = board.board_data
        bingo = 0
        bingo_board = [[board_data[str(i * 5 + j)]["status"] for j in range(5)] for i in range(5)]

        for row in bingo_board:  # 가로
            if all(status == 1 for status in row):
                bingo += 1

        for col in zip(*bingo_board):  # 세로
            if all(status == 1 for status in col):
                bingo += 1

        if all(bingo_board[i][i] == 1 for i in range(5)):  # 대각선 왼 -> 오
            bingo += 1

        if all(bingo_board[i][4 - i] == 1 for i in range(5)):  # 대각선 오 -> 왼
            bingo += 1

        board.bingo_count = bingo
        await session.flush()
        return board

    @classmethod
    async def get_user_selected_words(cls, session: AsyncSession, user_id: int):
        board = await cls.get_board_by_userid(session, user_id)

        board_data = board.board_data
        selected_words = []
        for i in range(5):
            for j in range(5):
                if board_data[str(i * 5 + j)]["selected"] == 1:
                    selected_words.append(board_data[str(i * 5 + j)]["value"])
        return selected_words
