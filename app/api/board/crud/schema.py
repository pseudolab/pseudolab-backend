from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from core.base_schema import BaseSchema


class BoardRequest(BaseModel):
    title: str
    author: str = Field(default="anonymous", description="Author of the board")
    content: str
    password: str = Field(default="0000", description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardResponse(BaseSchema):
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    author: Optional[str] = Field(title="작성자", default=None)
    view_count: Optional[int] = Field(title="조회수", default=None)
    title: Optional[str] = Field(title="제목", default=None)
    content: Optional[str] = Field(title="내용", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    updated_at: Optional[int] = Field(title="수정일", default=None)


class BoardListResponse(BaseSchema):
    boards: List[BoardResponse]
    all_count: int
