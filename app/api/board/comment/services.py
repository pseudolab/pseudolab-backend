from core.db import AsyncSessionDepends
from models.board import Boards, Comments
from api.board.comment.schema import (
    BoardCommentResponse,
)


class BaseComment:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoardComment(BaseComment):
    async def execute(self, board_id: int, content: str, password: str) -> BoardCommentResponse:
        try:
            print(board_id, content, password)
            res = await Comments.create(self.async_session, board_id, content, password)
            return BoardCommentResponse(
                comment_id=res.comment_id,
                board_id=res.board_id,
                content=res.content,
                ok=True,
                message="Comment created successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class GetCommentByCommentId(BaseComment):
    async def execute(self, board_id: int, comment_id, password: str) -> BoardCommentResponse:
        try:
            comment = await Comments.get_comment_by_comment_id_with_password(
                self.async_session, board_id, comment_id, password
            )
            if comment.password != password:
                return BoardCommentResponse(ok=False, message=str("Incorrect password"))
            return BoardCommentResponse(
                comment_id=comment.comment_id,
                board_id=comment.board_id,
                content=comment.content,
                ok=True,
                message="Comment retrieved successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class UpdateCommentByCommentId(BaseComment):
    async def execute(self, board_id: int, comment_id: int, content: str, password: str) -> BoardCommentResponse:
        try:
            comment = await Comments.get_comment_by_comment_id_with_password(
                self.async_session, board_id, comment_id, password
            )
            if comment.password != password:
                raise BoardCommentResponse(ok=False, message="Incorrect password")
            updated_comment = await Comments.update_comment_by_comment_id(
                self.async_session, board_id, comment_id, content, password
            )
            return BoardCommentResponse(
                comment_id=updated_comment.comment_id,
                board_id=updated_comment.board_id,
                content=updated_comment.content,
                ok=True,
                message="Comment updated successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class DeleteCommentByCommentId(BaseComment):
    async def execute(self, board_id: int, comment_id: int, password: str) -> BoardCommentResponse:
        try:
            deleted_comment = await Comments.delete_comment_by_comment_id(
                self.async_session, board_id, comment_id, password
            )
            return BoardCommentResponse(
                board_id=deleted_comment.board_id,
                title=deleted_comment.title,
                content=deleted_comment.content,
                ok=True,
                message="Comment deleted successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))
