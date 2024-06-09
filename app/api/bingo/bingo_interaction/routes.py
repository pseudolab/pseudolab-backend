from fastapi import APIRouter, Depends, Path

from .schema import BingoInteractionRequest
from .services import CreateBingoInteraction, GetUserLatestInteraction


bingo_interaction_router = APIRouter(prefix="/bingo/interactions", tags=["bingo"])


@bingo_interaction_router.post("")
async def create_bingo_interaction(
    data: BingoInteractionRequest,
    bingo_interaction: CreateBingoInteraction = Depends(CreateBingoInteraction),
):
    return await bingo_interaction.execute(**data.model_dump())


@bingo_interaction_router.get("/{user_id}")
async def get_user_latest_interaction(
    user_id: int = Path(..., title="유저 아이디"),
    bingo_interaction: GetUserLatestInteraction = Depends(GetUserLatestInteraction),
):
    return await bingo_interaction.execute(user_id=user_id)
