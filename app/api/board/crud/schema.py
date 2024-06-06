from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from core.base_schema import BaseSchema
from api.board.comment.schema import BoardCommentResponse


class BoardRequest(BaseModel):
    title: str
    author: str = Field(default="anonymous", description="Author of the board")
    contents: str
    password: str = Field(default="0000", description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardUpdateRequest(BaseModel):
    title: str
    contents: str
    password: str = Field(..., description="Password must be a 4-digit number")

    @field_validator("password")
    def password_must_be_4_digits(cls, v):
        if len(v) != 4 or not v.isdigit():
            raise ValueError("Password must be a 4-digit number")
        return v


class BoardResponse(BaseSchema):
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    title: Optional[str] = Field(title="제목", default=None)
    author: Optional[str] = Field(title="작성자", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    view_count: Optional[int] = Field(title="조회수", default=None)
    contents: Optional[str] = Field(title="내용", default=None)
    comment_list: List[BoardCommentResponse]


class BoardListItemResponse(BaseSchema):
    board_id: Optional[int] = Field(title="게시판 ID", default=None)
    title: Optional[str] = Field(title="제목", default=None)
    author: Optional[str] = Field(title="작성자", default=None)
    created_at: Optional[int] = Field(title="생성일", default=None)
    view_count: Optional[int] = Field(title="조회수", default=None)
    comment_count: Optional[int] = Field(title="댓글수", default=None)
    like_count: Optional[int] = Field(title="좋아요 수", default=None)


class BoardListResponse(BaseSchema):
    boards: List[BoardListItemResponse]
    all_count: int
