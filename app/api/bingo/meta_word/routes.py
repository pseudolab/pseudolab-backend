from fastapi import APIRouter, Depends, Path, Request

from models import MetaWordSchema

from .schema import CreateMetaWordRequest, CreateMetaWordResponse, MetaWordsListResponse
from .services import CreateMetaWord, GetMetaWordsByType

meta_word_router = APIRouter(prefix="/bingo", tags=["bingo"])


@meta_word_router.get("/")
async def read_root():
    return {"message": "Hello World"}


@meta_word_router.post("/meta_word", response_model=CreateMetaWordResponse, status_code=201)
async def create_meta_word(
    data: CreateMetaWordRequest, use_case: CreateMetaWord = Depends(CreateMetaWord)
) -> CreateMetaWordResponse:
    return await use_case.execute(**data.model_dump())


@meta_word_router.get("/meta_word/{word_type}", response_model=MetaWordsListResponse)
async def get_meta_words_by_type(
    word_type: int = Path(..., title="단어 타입", ge=0, le=3),
    use_case: GetMetaWordsByType = Depends(GetMetaWordsByType),
) -> list[MetaWordsListResponse]:
    return MetaWordsListResponse(meta_words=[meta_word async for meta_word in use_case.execute(word_type)])
