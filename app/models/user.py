from app.models.base import Base
from app.core.db import AsyncSessionDepends
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import mapped_column
from typing import AsyncIterator


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)

    @classmethod
    async def get_user_by_id(cls, session: AsyncSessionDepends, user_id: int) -> User | None:
        stmt = select(cls).where(cls.id == user_id)
        return await session.sclar(stmt)
