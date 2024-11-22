from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from core.base_schema import BaseSchema
from models.bingo.schema import BingoEventUserInfo


class BingoBoardRequest(BaseModel):
    user_id: int = Field(..., title="유저 ID")
    board_data: dict = Field(..., title="빙고판 데이터")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                # 동명이인(user)이 있을 수 있으므로 value 외에 user_id도 저장
                "board_data": {
                    str(i): {"value": "", "selected": 0, "status": 0, "user_id": None}
                    for i in range(25)
                }
            }
        }


class BingoBoardResponse(BaseSchema):
    user_id: Optional[int] = Field(title="유저 ID", default=None)
    board_data: Optional[dict] = Field(title="빙고판 데이터", default=None)
    bingo_count: Optional[int] = Field(title="빙고 갯수", default=None)
    created_at: Optional[datetime] = Field(title="생성일", default=None)
    updated_at: Optional[datetime] = Field(title="수정일", default=None)


class UpdateBingoCountResponse(BaseSchema):
    user_id: Optional[int] = Field(title="유저 ID", default=None)
    bingo_count: Optional[int] = Field(title="업데이트된 빙고 갯수", default=None)


class UserSelectedWordsResponse(BaseSchema):
    selected_words: Optional[list[str]] = Field(title="선택한 단어들", default=None)


class UpdateBingoStatusResponse(BaseSchema):
    send_user_id: Optional[int] = Field(title="요청 유저 ID", default=None)
    receive_user_id: Optional[int] = Field(title="대상 유저 ID", default=None)
    updated_words: Optional[list[str]] = Field(title="업데이트된 단어들", default=None)
    bingo_count: Optional[int] = Field(title="업데이트된 빙고 갯수", default=None)


class UpdateBingoStatusResponseByQRScan(UpdateBingoCountResponse):
    booth_id: Optional[int] = Field(title="요청 부스 ID", default=None)
    updated_words: Optional[list[str]] = Field(title="업데이트된 단어들", default=None)


class GetUserBingoEventUser(BaseSchema):
    bingo_event_users: Optional[list[BingoEventUserInfo]] = Field(title="빙고 이벤트 당첨 유저 목록", default=None)
