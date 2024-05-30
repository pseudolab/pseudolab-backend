from typing import Optional
from pydantic import BaseModel, Field, validator
from core.base_schema import BaseSchema


class BoardRequest(BaseModel):
    title: str
    content: str
    password: str = Field(..., description="Password must be a 4-digit number")

    @validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardResponse(BaseSchema):
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    title: Optional[str] = Field(title="제목", default=None)
    content: Optional[str] = Field(title="내용", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    updated_at: Optional[int] = Field(title="수정일", default=None)
