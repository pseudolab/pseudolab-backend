from fastapi import APIRouter, Depends, Path

from .schema import CreateBingoBoardRequest, UpdateBingoBoardRequest, BingoBoardResponse
from .services import (
    CreateBingoBoard,
    GetBingoBoardByUserId,
    UpdateBingoBoardByUserId,
    UpdateBingoCount,
    GetUserSelectedWords,
)


bingo_boards_router = APIRouter(prefix="/bingo/boards", tags=["bingo"])


@bingo_boards_router.post("/", response_model=BingoBoardResponse, status_code=201)
async def create_board(
    data: CreateBingoBoardRequest,
    bingo_boards: CreateBingoBoard = Depends(CreateBingoBoard),
):
    return await bingo_boards.execute(**data.model_dump())


@bingo_boards_router.get("/{user_id}", response_model=BingoBoardResponse)
async def get_board_by_user_id(
    user_id: int = Path(..., title="유저 ID", ge=1),
    bingo_boards: GetBingoBoardByUserId = Depends(GetBingoBoardByUserId),
):
    return await bingo_boards.execute(user_id)


@bingo_boards_router.put("/{user_id}", response_model=BingoBoardResponse)
async def update_board_by_user_id(
    data: UpdateBingoBoardRequest,
    bingo_boards: UpdateBingoBoardByUserId = Depends(UpdateBingoBoardByUserId),
):
    return await bingo_boards.execute(**data.model_dump())


@bingo_boards_router.put("/bingo_count/{user_id}", response_model=BingoBoardResponse)
async def update_bingo_count(
    user_id: int = Path(..., title="유저 ID", ge=1),
    bingo_boards: UpdateBingoCount = Depends(UpdateBingoCount),
):
    return await bingo_boards.execute(user_id)


@bingo_boards_router.get("/selected_words/{user_id}")
async def get_user_selected_words(
    user_id: int = Path(..., title="유저 ID", ge=1),
    bingo_boards: GetUserSelectedWords = Depends(GetUserSelectedWords),
) -> list[str]:
    return await bingo_boards.execute(user_id)
