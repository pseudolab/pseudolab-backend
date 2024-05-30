from core.db import AsyncSessionDepends
from models.board import Boards
from api.board.crud.schema import (
    BoardResponse,
)


class BaseBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoard(BaseBoard):
    async def execute(self, board_id: int, title: str, content: str, password: int) -> Boards:
        try:
            res = await Boards.create(self.async_session, board_id, title, content, password)
            return BoardResponse(**res.__dict__, ok=True, message="게시판 생성에 성공하였습니다.")
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, password: int) -> Boards:
        try:
            res = await Boards.get_board_by_board_id(self.async_session, board_id, password)
            return BoardResponse(**res.__dict__, ok=True, message="게시판 조회에 성공하였습니다.")
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class UpdateBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, title: str, content: str, password: int) -> Boards:
        try:
            res = await Boards.update_board_by_userid(self.async_session, board_id, title, content, password)
            return BoardResponse(**res.__dict__, ok=True, message="게시판 수정에 성공하였습니다.")
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))
