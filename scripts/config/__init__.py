import os
import pathlib
import shutil
import sys
from typing import Optional, Any

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings, Field, root_validator

load_dotenv()

PROJECT_NAME = "pinacle_assignment"


class _Service(BaseSettings):
    MODULE_NAME: str = Field(default="pinacle_assignment")
    APP_NAME: str = Field(default="pinacle_assignment")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=5112)
    LOG_LEVEL: str = Field(default="INFO")
    ENABLE_FILE_LOG: Optional[Any] = False
    ENABLE_CONSOLE_LOG: Optional[Any] = True

    @root_validator(allow_reuse=True)
    def validate_values(cls, values):
        values["LOG_LEVEL"] = values["LOG_LEVEL"] or "INFO"
        print(f"Logging Level set to: {values['LOG_LEVEL']}")
        return values


class _PathToStorage(BaseSettings):
    BASE_PATH: pathlib.Path = Field(None, env="BASE_PATH")
    MOUNT_DIR: pathlib.Path = Field(None, env="MOUNT_DIR")
    TEMP_PATH: pathlib.Path = Field(None, env="TEMP_PATH")
    MODULE_PATH: Optional[pathlib.Path]

    @root_validator(allow_reuse=True)
    def assign_values(cls, values):
        values["LOGS_MODULE_PATH"] = os.path.join(values.get("BASE_PATH"), "logs", values.get("MOUNT_DIR"))
        values["MODULE_PATH"] = os.path.join(values.get("BASE_PATH"), values.get("MOUNT_DIR"))
        return values

    @root_validator(allow_reuse=True)
    def validate_values(cls, values):
        if not values["BASE_PATH"]:
            print("Error, environment variable BASE_PATH not set")
            sys.exit(1)
        if not values["MOUNT_DIR"]:
            print("Error, environment variable MOUNT_DIR not set")
            sys.exit(1)
        return values


class _KeyPath(BaseSettings):
    KEYS_PATH: Optional[pathlib.Path] = Field(default="data/keys")
    PUBLIC: Optional[pathlib.Path]
    PRIVATE: Optional[pathlib.Path]

    @root_validator(allow_reuse=True)
    def assign_values(cls, values):
        if not os.path.isfile(os.path.join(values.get("KEYS_PATH"), "public")) or not os.path.isfile(
            os.path.join(values.get("KEYS_PATH"), "private")
        ):
            if not os.path.exists(values.get("KEYS_PATH")):
                os.makedirs(values.get("KEYS_PATH"))
            shutil.copy(os.path.join("assets", "keys", "public"), os.path.join(values.get("KEYS_PATH"), "public"))
            shutil.copy(os.path.join("assets", "keys", "private"), os.path.join(values.get("KEYS_PATH"), "private"))
        values["PUBLIC"] = os.path.join(values.get("KEYS_PATH"), "public")
        values["PRIVATE"] = os.path.join(values.get("KEYS_PATH"), "private")
        return values


class _Databases(BaseSettings):
    MONGO_URI: Optional[str]
    REDIS_URI: Optional[str]
    REDIS_LOGIN_DB: Optional[int] = 14
    REDIS_USER_PERMISSION_DB: Optional[int] = 15

    @root_validator(allow_reuse=True)
    def validate_values(cls, values):
        if not values["MONGO_URI"]:
            print("Error, environment variable MONGO_URI not set")
            sys.exit(1)
        if not values["REDIS_URI"]:
            print("Error, environment variable REDIS_URI not set")
            sys.exit(1)
        return values


Service = _Service()
PathToStorage = _PathToStorage()
KeyPath = _KeyPath()
DBConf = _Databases()

__all__ = [
    "PROJECT_NAME",
    "Service",
    "PathToStorage",
    "KeyPath",
    "DBConf"
]
