from __future__ import annotations

from typing import AsyncIterator

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import mapped_column

from core.db import AsyncSession
from models.base import Base


class MetaWord(Base):
    __tablename__ = "meta_word"

    word_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_type = mapped_column(Integer, nullable=False, default=0)
    word = mapped_column(String(200), nullable=False, unique=True)

    @classmethod
    async def create(cls, session: AsyncSession, word_type: int, word: str) -> MetaWord:
        new_word = MetaWord(word_type=word_type, word=word)
        session.add(new_word)
        created_word = await cls.get_word_by_id(session, new_word.word_id)
        return created_word

    @classmethod
    async def get_word_by_id(cls, session: AsyncSession, word_id: int):
        return await session.get(cls, word_id)

    @classmethod
    async def get_words_by_type(cls, session: AsyncSession, word_type: int) -> AsyncIterator[MetaWord]:
        stmt = select(cls).where(cls.word_type == word_type)
        stream = await session.stream_scalars(stmt.order_by(cls.word_id))
        async for row in stream:
            yield row
