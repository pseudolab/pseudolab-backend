import os
from typing import AsyncIterator
from app.core.db import AsyncSessionDepends
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated
from enum import Enum

REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"


class LoginState(Enum):
    SignIn = 0
    SignUp = 1


class DiscordLogin:
    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def login(self, code: str) -> LoginState:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "scope": "identify, email, ",
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

        # DB 체크해서 로그인, 회원가입 상태 체크
        return LoginState.SignIn

    async def create_user(self):
        pass


DiscordLoginDepends = Annotated[DiscordLogin, Depends(DiscordLogin)]
