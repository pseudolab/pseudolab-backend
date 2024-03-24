from fastapi import APIRouter
from api.auth.schema import LoginToken, LoginResponse
from api.auth.handlers.social_login import SocialLoginDepends

router = APIRouter(prefix="/auth")


@router.get("/login", description="로그인 API")
async def oauth2_login(login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.discord_login(login_token.code)


@router.get("/sign-up", description="회원가입 API")
async def oauth2_login(login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.discord_login(login_token.code)
