from core.db import AsyncSessionDepends
from models.board import Boards
from api.board.crud.schema import (
    BoardResponse,
    BoardListResponse,
    BoardListItemResponse,
)


class BaseBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoard(BaseBoard):
    async def execute(self, title: str, author: str, contents: str, password: int) -> BoardResponse:
        try:
            board = await Boards.create(self.async_session, title, author, contents, password)
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                author=board.author,
                contents=board.contents,
                view_count=board.view_count,
                created_at=board.created_at,
                ok=True,
                message="Board created successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int) -> BoardResponse:
        try:
            board = await Boards.get_board_by_board_id(self.async_session, board_id)
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                contents=board.contents,
                view_count=board.view_count,
                ok=True,
                message="Board retrieved successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class GetBoardByBoardIdWithPassword(BaseBoard):
    async def execute(self, board_id: int, password: str) -> BoardResponse:
        try:
            board = await Boards.get_board_by_board_id_with_password(self.async_session, board_id, password)
            if board.password != password:
                return BoardResponse(ok=False, message=str("Incorrect password"))
            return BoardResponse(
                board_id=board.board_id,
                title=board.title,
                contents=board.contents,
                view_count=board.view_count,
                ok=True,
                message="Board retrieved successfully.",
            )
        except ValueError as e:
            return BoardResponse(ok=False, message=str(e))


class UpdateBoardByBoardId(BaseBoard):
    async def execute(self, board_id: int, title: str, contents: str, password: int) -> BoardResponse:
        try:
            board = await Boards.get_board_by_board_id_with_password(self.async_session, board_id, password)
            if board.password != password:
                raise BoardResponse(ok=False, message="Incorrect password")
            updated_board = await Boards.update_board_by_board_id(
                self.async_session, board_id, title, contents, password
            )
            return BoardResponse(
                board_id=updated_board.board_id,
                title=updated_board.title,
                contents=updated_board.contents,
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
                contents=deleted_board.contents,
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
                BoardListItemResponse(
                    board_id=board.board_id,
                    title=board.title,
                    author=board.author,
                    created_at=board.created_at,
                    view_count=board.view_count,
                    comment_count=len(board.comments),
                    like_count=board.like_count,
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
