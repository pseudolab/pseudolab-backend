from fastapi import APIRouter
from api.auth.schema import LoginToken, LoginResponse
from api.auth.handlers.social_login import SocialLoginDepends, LoginType

router = APIRouter(prefix="/auth")


@router.get("/discord/callback", description="로그인 redirect")
async def oauth2_login(login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.login(LoginType.discord, login_token.code)


@router.get("/google/login", description="로그인 URL 생성")
async def oauth2_login(login_type: str, login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.login(LoginType.google, login_token.code)


@router.get("/google/callback", description="로그인 redirect")
async def oauth2_login(login_type: str, login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.login(LoginType.google, login_token.code)


@router.get("/sign-up", description="회원가입 API")
async def sign_up(social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.sign_up()
