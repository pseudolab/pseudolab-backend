from core.db import AsyncSessionDepends
from models.bingo import BingoInteraction
from api.bingo.bingo_boards.schema import (
    BingoBoardResponse,
)


class BaseBingoInteraction:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBingoInteraction(BaseBingoInteraction):
    async def execute(self, word_id_list: str, send_user_id: int, receive_user_id: int) -> BingoInteraction:
        try:
            interaction = await BingoInteraction.create(self.async_session, word_id_list, send_user_id, receive_user_id)
            return BingoBoardResponse(**interaction.__dict__, ok=True, message="빙고 인터렉션 생성에 성공하였습니다.")
        except ValueError as e:
            return BingoBoardResponse(ok=False, message=str(e))
