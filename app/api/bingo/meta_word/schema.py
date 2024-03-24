from pydantic import BaseModel, Field

from models import MetaWordSchema


class CreateMetaWordRequest(BaseModel):
    word_type: int = Field(..., title="단어 타입")
    word: str = Field(..., title="단어")


class CreateMetaWordResponse(BaseModel):
    word_id: int = Field(..., title="단어 ID")
    word_type: int = Field(..., title="단어 타입")
    word: str = Field(..., title="단어")


class MetaWordsListResponse(BaseModel):
    meta_words: list[MetaWordSchema]
