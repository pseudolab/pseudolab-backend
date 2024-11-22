from core.db import AsyncSessionDepends
from models.bingo import BingoBoards
from api.bingo.bingo_boards.schema import BingoBoardRequest, BingoBoardResponse, UpdateBingoCountResponse, UserSelectedWordsResponse, UpdateBingoStatusResponse, GetUserBingoEventUser, UpdateBingoStatusResponseByQRScan


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

class UpdateBingoStatusBySelectedUser(BaseBingoBoard):
    async def execute(self, send_user_id: int, receive_user_id: int) -> BingoBoards:
        try:
            res = await BingoBoards.update_bingo_status_by_selected_user(self.async_session, send_user_id, receive_user_id)
            return UpdateBingoStatusResponse(**res.__dict__, ok=True, message="빙고판 상태 업데이트에 성공하였습니다.")
        except ValueError as e:
            return UpdateBingoStatusResponse(ok=False, message=str(e))

class GetBingoEventUser(BaseBingoBoard):
    async def execute(self, bingo_count: int) -> list[str]:
        try:
            res = await BingoBoards.get_bingo_event_users(self.async_session, bingo_count)
            return GetUserBingoEventUser(bingo_event_users=res, ok=True, message="빙고 이벤트 당첨 유저 목록 생성에 성공하였습니다.")
        except ValueError as e:
            return GetUserBingoEventUser(ok=False, message=str(e))
        
class UpdateBingoStatusByQRScan(BaseBingoBoard):
    async def execute(self, user_id: int, booth_id: int) -> BingoBoards:
        try:
            res = await BingoBoards.update_bingo_status_by_qr_scan(self.async_session, user_id, booth_id)
            return UpdateBingoStatusResponseByQRScan(**res.__dict__, ok=True, message="빙고판 상태 업데이트에 성공하였습니다.")
        except ValueError as e:
            return UpdateBingoStatusResponseByQRScan(ok=False, message=str(e))
