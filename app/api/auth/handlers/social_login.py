import os
from typing import AsyncIterator
from core.db import AsyncSessionDepends
from models.user import User
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated
from enum import Enum, auto
from api.auth.schema import LoginState, LoginType, LoginResponse

REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"


class SocialLogin:
    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def login(self, login_type: int, code: str) -> LoginResponse:
        if login_type == LoginType.discord.value:
            return await self.discord_login(code)
        elif login_type == LoginType.google.value:
            pass
        elif login_type == LoginType.github.value:
            pass

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

    async def sing_up(self):
        pass


SocialLoginDepends = Annotated[SocialLogin, Depends(SocialLogin)]
