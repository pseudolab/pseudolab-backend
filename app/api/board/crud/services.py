from core.db import AsyncSessionDepends
from models.board import Boards
from api.board.crud.schema import (
    BoardResponse,
    BoardListResponse,
)


class BaseBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoard(BaseBoard):
    async def execute(self, title: str, author: str, content: str, password: int) -> BoardResponse:
        try:
            board = await Boards.create(self.async_session, title, author, content, password)
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                author=board.author,
                content=board.content,
                view_count=board.view_count,
                ok=True,
                message="Board created successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, password: str) -> BoardResponse:
        try:
            board = await Boards.get_board_by_board_id_with_password(self.async_session, board_id, password)
            if board.password != password:
                return BoardResponse(ok=False, message=str("Incorrect password"))
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                content=board.content,
                view_count=board.view_count,
                ok=True,
                message="Board retrieved successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class UpdateBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, title: str, content: str, password: int) -> BoardResponse:
        try:
            board = await Boards.get_board_by_board_id_with_password(self.async_session, board_id, password)
            if board.password != password:
                raise BoardResponse(ok=False, message="Incorrect password")
            updated_board = await Boards.update_board_by_board_id(
                self.async_session, board_id, title, content, password
            )
            return BoardResponse(
                board_id=updated_board.board_id,
                title=updated_board.title,
                content=updated_board.content,
                ok=True,
                message="Board updated successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class DeleteBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, password: str) -> BoardResponse:
        try:
            deleted_board = await Boards.delete_board_by_board_id(self.async_session, board_id, password)
            return BoardResponse(
                board_id=deleted_board.board_id,
                title=deleted_board.title,
                content=deleted_board.content,
                ok=True,
                message="Board deleted successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetAllBoards(BaseBoard):
    async def execute(self) -> BoardListResponse:
        try:
            boards = await Boards.get_all_boards(self.async_session)
            boards_response = [
                BoardResponse(
                    board_id=board.board_id,
                    title=board.title,
                    content=board.content,
                    ok=True,
                    message="Board retrieved successfully.",
                )
                for board in boards
            ]
            return BoardListResponse(
                boards=boards_response,
                all_count=len(boards_response),
                ok=True,
                message="All boards retrieved successfully.",
            )
        except Exception as e:
            return BoardListResponse(boards=[], all_count=0, ok=False, message=str(e))
