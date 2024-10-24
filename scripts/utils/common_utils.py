from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
import time
from fastapi import Request
from scripts.db.mongo import mongo_client
from scripts.constants.common_constants import Secrets, CommonKeys
from scripts.db.mongo.blog_posts.collections.unique_id import UniqueId, UniqueIdSchema
from scripts.logging import logger
from scripts.utils.security_utils.apply_encrytion_util import create_token
from scripts.utils.security_utils.jwt_util import JWT


def timed_lru_cache(seconds: int = 10, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now(timezone.utc) + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.now(timezone.utc) >= func.expiration:
                logger.debug("Cache Expired")
                func.cache_clear()
                func.expiration = datetime.now(timezone.utc) + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


class CommonUtils(CommonKeys):
    def __init__(self):
        self.unique_con = UniqueId(mongo_client)

    def get_next_id(self, _param):
        my_dict = UniqueIdSchema(key=_param)
        my_doc = self.unique_con.find_one_record(key=_param)
        if not my_doc.id:
            my_dict.id = "100"
            return self.unique_con.insert_record(my_dict)
        else:
            count_value = str(int(my_doc.id) + 1)
            my_dict.id = count_value
            return self.unique_con.update_record(my_dict)

    def get_user_meta(self, user_id=None, check_flag=False):
        data_for_meta = {}
        if check_flag:
            data_for_meta[self.KEY_CREATED_BY] = user_id
            data_for_meta[self.KEY_CREATED_TIME] = int(time.time() * 1000)
        data_for_meta[self.KEY_UPDATED_AT] = user_id
        data_for_meta[self.KEY_LAST_UPDATED_TIME] = int(time.time() * 1000)
        return data_for_meta

    @staticmethod
    def encode_using_jwt(request_id, user_id):
        jwt = JWT()
        payload = {"request_id": request_id, "user_id": user_id}
        exp = datetime.now() + timedelta(days=30)
        _extras = {"iss": Secrets.issuer, "exp": exp}
        _payload = {**payload, **_extras}
        return jwt.encode(_payload)

    @staticmethod
    def form_request_cookies(request_obj: Request) -> dict:
        return {
            "login-token": request_obj.headers.get("login-token", request_obj.cookies.get("login-token")),
            "userId": request_obj.cookies.get(
                "user_id", request_obj.cookies.get("userId", request_obj.headers.get("userId"))
            ),
        }

    @staticmethod
    def create_token(host: str = "127.0.0.1", user_id=None, internal_token=Secrets.token):
        """
        This method is to create a cookie
        """

        try:
            if user_id is None:
                user_id = "user_099"
            return create_token(user_id=user_id, ip=host, token=internal_token)
        except Exception as e:
            logger.exception(str(e))
            raise
