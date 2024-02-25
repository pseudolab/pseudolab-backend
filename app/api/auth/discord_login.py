from typing import AsyncIterator
from app.core.db import AsyncSessionDepends
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated

CLINET_ID = "1196826150446571602"
CLIENT_SECRET = "-74RIQXeoFaDmyPvwtN5UjUpwuCk8hY-"
REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"


class DiscordLogin:
    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def login(self, code: str):
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": CLINET_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "scope": "identify",
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

        # DB 가입 여부 체크해서 보낼 url 다르게.
        return True

    async def create_user(self):
        pass


DiscordLoginDepends = Annotated[DiscordLogin, Depends(DiscordLogin)]
