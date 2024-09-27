import json
import os
from dataclasses import dataclass
from apps.container import Config
from src.framework_ddd.mailing.domain.value_objects import Email
from src.framework_ddd.mailing.infrastructure.email_sender import EmailServerURL

secrets_filename: str = os.getenv("SECRETS_FILENAME")  # type: ignore

secrets_json: dict

with open(secrets_filename, "r") as env_file:
    secrets_json = json.loads(env_file.read())

env_db = secrets_json["db"]
env_gridfs = secrets_json["motor_mongodb"]
env_smtp_server = secrets_json["smtp_server"]


@dataclass
class ApiConfig(Config):
    EMAIL_SERVER_URL: EmailServerURL = EmailServerURL(
        host=env_smtp_server["host"],
        port=env_smtp_server["port"],
        user=env_smtp_server["user"],
        password=env_smtp_server["password"]
    )
    SYSTEM_EMAIL: Email = Email(secrets_json["system_email"])
    APP_NAME: str = "Aletheia Courses agora API REST"
    DEBUG: bool = True if os.getenv("DEBUG") == 1 else 0  # type: ignore
    DATABASE_ECHO: bool = True if os.getenv("DATABASE_ECHO") == 1 else 0  # type: ignore
    DATABASE_URL: str = \
        f"postgresql+asyncpg://{env_db['user']}:{env_db['passwd']}@{env_db['host']}:{env_db['port']}/{env_db['name']}"
    BUCKET_URL: str = (
        f"motor_mongodb://{env_gridfs['user']}:{env_gridfs['passwd']}@"
        f"{env_gridfs['host']}:{env_gridfs['port']}/{env_gridfs['name']}"
    )
    LOGGER_NAME: str = "api"
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # type: ignore
