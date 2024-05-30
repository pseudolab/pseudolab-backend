from fastapi import APIRouter, Depends, Path, Query

from .schema import (
    BoardResponse,
    BoardRequest,
)
from .services import (
    CreateBoard,
    GetBoardByBoardId,
    UpdateBoardByBoardId,
    DeleteBoardByBoardId,
)


boards_router = APIRouter(prefix="/board", tags=["board"])


@boards_router.post("", response_model=BoardResponse)
async def create_board(
    data: BoardRequest,
    boards: CreateBoard = Depends(CreateBoard),
):
    return await boards.execute(**data.model_dump())


@boards_router.get("/{board_id}", response_model=BoardResponse)
async def get_board_by_board_id_with_password(
    board_id: int = Path(..., title="board_id ID", ge=1),
    password: str = Query(..., description="Password to access the board"),
    boards: GetBoardByBoardId = Depends(GetBoardByBoardId),
):
    return await boards.execute(board_id, password)


@boards_router.put("/{board_id}", response_model=BoardResponse)
async def update_board_by_board_id(
    data: BoardRequest,
    board_id: int = Path(..., title="Board ID", ge=1),
    boards: UpdateBoardByBoardId = Depends(UpdateBoardByBoardId),
):
    return await boards.execute(board_id, **data.model_dump())


@boards_router.delete("/{board_id}", response_model=BoardResponse)
async def update_board_by_board_id(
    board_id: int = Path(..., title="Board ID", ge=1),
    password: str = Query(..., description="Password to delete the board"),
    boards: DeleteBoardByBoardId = Depends(DeleteBoardByBoardId),
):
    return await boards.execute(board_id, password)
