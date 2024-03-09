from models.base import Base
from core.db import AsyncSession
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import mapped_column
from typing import AsyncIterator


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    email = mapped_column(String(120), unique=True, nullable=False)

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
