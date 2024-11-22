from core.db import AsyncSessionDepends
from models.user import BingoUser
from api.auth.schema import BingoUser as BingoUserResponse


class BaseBingoUser:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class LoginUser(BaseBingoUser):
    async def execute(self, username: str, password: str) -> BingoUser:
        try:
            user = await BingoUser.get_user_by_name(self.async_session, username)
            if not user:
                user = await BingoUser.create(self.async_session, username, password)
            elif password != user.password:
                raise ValueError("password가 잘못되었습니다.")
            return BingoUserResponse(**user.__dict__, ok=True, message="빙고 유저 생성에 성공하였습니다.")
        except ValueError as e:
            return BingoUserResponse(ok=False, message=str(e))


class GetBingoUserByName(BaseBingoUser):
    async def execute(self, username: str) -> BingoUser:
        try:
            user = await BingoUser.get_user_by_name(self.async_session, username)
            if user is None:
                raise ValueError(f"{user} 가 존재하지 않습니다.")

            return BingoUserResponse(**user.__dict__, ok=True, message="빙고 유저 조회에 성공하였습니다.")
        except ValueError as e:
            return BingoUserResponse(ok=False, message=str(e))


class GetBingoUserById(BaseBingoUser):
    async def execute(self, user_id: int) -> BingoUser:
        try:
            user = await BingoUser.get_user_by_id(self.async_session, user_id)
            return BingoUserResponse(**user.__dict__, ok=True, message="빙고 유저 조회에 성공하였습니다.")
        except ValueError as e:
            return BingoUserResponse(ok=False, message=str(e))
