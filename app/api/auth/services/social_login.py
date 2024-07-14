import os
from typing import AsyncIterator
from core.db import AsyncSessionDepends
from core.dependencies import OAuth2SchemeDepends
from models.user import User
from httpx import AsyncClient
from fastapi import HTTPException, Depends
from typing import Annotated
from enum import Enum, auto
from api.auth.schema import LoginState, LoginResponse, LoginUrl
from urllib.parse import parse_qs
from api.auth.services.jwts import create_access_token, create_refresh_token

REDIRECT_URI_DISCORD = os.getenv("REDIRECT_URI_DISCORD")
REDIRECT_URI_GOOGLE = os.getenv("REDIRECT_URI_GOOGLE")
REDIRECT_URI_GITHUB = os.getenv("REDIRECT_URI_GITHUB")
REDIRECT_URI_KAKAO = os.getenv("REDIRECT_URI_KAKAO")


class SocialLogin:
    """
    Social 로그인 순서
    1. login API로 로그인 URL을 전달 받음
    2. 해당 URL로 승인하면 각 OAuth에 설정한 redirect url 에 code와 함께 API 접근
    3. code를 활용하여 각 OAuth에 대한 access_token 발급
    4. 해당 access_token은 회원 정보를 가져오기 위한 토큰이니 별도로 JWT token과 refresh token을 발급해야할 뜻? 확인 필요.
    """

    def __init__(self, session: AsyncSessionDepends):
        self.session = session

    async def discord_login(self) -> LoginUrl:
        client_id = os.getenv("DISCORD_CLIENT_ID")
        redirect_uri = REDIRECT_URI_DISCORD
        scope = "identify+email+guilds.join"
        login_url = f"https://discord.com/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        return LoginUrl(url=login_url, ok=True, message="Discord login URL generated successfully")

    async def discord_login_redirect(self, code: str) -> LoginResponse:
        login_state = LoginState.sign_in
        message = "로그인 성공"
        client_id = os.getenv("DISCORD_CLIENT_ID")
        client_secret = os.getenv("DISCORD_CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI_DISCORD,
                "scope": "identify, email",
            }
            response = await client.post("https://discord.com/api/oauth2/token", headers=headers, data=data)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
                )

            res_data = response.json()

            # 해당 토큰은 보관하는게 나을꺼같은데?
            access_token = res_data.get("access_token")
            headers = {"authorization": f"Bearer {access_token}"}
            response = await client.get("https://discordapp.com/api/users/@me", headers=headers)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Discord API: {response.json()}"
                )

            user_data = response.json()
            email = user_data.get("email")

            # 이메일로 유저 가입 유무 체크
            find_user = await User.get_user_by_email(self.session, email)
            access_token_jwt = ""
            refresh_token_jwt = ""
            if not find_user:
                message = "회원 가입이 필요합니다."
                login_state = LoginState.sign_up
            else:
                user_id = find_user.user_id
                access_token_jwt, access_expires = create_access_token(data={"sub": user_id})
                refresh_token_jwt, refresh_expires = create_refresh_token(data={"sub": user_id})
                await User.update_tokens(
                    self.session, user_id, access_token_jwt, refresh_token_jwt, access_expires, refresh_expires
                )

        return LoginResponse(
            ok=True,
            message=message,
            login_state=login_state,
            access_token=access_token_jwt,
            refresh_token=refresh_token_jwt,
        )

    async def google_login(self) -> LoginUrl:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = REDIRECT_URI_GOOGLE
        scope = "https://www.googleapis.com/auth/userinfo.email"
        # scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        login_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
        return LoginUrl(url=login_url, ok=True, message="Google login URL generated successfully")

    async def google_login_redirect(self, code: str) -> LoginResponse:
        login_state = LoginState.sign_in
        message = "로그인 성공"
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI_GOOGLE,
            }
            response = await client.post("https://oauth2.googleapis.com/token", headers=headers, data=data)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Google API: {response.json()}"
                )

            res_data = response.json()
            access_token = res_data.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting user data from Google API: {response.json()}"
                )

            user_data = response.json()
            email = user_data.get("email")

            find_user = await User.get_user_by_email(self.session, email)
            access_token_jwt = ""
            refresh_token_jwt = ""
            if not find_user:
                message = "회원 가입이 필요합니다."
                login_state = LoginState.sign_up
            else:
                user_id = find_user.user_id
                access_token_jwt, access_expires = create_access_token(data={"sub": user_id})
                refresh_token_jwt, refresh_expires = create_refresh_token(data={"sub": user_id})
                await User.update_tokens(
                    self.session, user_id, access_token_jwt, refresh_token_jwt, access_expires, refresh_expires
                )

        return LoginResponse(
            ok=True,
            message=message,
            login_state=login_state,
            access_token=access_token_jwt,
            refresh_token=refresh_token_jwt,
        )

    async def github_login(self) -> LoginUrl:
        client_id = os.getenv("GITHUB_CLIENT_ID")
        redirect_uri = REDIRECT_URI_GITHUB
        scope = "user:email"
        login_url = (
            f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        )
        return LoginUrl(url=login_url, ok=True, message="GitHub login URL generated successfully")

    async def github_login_redirect(self, code: str) -> LoginResponse:
        login_state = LoginState.sign_in
        message = "로그인 성공"
        client_id = os.getenv("GITHUB_CLIENT_ID")
        client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/json"}
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": REDIRECT_URI_GITHUB,
            }
            response = await client.post("https://github.com/login/oauth/access_token", headers=headers, json=data)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from GitHub API: {response.content}"
                )

            res_data = parse_qs(response.content.decode())
            access_token = res_data.get("access_token")[0]
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get("https://api.github.com/user", headers=headers)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting user data from GitHub API: {response.json()}"
                )

            user_data = response.json()
            email = user_data.get("email")

            find_user = await User.get_user_by_email(self.session, email)
            access_token_jwt = ""
            refresh_token_jwt = ""
            if not find_user:
                message = "회원 가입이 필요합니다."
                login_state = LoginState.sign_up
            else:
                user_id = find_user.user_id
                access_token_jwt, access_expires = create_access_token(data={"sub": user_id})
                refresh_token_jwt, refresh_expires = create_refresh_token(data={"sub": user_id})
                await User.update_tokens(
                    self.session, user_id, access_token_jwt, refresh_token_jwt, access_expires, refresh_expires
                )

        return LoginResponse(
            ok=True,
            message=message,
            login_state=login_state,
            access_token=access_token_jwt,
            refresh_token=refresh_token_jwt,
        )

    async def kakao_login(self) -> LoginUrl:
        client_id = os.getenv("KAKAO_CLIENT_ID")
        redirect_uri = REDIRECT_URI_KAKAO
        scope = "account_email"
        login_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
        return LoginUrl(url=login_url, ok=True, message="Kakao login URL generated successfully")

    async def kakao_login_redirect(self, code: str) -> LoginResponse:
        login_state = LoginState.sign_in
        message = "로그인 성공"
        client_id = os.getenv("KAKAO_CLIENT_ID")
        client_secret = os.getenv("KAKAO_CLIENT_SECRET")
        async with AsyncClient() as client:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": REDIRECT_URI_KAKAO,
                "code": code,
            }
            response = await client.post("https://kauth.kakao.com/oauth/token", headers=headers, data=data)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting token or user data from Kakao API: {response.json()}"
                )

            res_data = response.json()
            access_token = res_data.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get("https://kapi.kakao.com/v2/user/me", headers=headers)
            if not response.is_success:
                raise HTTPException(
                    status_code=500, detail=f"Error in getting user data from Kakao API: {response.json()}"
                )

            user_data = response.json()
            kakao_account = user_data.get("kakao_account")
            email = kakao_account.get("email")

            find_user = await User.get_user_by_email(self.session, email)
            access_token_jwt = ""
            refresh_token_jwt = ""
            if not find_user:
                message = "회원 가입이 필요합니다."
                login_state = LoginState.sign_up
            else:
                user_id = find_user.user_id
                access_token_jwt, access_expires = create_access_token(data={"sub": user_id})
                refresh_token_jwt, refresh_expires = create_refresh_token(data={"sub": user_id})
                await User.update_tokens(
                    self.session, user_id, access_token_jwt, refresh_token_jwt, access_expires, refresh_expires
                )

        return LoginResponse(
            ok=True,
            message=message,
            login_state=login_state,
            access_token=access_token_jwt,
            refresh_token=refresh_token_jwt,
        )


class SignUp:
    def __init__(self, session: AsyncSessionDepends, token: OAuth2SchemeDepends):
        self.session = session
        self.token = token

    async def execute(self):
        pass


SocialLoginDepends = Annotated[SocialLogin, Depends(SocialLogin)]
