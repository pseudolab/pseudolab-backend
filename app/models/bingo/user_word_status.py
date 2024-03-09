from models.base import Base
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class UserWordStatus(Base):
    __tablename__ = "user_word_status"

    user_id = mapped_column(Integer, primary_key=True, nullable=False)
    word_id = mapped_column(Integer, primary_key=True, nullable=False)
    status = mapped_column(Integer, nullable=False, default=0)
    position = mapped_column(Integer, nullable=False, default=0)
