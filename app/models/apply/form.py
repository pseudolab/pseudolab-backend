from core.db import AsyncSession
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, desc, func, select
from sqlalchemy.orm import mapped_column

from models.base import Base


class FormRepository(Base):
    __tablename__ = "form_repository"

    id = mapped_column(Integer, primary_key=True, comment="신청양식ID")
    form_type = mapped_column(
        Integer, nullable=False, comment="신청양식 구분 (1: builder, 2: learner)"
    )
    form_content = mapped_column(JSON, nullable=False, comment="신청양식 내용")
    created_at = mapped_column(Integer, nullable=False, comment="입력 날짜")
    updated_at = mapped_column(Integer, comment="수정 날짜")


class Application(Base):
    __tablename__ = "application"

    id = mapped_column(Integer, primary_key=True, comment="신청서ID")
    user_id = mapped_column(
        Integer, ForeignKey("user.user_id"), nullable=False, comment="유저ID"
    )
    form_type = mapped_column(
        Integer, nullable=False, comment="신청양식 구분 (1: builder, 2: learner)"
    )
    form_content = mapped_column(JSON, nullable=False, comment="신청양식 내용")
    is_selected = mapped_column(Boolean, nullable=False, comment="선정 여부", default=False)