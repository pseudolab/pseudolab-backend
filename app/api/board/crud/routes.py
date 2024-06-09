from fastapi import APIRouter, Depends, Path, Query

from .schema import (
    BoardResponse,
    BoardListResponse,
    BoardRequest,
    BoardUpdateRequest,
)
from .services import (
    CreateBoard,
    GetBoardByBoardId,
    UpdateBoardByBoardId,
    DeleteBoardByBoardId,
    GetAllBoards,
    GetPageBoards,
)

boards_router = APIRouter(prefix="/board", tags=["board"])


@boards_router.post("", response_model=BoardResponse)
async def create_board(
    data: BoardRequest,
    boards: CreateBoard = Depends(CreateBoard),
):
    return await boards.execute(**data.model_dump())


@boards_router.get("/all", response_model=BoardListResponse)
async def get_all_boards(
    boards: GetAllBoards = Depends(GetAllBoards),
):
    return await boards.execute()


# TODO : Offset 아니라 Where 사용?
@boards_router.get("/list", response_model=BoardListResponse)
async def get_page_boards(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of boards per page"),
    boards: GetPageBoards = Depends(GetPageBoards),
):
    return await boards.execute(page, page_size)


@boards_router.get("/{board_id}", response_model=BoardResponse)
async def get_board_by_board_id(
    board_id: int = Path(..., title="Board ID", ge=1),
    boards: GetBoardByBoardId = Depends(GetBoardByBoardId),
):
    return await boards.execute(board_id)


@boards_router.put("/{board_id}", response_model=BoardResponse)
async def update_board_by_board_id(
    data: BoardUpdateRequest,
    board_id: int = Path(..., title="Board ID", ge=1),
    boards: UpdateBoardByBoardId = Depends(UpdateBoardByBoardId),
):
    return await boards.execute(board_id, **data.model_dump())


@boards_router.delete("/{board_id}", response_model=BoardResponse)
async def delete_board_by_board_id(
    board_id: int = Path(..., title="Board ID", ge=1),
    password: str = Query(..., description="Password to delete the board"),
    boards: DeleteBoardByBoardId = Depends(DeleteBoardByBoardId),
):
    return await boards.execute(board_id, password)
