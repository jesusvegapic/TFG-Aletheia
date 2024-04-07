import json
import os
from dataclasses import dataclass

from apps.config.container import Config

secrets_filename: str = os.getenv("SECRETS_FILENAME")  # type: ignore

secrets_json: dict

with open(secrets_filename, "r") as env_file:
    secrets_json = json.loads(env_file.read())

env_db = secrets_json["db"]


@dataclass
class ApiConfig(Config):
    APP_NAME: str = "Aletheia Courses platform API REST"
    DEBUG: bool = True if os.getenv("DEBUG") == 1 else 0  # type: ignore
    DATABASE_ECHO: bool = True if os.getenv("DATABASE_ECHO") == 1 else 0  # type: ignore
    DATABASE_URL: str = \
        f"postgresql+asyncpg://{env_db['user']}:{env_db['passwd']}@{env_db['host']}:{env_db['port']}/{env_db['name']}"
    LOGGER_NAME: str = "api"
