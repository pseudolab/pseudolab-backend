from typing import Optional
from pydantic import BaseModel, Field

from core.base_schema import BaseSchema


class BoardRequest(BaseModel):
    board_id: int

    class Config:
        orm_mode = True


class BoardResponse(BaseSchema):
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    title: Optional[str] = Field(title="제목", default=None)
    content: Optional[str] = Field(title="내용", default=None)
    password: Optional[str] = Field(title="비밀 번호", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    updated_at: Optional[int] = Field(title="수정일", default=None)
