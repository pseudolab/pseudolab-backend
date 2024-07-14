import os
from asyncio import current_task
from core.log import log
from typing import Annotated, AsyncIterator
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
    AsyncSession,
)

from dotenv import load_dotenv
from models.base import Base

load_dotenv("config/.env", override=True)


class Database:
    def __init__(self):
        self.async_engine = None
        self.async_session_factory = None
        self.async_scoped_session = None

    def initialize(self):
        self.async_engine = create_async_engine(
            os.getenv("DB_URL"),
            pool_pre_ping=True,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine, autoflush=False, future=True, expire_on_commit=False, class_=AsyncSession
        )
        self.async_scoped_session = async_scoped_session(self.async_session_factory, scopefunc=current_task)

    async def create_database(self) -> None:
        if os.getenv("ENV") == "test":
            async with self.async_engine.begin() as conn:
                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

    async def reset_database(self) -> None:
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_scoped_session() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                log.error(e)
                await session.rollback()
            finally:
                await session.close()


db = Database()
AsyncSessionDepends = Annotated[AsyncSession, Depends(db.get_session)]
