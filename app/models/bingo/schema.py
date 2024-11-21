from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MetaWordSchema(BaseModel):
    word_id: int
    word_type: int
    word: str

    model_config = ConfigDict(from_attributes=True)


class BingoBoardSchema(BaseModel):
    user_id: int
    board_data: dict
    bingo_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BingoInteractionSchema(BaseModel):
    send_user_id: int
    receive_user_id: int
    updated_words: list[str]
    bingo_count: int


class BingoQRScanSchema(BaseModel):
    user_id: int
    booth_id: int
    updated_words: list[str]
    bingo_count: int


class BingoEventUserInfo(BaseModel):
    rank: int
    user_name: str
    bingo_count: int
