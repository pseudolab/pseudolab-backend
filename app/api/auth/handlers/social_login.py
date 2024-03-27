import os
from typing import AsyncIterator
from core.db import AsyncSessionDepends
from core.dependencies import OAuth2SchemeDepends
from models.user import User
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated
from enum import Enum, auto
from api.auth.schema import LoginState, LoginType, LoginResponse, LoginUrl

REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"


class SocialLogin:
    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def login(self, login_type: LoginType, code: str) -> LoginResponse:
        """
        OAuth2 redirect 통하여 로그인할 때 사용
        :param login_type: 로그인 타입
        :param code: 로그인 토큰
        :return:
        """
        if login_type == LoginType.discord:
            return await self.discord_login(code)
        elif login_type == LoginType.google:
            pass
        elif login_type == LoginType.github:
            pass
        else:
            raise HTTPException(status_code=404, detail="login_type이 비정상 입니다.")

    async def discord_login(self, code: str) -> LoginResponse:
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

    async def google_auth(self, code: str) -> LoginUrl:
        return LoginUrl(url="")

    async def google_login(self, code: str) -> LoginResponse:
        pass


class SignUp:
    def __init__(self, session: AsyncSessionDepends, token: OAuth2SchemeDepends):
        self.session = session

    async def execute(self):
        pass


SocialLoginDepends = Annotated[SocialLogin, Depends(SocialLogin)]
