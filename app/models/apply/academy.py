from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from models.base import Base

class Period(Base):
    __tablename__ = "period"

    id = mapped_column(Integer, primary_key=True, comment="기수ID")
    start = mapped_column(Integer, nullable=True, comment="기수 시작일")
    end = mapped_column(Integer, nullable=True, comment="기수 종료일")
    leaner_open = mapped_column(Integer, nullable=True, comment="러너모집 시작일")
    leaner_close = mapped_column(Integer, nullable=True, comment="러너모집 종료일")


class Academy(Base):
    __tablename__ = "academy"

    id = mapped_column(Integer, primary_key=True, nullable=False, comment="아카데미ID")
    user_id = mapped_column(Integer, ForeignKey('user.user_id'), nullable=False, comment="빌더유저ID")
    period_id = mapped_column(Integer, ForeignKey('period.id'), nullable=False, comment="기수ID")
    academy_name = mapped_column(String(100), nullable=False, comment="아카데미 이름")
    description = mapped_column(String(255), nullable=True, comment="아카데미 설명")

    # user = relationship("User", back_populates="academie")
