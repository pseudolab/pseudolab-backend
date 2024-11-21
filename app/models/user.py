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
    password = mapped_column(String(100), nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )

    @classmethod
    async def create(cls, session: AsyncSession, username: str, password: str):
        is_user = await session.execute(select(cls).where(cls.username == username))
        is_user = is_user.one_or_none()
        if is_user:
            raise ValueError(f"{username}은 이미 존재하는 유저입니다. 다른 이름을 사용해주세요.")
        new_user = BingoUser(username=username, password=password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def get_user_by_name(cls, session: AsyncSession, username: str):
        res = await session.execute(select(cls).where(cls.username == username))
        user = res.scalars().first()
        return user

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        res = await session.execute(select(cls).where(cls.user_id == user_id))
        user = res.scalars().first()
        if not user:
            raise ValueError(f"{user_id} 의 빙고 유저가 존재하지 않습니다.")
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

    access_token = mapped_column(String(255), nullable=True)
    refresh_token = mapped_column(String(255), nullable=True)
    access_token_expires_at = mapped_column(DateTime, nullable=True)
    refresh_token_expires_at = mapped_column(DateTime, nullable=True)

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        stmt = select(cls).where(cls.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        stmt = select(cls).where(cls.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def update_tokens(
        cls,
        session: AsyncSession,
        user_id: int,
        access_token: str,
        refresh_token: str,
        access_expires: datetime,
        refresh_expires: datetime,
    ):
        stmt = select(cls).where(cls.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()
        if user:
            user.access_token = access_token
            user.refresh_token = refresh_token
            user.access_token_expires_at = access_expires
            user.refresh_token_expires_at = refresh_expires
            await session.commit()
            await session.refresh(user)
        return user
