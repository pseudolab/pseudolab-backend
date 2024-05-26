from fastapi import APIRouter, Depends, Path

from .schema import BingoInteractionRequest
from .services import CreateBingoInteraction


bingo_interaction_router = APIRouter(prefix="/bingo/interactions", tags=["bingo"])


@bingo_interaction_router.post("")
async def create_board(
    data: BingoInteractionRequest,
    bingo_boards: CreateBingoInteraction = Depends(CreateBingoInteraction),
):
    print(data)
    return await bingo_boards.execute(**data.model_dump())
