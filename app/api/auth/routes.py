from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.api.auth.discord_login import DiscordLoginDepends

router = APIRouter(prefix="/auth")


@router.get("/discord/login/redirect")
async def discord_login(code: str, discord_login: DiscordLoginDepends) -> RedirectResponse:
    if not discord_login.login(code):
        raise Exception()
    return RedirectResponse("http://localhost:5173/")
