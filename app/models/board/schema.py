from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BoardSchema(BaseModel):
    board_id: int
    title: str
    author: str
    view_count: int
    comment_count: int
    like_count: int
    contents: str
    password: str
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class BoardCommentSchema(BaseModel):
    board_id: int
    comment_id: int
    contents: str
    password: str
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)
