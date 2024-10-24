import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from scripts.utils.mongo_util import MongoCollectionBaseClass

from scripts.constants.db_constants import DBConstants, DatabaseNames


class UserCollectionKeys:
    KEY_LANGUAGE = "language"
    KEY_NAME = "name"
    KEY_USER_ID = "user_id"
    KEY_PROJECT_ID = "project_id"
    KEY_USERNAME = "username"
    KEY_USER_ROLE = "userrole"
    KEY_EMAIL = "email"


class UserSchema(BaseModel):
    name: Optional[str] = ""
    project_id: Optional[str] = ""
    username: Optional[str] = ""
    password: Optional[str] = ""
    email: Optional[Any] = None
    phonenumber: Optional[Any] = None
    userrole: Optional[List[str]] = None
    user_type: Optional[str] = ""
    user_id: Optional[str] = ""
    AccessLevel: Optional[Any] = None
    user_access_select_all: Optional[bool] = None
    access_group_ids: Optional[List[str]] = None
    client_id: Optional[str] = ""
    created_by: Optional[str] = ""
    hmi: Optional[Dict] = {}
    encryption_salt: Optional[Dict] = {}
    product_encrypted: Optional[bool] = None
    email_preferences: Optional[Dict] = {}
    language: Optional[str] = ""
    passwordReset: Optional[Dict] = {}
    failed_attempts: Optional[int] = 0
    is_user_locked: Optional[bool] = None
    last_failed_attempt: Optional[str] = ""
    profileImage_name: Optional[str] = ""
    profileImage_url: Optional[str] = ""
    date_format: Optional[str] = ""
    date_time_format: Optional[str] = ""
    time_format: Optional[str] = ""
    tz: Optional[str] = ""
    app_url: Optional[str] = ""
    landing_page: Optional[str] = ""
    ilens_encrypted: Optional[bool] = None
    is_app_user: Optional[bool] = None
    product_access: Optional[List] = []
    location: Optional[str] = ""
    department: Optional[str] = ""
    section: Optional[str] = ""
    azure_id: Optional[str] = ""
    expires_on: Optional[str] = ""
    token_azure: Optional[str] = ""
    disable_user: Optional[bool] = False
    access_level_list: Optional[dict] = {}
    created_on: Optional[int] = 0
    updated_by: Optional[str] = ""
    updated_on: Optional[int] = 0
    mfa_enabled: Optional[bool] = False
    mfa_configured: Optional[bool] = False
    secret: Optional[str] = ""
    mfa_enabled_on: Optional[int] = 0
    password_added_on: Optional[int] = None
    default_project: Optional[str] = ""
    shift_enabled: Optional[bool] = False
    shift_details: Optional[dict] = {}


class User(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(mongo_client, database=DatabaseNames.blog_posts, collection=DBConstants.collection_user)
        self.key_user_id = UserCollectionKeys.KEY_USER_ID
        self.key_username = UserCollectionKeys.KEY_USERNAME
        self.key_email = UserCollectionKeys.KEY_EMAIL

    def find_user(self, user_id=None, username=None, email=None, filter_dict=None):
        query = {}
        if user_id:
            query[self.key_user_id] = user_id
        if username:
            query[self.key_username] = username
        if email:
            query[self.key_email] = re.compile(email, re.IGNORECASE)
            query[self.key_email] = email
        user = self.find_one(query=query, filter_dict=filter_dict)
        if user:
            return UserSchema(**user)
        return UserSchema(**{})

    @staticmethod
    def get_users_list(project_id=None):
        query_json = [
            {
                "$group": {
                    "_id": None,
                    "data": {"$push": {"k": {"$ifNull": ["$user_id", ""]}, "v": {"$ifNull": ["$username", ""]}}},
                }
            },
            {"$replaceRoot": {"newRoot": {"$arrayToObject": "$data"}}},
        ]
        if bool(project_id):
            query_json.insert(0, {"$match": {"project_id": project_id}})
        return query_json

    def users_list_by_aggregate(self, query: list):
        return self.aggregate(pipelines=query)

    def find_user_by_project_id(self, user_id, project_id):
        user = self.find_one(query={self.key_user_id: user_id, self.key_project_id: project_id})
        if user:
            return dict(user)
        return user

    def get_all_users(self, filter_dict=None, sort=None, skip=0, limit=None, **query):
        users = self.find(filter_dict=filter_dict, sort=sort, skip=skip, limit=limit, query=query)
        if users:
            return list(users)
        return []

    def find_user_role_for_user_id(self, user_id, project_id):
        query = {"user_id": user_id, "project_id": project_id}
        filter_dict = {"userrole": 1, "_id": 0}
        return self.find_one(query=query, filter_dict=filter_dict)
