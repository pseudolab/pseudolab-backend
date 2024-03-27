from enum import IntEnum
from core.base_schema import BaseSchema
from pydantic import Field
from typing import Optional


class LoginState(IntEnum):
    none = -1
    sign_in = 0
    sign_up = 1


class LoginToken(BaseSchema):
    login_type: LoginType = Field(description="Social 로그인 종류")
    code: str = Field(description="각 Social 로그인이 발급해주는 accept token")


class LoginResponse(BaseSchema):
    """
    Response 모델의 인자는 Optional로 처리. 실패한 경우 빈 상태로 반환할 수 있기때문
    """

    login_state: Optional[LoginState] = Field(description="로그인 상태 - 회원가입 필요 상태 또는 로그인 가능 상태")
    access_token: Optional[str] = Field(description="Bearer Access Token")
    refresh_token: Optional[str] = Field(description="Refresh Token")


class LoginUrl(BaseSchema):
    url: Optional[str] = Field(description="로그인을 위한 페이지를 보여주는 URL")
