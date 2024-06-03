from models.base import Base
from core.db import AsyncSession
from sqlalchemy import Integer, String, select, DateTime, Boolean, Sequence
from sqlalchemy.orm import mapped_column
from typing import AsyncIterator

from datetime import datetime
from zoneinfo import ZoneInfo


class BingoUser(Base):
    __tablename__ = "bingo_user"
    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    username = mapped_column(String(100), nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )

    @classmethod
    async def create(cls, session: AsyncSession, username: str):
        is_user = await session.execute(select(cls).where(cls.username == username))
        is_user = is_user.one_or_none()
        if is_user:
            raise ValueError(f"{username}은 이미 존재하는 유저입니다. 이름에 2를 붙여 가입해주세요.")
        new_user = BingoUser(username=username)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def get_user_by_name(cls, session: AsyncSession, username: str):
        res = await session.execute(select(cls).where(cls.username == username))
        user = res.scalars().first()
        if not user:
            raise ValueError(f"{username} 의 빙고 유저가 존재하지 않습니다.")
        return user

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        res = await session.get(cls, user_id)
        if not res:
            raise ValueError(f"{user_id} 의 빙고 유저가 존재하지 않습니다.")
        return res


class User(Base):
    __tablename__ = "user"

    user_id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(120), unique=True, index=True, nullable=False)
    username = mapped_column(String(100), nullable=False)
    nickname = mapped_column(String(30), nullable=False)
    phone_number = mapped_column(String(20), nullable=True)
    notion_id = mapped_column(String(100), nullable=True)
    discord_id = mapped_column(String(100), nullable=True)
    enabled = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        stmt = select(cls).where(cls.id == user_id)
        result = await session.execute(stmt)
        return result.sclar()

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        stmt = select(cls).where(cls.email == email)
        result = await session.execute(stmt)
        return result.one_or_none()
