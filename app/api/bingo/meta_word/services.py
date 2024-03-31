from typing import AsyncIterator

from core.db import AsyncSessionDepends
from models.bingo import MetaWord


class CreateMetaWord:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session

    async def execute(self, word_type: int, word: str) -> MetaWord:
        return await MetaWord.create(self.async_session, word_type, word)


class GetMetaWordsByType:
    def __init__(self, session: AsyncSessionDepends):
        self.async_session = session

    async def execute(self, word_type: int) -> AsyncIterator[MetaWord]:
        async for word in MetaWord.get_words_by_type(self.async_session, word_type):
            yield word
