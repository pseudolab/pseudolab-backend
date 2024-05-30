from fastapi import APIRouter, Depends, Path

from .schema import (
    BoardResponse,
    BoardRequest,
)
from .services import (
    CreateBoard,
    GetBoardByBoardId,
    UpdateBoardByBoardId,
)


boards_router = APIRouter(prefix="/board", tags=["board"])


@boards_router.post("", response_model=BoardResponse)
async def create_board(
    data: BoardRequest,
    boards: CreateBoard = Depends(CreateBoard),
):
    return await boards.execute(**data.model_dump())


@boards_router.get("/{board_id}", response_model=BoardResponse)
async def get_board_by_board_id(
    board_id: int = Path(..., title="게시판 ID", ge=1),
    boards: GetBoardByBoardId = Depends(GetBoardByBoardId),
    password: int = "0000",
):
    return await boards.execute(board_id, password)


@boards_router.put("/{board_id}", response_model=BoardResponse)
async def update_board_by_board_id(
    data: BoardRequest,
    boards: UpdateBoardByBoardId = Depends(UpdateBoardByBoardId),
):
    return await boards.execute(**data.model_dump())
