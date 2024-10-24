from secrets import compare_digest
from typing import Optional

from fastapi import HTTPException, Request, Response, status
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyCookie
from fastapi.security.api_key import APIKeyBase
from pydantic import BaseModel, Field

from scripts.config import Service
from scripts.db.redis_connection import login_db

from scripts.constants.common_constants import Secrets
from scripts.utils.security_utils.apply_encrytion_util import create_token
from scripts.utils.security_utils.jwt_util import JWT


class CookieAuthentication(APIKeyBase):
    """
    Authentication backend using a cookie.
    Internally, uses a JWT token to store the data.
    """

    scheme: APIKeyCookie
    cookie_name: str
    cookie_secure: bool

    def __init__(
        self,
        cookie_name: str = "login-token",
    ):
        super().__init__()
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name=cookie_name)
        self.scheme_name = self.__class__.__name__
        self.cookie_name = cookie_name
        self.scheme = APIKeyCookie(name=self.cookie_name, auto_error=False)
        self.login_redis = login_db
        self.jwt = JWT()

    async def __call__(self, request: Request, response: Response) -> str:
        cookies = request.cookies
        login_token = cookies.get("login-token")
        if not login_token:
            login_token = request.headers.get("login-token")
        if not login_token:
            raise HTTPException(status_code=401)

        jwt_token = self.login_redis.get(login_token)
        if not jwt_token:
            raise HTTPException(status_code=401)

        try:
            decoded_token = self.jwt.validate(token=jwt_token)
            if not decoded_token:
                raise HTTPException(status_code=401)
        except Exception as e:
            raise HTTPException(status_code=401, detail=e.args)

        user_id = decoded_token.get("user_id", decoded_token.get("userId"))
        _token = decoded_token.get("token")
        _age = int(decoded_token.get("age", Secrets.LOCK_OUT_TIME_MINS))

        if any(
            [
                not compare_digest(Secrets.token, _token),
                login_token != decoded_token.get("uid"),
            ]
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        request.cookies.update(
            {"user_id": user_id, "userId": user_id}
        )

        try:
            new_token = create_token(
                user_id=user_id,
                ip=request.client.host,
                token=Secrets.token,
                age=_age,
                login_token=login_token,
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.args)
        response.set_cookie(
            "login-token",
            new_token,
            samesite="strict",
            httponly=True,
            secure=Service.secure_cookie,
            max_age=Secrets.LOCK_OUT_TIME_MINS * 60,
        )
        # If project ID is null, this is susceptible to 500 Status Code. Ensure token formation has project ID in
        # login token
        response.headers.update(
            {
                "login-token": new_token,
                "userId": user_id,
                "user_id": user_id,
            }
        )

        return user_id


class MetaInfoSchema(BaseModel):
    user_id: Optional[str] = ""
    language: Optional[str] = ""
    ip_address: Optional[str] = ""
    login_token: Optional[str] = Field(alias="login-token")

    class Config:
        allow_population_by_field_name = True


class MetaInfoCookie(APIKeyBase):
    """
    Project ID backend using a cookie.
    """

    scheme: APIKeyCookie

    def __init__(self):
        super().__init__()
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name="meta")
        self.scheme_name = self.__class__.__name__

    def __call__(self, request: Request, response: Response):
        cookies = request.cookies
        cookie_json = {
            "userId": cookies.get(
                "user_id", cookies.get("userId", request.headers.get("userId", request.headers.get("user_id")))
            ),
            "language": cookies.get("language", request.headers.get("language")),
        }
        return MetaInfoSchema(
            user_id=cookie_json["userId"],
            language=cookie_json["language"],
            ip_address=request.client.host,
            login_token=cookies.get("login-token"),
        )


class GetUserID(APIKeyBase):
    """
    Project ID backend using a cookie.
    """

    scheme: APIKeyCookie

    def __init__(self):
        super().__init__()
        self.model: APIKey = APIKey(**{"in": APIKeyIn.cookie}, name="user_id")
        self.scheme_name = self.__class__.__name__

    def __call__(self, request: Request, response: Response):
        if user_id := request.cookies.get("user_id", request.cookies.get("userId", request.headers.get("userId"))):
            return user_id
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
