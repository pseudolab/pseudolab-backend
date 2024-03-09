from models.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column


class MetaWord(Base):
    __tablename__ = "meta_word"

    word_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_type = mapped_column(Integer, nullable=False, default=0)
    word = mapped_column(String(200), nullable=False)
