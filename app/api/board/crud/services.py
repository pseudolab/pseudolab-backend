from core.db import AsyncSessionDepends
from models.board import Boards
from api.board.crud.schema import (
    BoardResponse,
)


class BaseBoard:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateBoard(BaseBoard):
    async def execute(self, board_id: int, title: str, content: str, password: int) -> Boards:
        pass
