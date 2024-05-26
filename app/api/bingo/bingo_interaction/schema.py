from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from core.base_schema import BaseSchema


class BingoInteractionRequest(BaseModel):
    word_id_list: str = Field(..., title="빙고 인터렉션에 사용될 단어 리스트")
    send_user_id: int = Field(..., title="인터렉션을 보낸 유저 ID")
    receive_user_id: int = Field(..., title="인터렉션을 받는 유저 ID")
