import logging

import orjson as json
from fastapi import HTTPException, Request, status

from scripts.db.redis_connection import user_permissions_redis


class RBAC:
    def __init__(self, entity_name: str, operation: list[str]):
        self.entity_name = entity_name
        self.operation = operation

    def check_permissions(self, user_id: str) -> dict[str, bool]:
        user_permission_rec = user_permissions_redis.hget(user_id, self.entity_name)
        if not user_permission_rec:
            return {}  # TODO: raise exception here
        user_permission_rec = json.loads(user_permission_rec)
        if permission_dict := {i: True for i in self.operation if user_permission_rec.get(i)}:
            return permission_dict
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient Permission!")

    def __call__(self, request: Request) -> dict[str, bool]:
        user_id = request.cookies.get("userId", request.headers.get("userId"))
        return self.check_permissions(user_id=user_id)
