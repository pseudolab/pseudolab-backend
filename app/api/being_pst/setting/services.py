from core.db import AsyncSessionDepends
from models.being_pst import PstCategory, PstSentence
from api.being_pst.setting.schema import PstCategoryResponse, PstSentenceResponse


class BaseBeingPstSetting:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session


class CreateCategory(BaseBeingPstSetting):
    async def execute(self, category: str) -> PstCategory:
        try:
            res = await PstCategory.create(self.async_session, category)
            return PstCategoryResponse(**res.__dict__, ok=True, message="카테고리 생성에 성공하였습니다.")
        except ValueError as e:
            return PstCategoryResponse(ok=False, message=str(e))

class CreateSentence(BaseBeingPstSetting):
    async def execute(self, category_id: int, content: str) -> PstSentence:
        try:
            res = await PstSentence.create(self.async_session, category_id, content)
            return PstSentenceResponse(**res.__dict__, ok=True, message="문장 생성에 성공하였습니다.")
        except ValueError as e:
            return PstSentenceResponse(ok=False, message=str(e))