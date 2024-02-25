from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.api.auth.discord_login import DiscordLoginDepends

router = APIRouter(prefix="/auth")


@router.get("/discord/login/redirect")
async def discord_oauth2_login(code: str, discord_login: DiscordLoginDepends) -> RedirectResponse:
    result = await discord_login.login(code)
    return RedirectResponse("http://localhost:5173/")
