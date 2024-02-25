from typing import AsyncIterator
from app.api.auth import router
from httpx import AsyncClient
from fastapi import HTTPException
from fastapi.responses import RedirectResponse


@router.get("/discord/login/redirect")
async def discord_login(code: str) -> RedirectResponse:
    async with AsyncClient() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "client_id": "1196826150446571602",
            "client_secret": "uaxTEGKDAxi507plxEGDLt5LwvOfUBDG",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8000/auth/discord/login/redirect",
            "scope": "identify, email, guilds.join",
        }

        response = await client.post("https://discord.com/api/oauth2/token", headers=headers, json=body)
        if not response.is_success:
            raise HTTPException(
                status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
            )

        res_data = response.json()
        access_token = res_data.get("access_token")
        headers = {"authorization": access_token}
        response = await client.get("https://discordapp.com/api/users/@me", headers=headers)
        if not response.is_success:
            raise HTTPException(
                status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
            )

    return RedirectResponse("http://localhost:5173/")
