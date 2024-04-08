from core.db import AsyncSessionDepends
from models.bingo import BingoBoards
from api.bingo.bingo_boards.schema import BingoBoardResponse, UpdateBingoCountResponse, UserSelectedWordsResponse


class BaseBingoBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBingoBoard(BaseBingoBoard):
    async def execute(self, user_id: int, board_data: dict) -> BingoBoards:
        try:
            res = await BingoBoards.create(self.async_session, user_id, board_data)
            return BingoBoardResponse(**res.__dict__, ok=True, message="빙고판 생성에 성공하였습니다.")
        except ValueError as e:
            return BingoBoardResponse(ok=False, message=str(e))


class GetBingoBoardByUserId(BaseBingoBoard):
    async def execute(self, user_id: int) -> BingoBoards:
        try:
            res = await BingoBoards.get_board_by_userid(self.async_session, user_id)
            return BingoBoardResponse(**res.__dict__, ok=True, message="빙고판 조회에 성공하였습니다.")
        except ValueError as e:
            return BingoBoardResponse(ok=False, message=str(e))


class UpdateBingoBoardByUserId(BaseBingoBoard):
    async def execute(self, user_id: int, board_data: dict) -> BingoBoards:
        try:
            res = await BingoBoards.update_board_by_userid(self.async_session, user_id, board_data)
            return BingoBoardResponse(**res.__dict__, ok=True, message="빙고판 수정에 성공하였습니다.")
        except ValueError as e:
            return BingoBoardResponse(ok=False, message=str(e))


class UpdateBingoCount(BaseBingoBoard):
    async def execute(self, user_id: int) -> bool:
        try:
            res = await BingoBoards.update_bingo_count(self.async_session, user_id)
            return UpdateBingoCountResponse(**res.__dict__, ok=True, message="빙고 갯수 업데이트에 성공하였습니다.")
        except ValueError as e:
            return UpdateBingoCountResponse(ok=False, message=str(e))


class GetUserSelectedWords(BaseBingoBoard):
    async def execute(self, user_id: int) -> BingoBoards:
        try:
            res = await BingoBoards.get_user_selected_words(self.async_session, user_id)
            return UserSelectedWordsResponse(selected_words=res, ok=True, message="선택한 단어 조회에 성공하였습니다.")
        except ValueError as e:
            return UserSelectedWordsResponse(ok=False, message=str(e))
