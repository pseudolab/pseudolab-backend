from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BoardSchema(BaseModel):
    board_id: int
    title: str
    content: str
    password: str
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)


class BoardCommentSchema(BaseModel):
    board_id: int
    comment_id: int
    content: str
    password: str
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)
