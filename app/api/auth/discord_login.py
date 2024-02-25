from typing import AsyncIterator
from app.api.auth import router
from httpx import AsyncClient
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

CLINET_ID = "1196826150446571602"
CLIENT_SECRET = "-74RIQXeoFaDmyPvwtN5UjUpwuCk8hY-"
REDIRECT_URI = "http://localhost:8000/auth/discord/login/redirect"

@router.get("/discord/login/redirect")
async def discord_login(code: str) -> RedirectResponse:
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
        response = await client.post("https://discord.com/api/oauth2/token", data=data)
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

    return RedirectResponse("http://localhost:5173/")
