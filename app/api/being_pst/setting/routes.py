from fastapi import APIRouter, Depends, Path

from .schema import PstCategoryResponse, PstSentenceResponse
from .services import (
    CreateCategory, CreateSentence
)


being_pst_setting_router = APIRouter(prefix="/being_pst/setting", tags=["being_pst"])


##TODO 기본 json data를 생성해서 category, sentences 에 대해 미리 생성할 친구들을 작성해놓기

@being_pst_setting_router.post("/create_category", response_model=PstCategoryResponse)
async def create_category(
    category: str = Path(..., title="생성 카테고리"),
    pst_setting: CreateCategory = Depends(CreateCategory),
):
    return await pst_setting.execute(category)

@being_pst_setting_router.post("/create_sentence", response_model=PstSentenceResponse)
async def create_sentence(
    category_id: int = Path(..., title="카테고리 ID"),
    content: str = Path(..., title="생성 문장"),
    pst_setting: CreateSentence = Depends(CreateSentence),
):
    return await pst_setting.execute(category_id, content)
