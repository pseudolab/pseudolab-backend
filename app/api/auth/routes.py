from fastapi import APIRouter, Depends, Path, Request, HTTPException
from api.auth.schema import LoginToken, LoginResponse, BingoUser, LoginType, LoginUrl
from api.auth.services.social_login import SocialLoginDepends
from api.auth.services.bingo_login import LoginUser, GetBingoUserByName, GetBingoUserById

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/bingo/sign-up", response_model=BingoUser, description="빙고용 임시 회원가입 API")
async def bingo_sign_up(username: str, password: str, bingo_user: LoginUser = Depends(LoginUser)):
    res = await bingo_user.execute(username, password)
    return res


@auth_router.get("/bingo/get-user", response_model=BingoUser, description="빙고용 임시 유저 조회 API")
async def bingo_get_user(username: str, bingo_user: GetBingoUserByName = Depends(GetBingoUserByName)):
    return await bingo_user.execute(username)


@auth_router.get("/bingo/get-user/{user_id}", response_model=BingoUser, description="빙고용 임시 유저 조회 API")
async def bingo_get_user(user_id: int, bingo_user: GetBingoUserById = Depends(GetBingoUserById)):
    return await bingo_user.execute(user_id)


@auth_router.get("/discord/login", description="Discord 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginUrl:
    return await social_login.discord_login()


@auth_router.get("/discord/redirect", description="Discord 로그인 redirect")
async def oauth2_login(request: Request, social_login: SocialLoginDepends) -> LoginResponse:
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing 'code' parameter")
    return await social_login.discord_login_redirect(code)


@auth_router.get("/google/login", description="Google 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginUrl:
    return await social_login.google_login()


@auth_router.get("/google/redirect", description="Google 로그인 redirect")
async def oauth2_login(request: Request, social_login: SocialLoginDepends) -> LoginResponse:
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing 'code' parameter")
    return await social_login.google_login_redirect(code)


@auth_router.get("/github/login", description="Github 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginUrl:
    return await social_login.github_login()


@auth_router.get("/github/redirect", description="Github 로그인 redirect")
async def oauth2_login(request: Request, social_login: SocialLoginDepends) -> LoginResponse:
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing 'code' parameter")
    return await social_login.github_login_redirect(code)


@auth_router.get("/kakao/login", description="Kakao 로그인 URL 생성")
async def oauth2_login(social_login: SocialLoginDepends) -> LoginUrl:
    return await social_login.kakao_login()


@auth_router.get("/kakao/redirect", description="Kakao 로그인 redirect")
async def oauth2_login(request: Request, social_login: SocialLoginDepends) -> LoginResponse:
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing 'code' parameter")
    return await social_login.kakao_login_redirect(code)


@auth_router.get("/sign-up", description="회원가입 API")
async def sign_up(social_login: SocialLoginDepends) -> LoginResponse:
    return await social_login.sign_up()
