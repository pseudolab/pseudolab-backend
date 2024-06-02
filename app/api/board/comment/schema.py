from typing import Optional
from pydantic import BaseModel, Field, field_validator
from core.base_schema import BaseSchema


class BoardCommentRequest(BaseModel):
    content: str
    password: str = Field(..., description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardCommentResponse(BaseSchema):
    comment_id: Optional[int] = Field(title="게시판 ID", default=None)
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    content: Optional[str] = Field(title="내용", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    updated_at: Optional[int] = Field(title="수정일", default=None)
