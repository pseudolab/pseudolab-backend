from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import mapped_column

from models.base import Base


class ApplicationForm(Base):
    __tablename__ = "application_form"

    id = mapped_column(Integer, primary_key=True, comment="신청양식ID")
    form_content = mapped_column(JSON, nullable=False, comment="신청양식 내용")
    form_type = mapped_column(
        Integer, nullable=False, comment="신청양식 구분 (1: builder, 2: learner)"
    )
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="입력 날짜"
    )
    updated_at = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), comment="수정 날짜"
    )


class Builder(Base):
    __tablename__ = "builder"

    id = mapped_column(Integer, primary_key=True, comment="빌더아카데미ID")
    user_id = mapped_column(
        Integer, ForeignKey("user.user_id"), nullable=False, comment="빌더유저ID"
    )
    form_content = mapped_column(JSON, nullable=False, comment="신청양식 내용")
    is_selected = mapped_column(Boolean, nullable=False, comment="빌더 선정 여부")


class Learner(Base):
    __tablename__ = "learner"

    id = mapped_column(Integer, primary_key=True, comment="러너아카데미ID")
    user_id = mapped_column(
        Integer, ForeignKey("user.user_id"), nullable=False, comment="러너유저ID"
    )
    form_content = mapped_column(JSON, nullable=False, comment="신청양식 내용")
    is_selected = mapped_column(
        Boolean, nullable=False, comment="러너 선정 여부", default=False
    )
    is_completed = mapped_column(
        Boolean, nullable=False, comment="수료 여부", default=False
    )
