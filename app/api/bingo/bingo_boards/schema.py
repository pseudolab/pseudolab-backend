from datetime import datetime
from pydantic import BaseModel, Field


class CreateBingoBoardRequest(BaseModel):
    user_id: int = Field(..., title="유저 ID")
    board_data: dict = Field(..., title="빙고판 데이터")


class UpdateBingoBoardRequest(BaseModel):
    user_id: int = Field(..., title="유저 ID")
    board_data: dict = Field(..., title="빙고판 데이터")


class BingoBoardResponse(BaseModel):
    user_id: int = Field(..., title="유저 ID")
    board_data: dict = Field(..., title="빙고판 데이터")
    is_bingo: int = Field(..., title="빙고 여부")
    created_at: datetime = Field(..., title="생성일")
    updated_at: datetime = Field(..., title="수정일")
