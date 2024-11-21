from fastapi import APIRouter, Depends, Path

from .schema import (
    BingoBoardRequest,
    BingoBoardResponse,
    UpdateBingoCountResponse,
    UserSelectedWordsResponse,
    UpdateBingoStatusResponse,
    UpdateBingoStatusResponseByQRScan,
    GetUserBingoEventUser,
)
from .services import (
    CreateBingoBoard,
    GetBingoBoardByUserId,
    UpdateBingoBoardByUserId,
    UpdateBingoCount,
    GetUserSelectedWords,
    UpdateBingoStatusBySelectedUser,
    GetBingoEventUser,
    UpdateBingoStatusByQRScan,
)


bingo_boards_router = APIRouter(prefix="/bingo/boards", tags=["bingo"])


@bingo_boards_router.post("", response_model=BingoBoardResponse)
async def create_board(
    data: BingoBoardRequest,
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
    data: BingoBoardRequest,
    bingo_boards: UpdateBingoBoardByUserId = Depends(UpdateBingoBoardByUserId),
):
    return await bingo_boards.execute(**data.model_dump())


@bingo_boards_router.put("/bingo_count/{user_id}", response_model=UpdateBingoCountResponse)
async def update_bingo_count(
    user_id: int = Path(..., title="유저 ID", ge=0),
    bingo_boards: UpdateBingoCount = Depends(UpdateBingoCount),
):
    return await bingo_boards.execute(user_id)


@bingo_boards_router.get("/selected_words/{user_id}", response_model=UserSelectedWordsResponse)
async def get_user_selected_words(
    user_id: int = Path(..., title="유저 ID", ge=0),
    bingo_boards: GetUserSelectedWords = Depends(GetUserSelectedWords),
):
    return await bingo_boards.execute(user_id)


@bingo_boards_router.put("/bingo_status/{send_user_id}/{receive_user_id}", response_model=UpdateBingoStatusResponse)
async def update_bingo_status(
    send_user_id: int = Path(..., title="요청 유저 ID", ge=0),
    receive_user_id: int = Path(..., title="대상 유저 ID", ge=0),
    bingo_boards: UpdateBingoStatusBySelectedUser = Depends(UpdateBingoStatusBySelectedUser),
):
    return await bingo_boards.execute(send_user_id, receive_user_id)


@bingo_boards_router.get("/bingo_event_users/{bingo_count}", response_model=GetUserBingoEventUser)
async def get_bingo_event_users(
    bingo_count: int = Path(..., title="이벤트 조건 빙고 갯수", ge=0),
    bingo_boards: GetBingoEventUser = Depends(GetBingoEventUser),
):
    return await bingo_boards.execute(bingo_count)


@bingo_boards_router.patch("/update/{user_id}/{booth_id}", response_model=UpdateBingoStatusResponseByQRScan)
async def update_bingo_status_booth(
    user_id: int = Path(..., title="요청 유저 ID", ge=0),
    booth_id: int = Path(..., title="요청 부스 ID", ge=0),
    bingo_boards: UpdateBingoStatusByQRScan = Depends(UpdateBingoStatusByQRScan),
):
    return await bingo_boards.execute(user_id, booth_id)
