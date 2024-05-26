from fastapi import APIRouter, Depends, Path

from .schema import (
    BoardResponse,
)


boards_router = APIRouter(prefix="/board", tags=["board"])


@boards_router.post("", response_model=BoardResponse)
async def create_board():
    pass


@boards_router.get("/{board_id}", response_model=BoardResponse)
async def get_board_by_board_id():
    pass


@boards_router.put("/{board_id}", response_model=BoardResponse)
async def update_board_by_board_id():
    pass
