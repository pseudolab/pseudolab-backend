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
            board = await Boards.create(self.async_session, board_id, title, content, password)
            # return BoardResponse(**res.__dict__, ok=True, message="Board created successfully.")
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                content=board.content,
                ok=True,
                message="Board created successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, password: str) -> Boards:
        try:
            board = await Boards.get_board_by_board_id(self.async_session, board_id)
            if board.password != password:
                raise BoardResponse(ok=False, message="Incorrect password")
            # return BoardResponse(**res.__dict__, ok=True, message="게시판 조회에 성공하였습니다.")
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                content=board.content,
                ok=True,
                message="Board retrieved successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class UpdateBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, title: str, content: str, password: int) -> Boards:
        try:
            board = await Boards.get_board_by_board_id(self.async_session, board_id)
            if board.password != password:
                raise BoardResponse(ok=False, message="Incorrect password")
            updated_board = await Boards.update_board_by_board_id(self.async_session, board_id, title, content)
            return BoardResponse(
                board_id=updated_board.board_id,
                title=updated_board.title,
                content=updated_board.content,
                ok=True,
                message="Board updated successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))
