from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio
import random

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, DateTime, JSON, select, desc
from sqlalchemy.ext.mutable import MutableDict

from core.db import AsyncSession
from models.base import Base
from models.bingo.schema import BingoInteractionSchema, BingoEventUserInfo, BingoQRScanSchema
from models.user import BingoUser


class BingoBoards(Base):
    __tablename__ = "bingo_boards"

    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    board_data = mapped_column(MutableDict.as_mutable(JSON), nullable=False)

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
        board.board_data.update(board_data)

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

        return board

    @classmethod
    async def get_user_selected_words(cls, session: AsyncSession, user_id: int):
        board = await cls.get_board_by_userid(session, user_id)

        board_data = board.board_data
        selected_words = []
        for board_block in board_data.values():
            if board_block.get("selected") == 1:
                selected_words.append(board_block.get("value"))

        return selected_words

    @classmethod
    async def update_bingo_status_by_selected_user(
        cls, session: AsyncSession, send_user_id: int, receive_user_id: int
    ) -> BingoInteractionSchema:
        if send_user_id == receive_user_id:
            raise ValueError("보내는 계정과 받는 계정이 같습니다.")

        board = await cls.get_board_by_userid(session, receive_user_id)
        # selected_words = await cls.get_user_selected_words(session, send_user_id)
        board_data = board.board_data
        send_user = await BingoUser.get_user_by_id(session, send_user_id)
        if not send_user:
            raise ValueError(f"{send_user_id} 존재하지 않는 아이디")

        receive_user = await BingoUser.get_user_by_id(session, receive_user_id)
        if not receive_user:
            raise ValueError(f"{receive_user_id} 존재하지 않는 아이디")

        already_interaction = False

        not_selected_ids = []
        for idx, bingo_dict in board_data.items():
            value, status = bingo_dict["value"], bingo_dict["status"]
            if send_user.username == value:  # 이미 interaction 한 유저인 경우는 Pass
                already_interaction = True
                break
            if status == 0:
                # get not selected list
                not_selected_ids.append(idx)

        if not already_interaction:
            # update random board data
            update_idx = random.choice(not_selected_ids)
            board_data[update_idx]["value"] = send_user.username
            board_data[update_idx]["status"] = 1
            board_data[update_idx]["user_id"] = send_user_id
            await cls.update_board_by_userid(session, receive_user_id, board_data)
            board = await cls.update_bingo_count(session, receive_user_id)

        return BingoInteractionSchema(
            send_user_id=send_user_id,
            receive_user_id=receive_user_id,
            updated_words=[send_user.username],
            bingo_count=board.bingo_count,
        )

    @classmethod
    async def get_bingo_event_users(cls, session: AsyncSession, bingo_count: int) -> list:
        query = select(cls).filter(cls.bingo_count >= bingo_count).order_by(desc(cls.bingo_count))
        result = await session.execute(query)
        bingo_event_users = [(board.user_id, board.bingo_count) for board in result.scalars().all()]

        selected_users_info = await asyncio.gather(
            *[BingoUser.get_user_by_id(session, user_id) for user_id, _ in bingo_event_users]
        )
        bingo_event_users_info = [
            BingoEventUserInfo(rank=idx, user_name=user_info.username, bingo_count=bingo_count)
            for idx, ((_, bingo_count), user_info) in enumerate(zip(bingo_event_users, selected_users_info), start=1)
        ]

        return bingo_event_users_info

    @classmethod
    async def update_bingo_status_by_qr_scan(cls, session: AsyncSession, user_id: int, booth_id: int):
        booth_exist = False
        not_selected_ids = []
        # get board_data, check user_id is already have booth bingo
        board = await cls.get_board_by_userid(session, user_id)
        board_data = board.board_data
        updated_booth_name = f"Booth {booth_id}"
        for idx, bingo_dict in board_data.items():
            value, status = bingo_dict["value"], bingo_dict["status"]
            if value == updated_booth_name:
                booth_exist = True
                break
            if status == 0:
                # get not selected list
                not_selected_ids.append(idx)

        if not booth_exist:
            # update random board data
            booth_idx = random.choice(not_selected_ids)
            board_data[booth_idx]["value"] = updated_booth_name
            board_data[booth_idx]["status"] = 1
            await cls.update_board_by_userid(session, user_id, board_data)
            board = await cls.update_bingo_count(session, user_id)

        return BingoQRScanSchema(
            user_id=user_id,
            booth_id=booth_id,
            updated_words=[updated_booth_name],
            bingo_count=board.bingo_count,
        )
