from core.db import AsyncSessionDepends
from models.bingo import BingoBoards


class BaseBingoBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBingoBoard(BaseBingoBoard):
    async def execute(self, user_id: int, board_data: dict) -> BingoBoards:
        return await BingoBoards.create(self.async_session, user_id, board_data)


class GetBingoBoardByUserId(BaseBingoBoard):
    async def execute(self, user_id: int) -> BingoBoards:
        return await BingoBoards.get_board_by_userid(self.async_session, user_id)


class UpdateBingoBoardByUserId(BaseBingoBoard):
    async def execute(self, user_id: int, board_data: dict) -> BingoBoards:
        return await BingoBoards.update_board_by_userid(self.async_session, user_id, board_data)


class UpdateBingoCount(BaseBingoBoard):
    async def execute(self, user_id: int) -> bool:
        return await BingoBoards.update_bingo_count(self.async_session, user_id)


class GetUserSelectedWords(BaseBingoBoard):
    async def execute(self, user_id: int) -> BingoBoards:
        return await BingoBoards.get_user_selected_words(self.async_session, user_id)
