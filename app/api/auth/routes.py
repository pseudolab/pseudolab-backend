from fastapi import APIRouter, Depends, Path
from api.auth.schema import LoginToken, LoginResponse, BingoUser
from api.auth.services.social_login import SocialLoginDepends
from api.auth.services.bingo_login import CreateBingoUser, GetBingoUserByName

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/bingo/sign-up", response_model=BingoUser, description="빙고용 임시 회원가입 API")
async def bingo_sign_up(username: str, bingo_user: CreateBingoUser = Depends(CreateBingoUser)):
    res = await bingo_user.execute(username)
    return res


@auth_router.get("/bingo/get-user", response_model=BingoUser, description="빙고용 임시 유저 조회 API")
async def bingo_get_user(username: str, bingo_user: GetBingoUserByName = Depends(GetBingoUserByName)):
    return await bingo_user.execute(username)


@auth_router.get("/discord/login", description="Discord 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.discord_login()


@auth_router.get("/discord/redirect", description="Discord 로그인 redirect")
async def oauth2_login(login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.discord_login_redirect(LoginType.discord, login_token.code)


@auth_router.get("/google/login", description="Google 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.google_login()


@auth_router.get("/google/redirect", description="Google 로그인 redirect")
async def oauth2_login(login_token: LoginToken, social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.google_login(login_token.code)


@auth_router.get("/sign-up", description="회원가입 API")
async def sign_up(social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.sign_up()
