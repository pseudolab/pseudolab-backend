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
    bingo_count: int = Field(..., title="빙고 갯수")
    created_at: datetime = Field(..., title="생성일")
    updated_at: datetime = Field(..., title="수정일")
