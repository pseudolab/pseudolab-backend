from datetime import datetime
from zoneinfo import ZoneInfo

from models.base import Base
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import mapped_column


class BingoInteraction(Base):
    __tablename__ = "bingo_interaction"

    interaction_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_id = mapped_column(Integer, nullable=False)
    send_user_id = mapped_column(Integer, nullable=False)
    receive_user_id = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Asia/Seoul")), nullable=False
    )
