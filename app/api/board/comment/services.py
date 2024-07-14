from core.db import AsyncSessionDepends
from models.board import Boards, Comments
from api.board.comment.schema import (
    BoardCommentResponse,
    BoardCommentListResponse,
)


class BaseComment:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoardComment(BaseComment):
    async def execute(self, board_id: int, author: str, contents: str, password: str) -> BoardCommentResponse:
        try:
            res = await Comments.create(self.async_session, board_id, author, contents, password)
            return BoardCommentResponse(
                comment_id=res.comment_id,
                board_id=res.board_id,
                author=res.author,
                contents=res.contents,
                created_at=res.created_at,
                ok=True,
                message="Comment created successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class GetCommentByCommentId(BaseComment):
    async def execute(self, board_id: int, comment_id) -> BoardCommentResponse:
        try:
            comment = await Comments.get_comment_by_comment_id(self.async_session, board_id, comment_id)
            return BoardCommentResponse(
                comment_id=comment.comment_id,
                board_id=comment.board_id,
                contents=comment.contents,
                ok=True,
                message="Comment retrieved successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class GetCommentByCommentIdWithPassword(BaseComment):
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
                contents=comment.contents,
                ok=True,
                message="Comment retrieved successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class UpdateCommentByCommentId(BaseComment):
    async def execute(self, board_id: int, comment_id: int, contents: str, password: str) -> BoardCommentResponse:
        try:
            comment = await Comments.get_comment_by_comment_id_with_password(
                self.async_session, board_id, comment_id, password
            )
            if comment.password != password:
                raise BoardCommentResponse(ok=False, message="Incorrect password")
            updated_comment = await Comments.update_comment_by_comment_id(
                self.async_session, board_id, comment_id, contents, password
            )
            return BoardCommentResponse(
                comment_id=updated_comment.comment_id,
                board_id=updated_comment.board_id,
                contents=updated_comment.contents,
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
                comment_id=deleted_comment.comment_id,
                board_id=deleted_comment.board_id,
                contents=deleted_comment.contents,
                ok=True,
                message="Comment deleted successfully.",
            )
        except ValueError as e:
            return BoardCommentResponse(ok=False, message=str(e))


class GetAllComments(BaseComment):
    async def execute(self, board_id: int) -> BoardCommentListResponse:
        try:
            comments = await Comments.get_board_all_comments(self.async_session, board_id=board_id)
            comments_response = [
                BoardCommentResponse(
                    comment_id=comment.comment_id,
                    board_id=comment.board_id,
                    author=comment.author,
                    contents=comment.contents,
                    created_at=comment.created_at,
                    ok=True,
                    message="Comment retrieved successfully.",
                )
                for comment in comments
            ]
            return BoardCommentListResponse(
                comments=comments_response,
                all_count=len(comments_response),
                ok=True,
                message="All comments retrieved successfully.",
            )
        except Exception as e:
            return BoardCommentListResponse(comments=[], all_count=0, ok=False, message=str(e))
