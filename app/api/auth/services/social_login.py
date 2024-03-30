import os
from typing import AsyncIterator
from core.db import AsyncSessionDepends
from core.dependencies import OAuth2SchemeDepends
from models.user import User
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated
from enum import Enum, auto
from api.auth.schema import LoginState, LoginResponse, LoginUrl

REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"


class SocialLogin:
    """
    Social 로그인 순서
    1. login API로 로그인 URL을 전달 받음
    2. 해당 URL로 승인하면 각 OAuth에 설정한 redirect url 에 code와 함께 API 접근
    3. code를 활용하여 각 OAuth에 대한 access_token 발급
    4. 해당 access_token은 회원 정보를 가져오기 위한 토큰이니 별도로 JWT token과 refresh token을 발급해야할 뜻? 확인 필요.
    """

    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def discord_login(self) -> LoginUrl:
        return LoginUrl(url="https://discord.com/api/oauth2/token")

    async def discord_login_redirect(self, code: str) -> LoginResponse:
        login_state = LoginState.sign_in
        message = "로그인 성공"
        client_id = os.getenv("DISCORD_CLIENT_ID")
        client_secret = os.getenv("DISCORD_CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "scope": "identify, email",
            }
            response = await client.post("https://discord.com/api/oauth2/token", headers=headers, data=data)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
                )

            res_data = response.json()

            # 해당 토큰은 보관하는게 나을꺼같은데?
            access_token = res_data.get("access_token")
            headers = {"authorization": f"Bearer {access_token}"}
            response = await client.get("https://discordapp.com/api/users/@me", headers=headers)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
                )

            user_data = response.json()
            email = user_data.get("email")

            # 이메일로 유저 가입 유무 체크
            find_user = await User.get_user_by_email(self.session, email)
            if not find_user:
                message = "회원 가입이 필요합니다."
                login_state = LoginState.sign_up

        # DB 체크해서 로그인, 회원가입 상태 체크
        return LoginResponse(
            ok=True,
            message=message,
            login_state=login_state,
            access_token="",
            refresh_token="",
        )

    async def google_login(self) -> LoginUrl:
        return LoginUrl(url="")

    async def google_login_redirect(self, code: str) -> LoginResponse:
        pass


class SignUp:
    def __init__(self, session: AsyncSessionDepends, token: OAuth2SchemeDepends):
        self.session = session
        self.token = token

    async def execute(self):
        pass


SocialLoginDepends = Annotated[SocialLogin, Depends(SocialLogin)]
