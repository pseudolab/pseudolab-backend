from fastapi import APIRouter, Depends, Path, HTTPException

from .schema import (
    BingoBoardRequest,
    BingoBoardResponse,
    UpdateBingoCountResponse,
    UserSelectedWordsResponse,
    UpdateBingoStatusResponse,
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

import random
@bingo_boards_router.patch("/update/{booth_id}")
async def update_bingo_status(
    booth_id: str,
    update_bingo_boards: UpdateBingoBoardByUserId = Depends(UpdateBingoBoardByUserId),
    get_bingo_boards: GetBingoBoardByUserId = Depends(GetBingoBoardByUserId),
):
    booth_exist = False
    not_selected_ids = []
    # TODO: get user_id
    user_id = 6

    # get board_data, check user_id is already have booth bingo
    data = await get_bingo_boards.execute(user_id)
    board_data = data.board_data
    for idx, bingo_dict in board_data.items():
        value, status = bingo_dict["value"], bingo_dict["status"]
        if value == f'Booth {booth_id}':
            booth_exist = True
            break
        if status == 0:
            # get not selected list
            not_selected_ids.append(idx)
    
    if not booth_exist:
        # update random board data
        booth_idx = random.choice(not_selected_ids)
        print('update idx', booth_idx)
        board_data[booth_idx]["value"] = f'Booth {booth_id}'
        board_data[booth_idx]["status"] = 1
        print('update board_data', board_data)
        new_data = BingoBoardRequest(
            user_id=user_id,
            board_data=board_data
        )
        print('update!')
        return await update_bingo_boards.execute(**new_data.model_dump())
    else:
        # not update
        print('not update!')
        return