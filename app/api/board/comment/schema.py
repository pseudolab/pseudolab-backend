from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from core.base_schema import BaseSchema


class BoardCommentRequest(BaseModel):
    author: str = Field(default="anonymous", description="Author of the comment")
    contents: str
    password: str = Field(default="0000", description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardCommentUpdateRequest(BaseModel):
    contents: str
    password: str = Field(..., description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardCommentResponse(BaseSchema):
    comment_id: Optional[int] = Field(title="댓글 ID", default=None)
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    author: Optional[str] = Field(title="작성자", default=None)
    contents: Optional[str] = Field(title="내용", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)


class BoardCommentListResponse(BaseSchema):
    comments: List[BoardCommentResponse]
    all_count: int
