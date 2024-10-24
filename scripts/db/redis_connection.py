import redis

from scripts.config import DBConf

login_db = redis.from_url(DBConf.REDIS_URI, db=int(DBConf.REDIS_LOGIN_DB), decode_responses=True)
user_permissions_redis = redis.from_url(DBConf.REDIS_URI, db=int(DBConf.REDIS_USER_PERMISSION_DB), decode_responses=True)