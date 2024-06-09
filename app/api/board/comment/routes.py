from fastapi import APIRouter, Depends, Path, Query

from .schema import BoardCommentResponse, BoardCommentRequest, BoardCommentUpdateRequest, BoardCommentListResponse
from .services import (
    CreateBoardComment,
    GetCommentByCommentId,
    UpdateCommentByCommentId,
    DeleteCommentByCommentId,
    GetAllComments,
)


comments_router = APIRouter(prefix="/comment", tags=["comment"])


@comments_router.post("/{board_id}", response_model=BoardCommentResponse)
async def create_board_comment(
    data: BoardCommentRequest,
    board_id: int = Path(..., title="Board ID", ge=1),
    comments: CreateBoardComment = Depends(CreateBoardComment),
):
    return await comments.execute(board_id, **data.model_dump())


@comments_router.get("/{board_id}/all", response_model=BoardCommentListResponse)
async def get_all_board_comments(
    board_id: int = Path(..., title="Board ID", ge=1),
    boards: GetAllComments = Depends(GetAllComments),
):
    return await boards.execute(board_id)


@comments_router.get("/{board_id}/{comment_id}", response_model=BoardCommentResponse)
async def get_comment_by_comment_id(
    board_id: int = Path(..., title="Board ID", ge=1),
    comment_id: int = Path(..., title="Comment ID", ge=1),
    comments: GetCommentByCommentId = Depends(GetCommentByCommentId),
):
    return await comments.execute(board_id, comment_id)


@comments_router.put("/{board_id}/{comment_id}", response_model=BoardCommentResponse)
async def update_comment_by_comment_id(
    data: BoardCommentUpdateRequest,
    board_id: int = Path(..., title="Board ID", ge=1),
    comment_id: int = Path(..., title="Comment ID", ge=1),
    comments: UpdateCommentByCommentId = Depends(UpdateCommentByCommentId),
):
    return await comments.execute(board_id, comment_id, **data.model_dump())


@comments_router.delete("/{board_id}/{comment_id}", response_model=BoardCommentResponse)
async def delete_comment_by_comment_id(
    board_id: int = Path(..., title="Board ID", ge=1),
    comment_id: int = Path(..., title="Comment ID", ge=1),
    password: str = Query(..., description="Password to delete the comment"),
    comments: DeleteCommentByCommentId = Depends(DeleteCommentByCommentId),
):
    return await comments.execute(board_id, comment_id, password)
