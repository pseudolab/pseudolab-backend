from typing import Optional
from datetime import datetime
from pydantic import Field

from core.base_schema import BaseSchema

class PstCategoryResponse(BaseSchema):
    category_id: Optional[int] = Field(title="카테고리 ID", default=None)
    category: Optional[str] = Field(title="카테고리", default=None)
    created_at: Optional[datetime] = Field(title="생성일", default=None)

class PstSentenceResponse(BaseSchema):
    sentence_id: Optional[int] = Field(title="단어 ID", default=None)
    category_id: Optional[int] = Field(title="카테고리 ID", default=None)
    sentence: Optional[str] = Field(title="단어", default=None)
    created_at: Optional[datetime] = Field(title="생성일", default=None)