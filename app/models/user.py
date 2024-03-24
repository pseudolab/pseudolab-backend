from models.base import Base
from core.db import AsyncSession
from sqlalchemy import Integer, String, select, DateTime, Boolean
from sqlalchemy.orm import mapped_column
from typing import AsyncIterator


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
