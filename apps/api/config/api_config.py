from dataclasses import dataclass

from apps.config.container import Config


# env_filename = os.getenv("ENV_FILENAME", ".env")


@dataclass
class ApiConfig(Config):
    APP_NAME: str = "Aletheia Courses platform API REST"
    DEBUG: bool = True
    DATABASE_ECHO: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@postgres:5432/postgres"
    LOGGER_NAME: str = "api"

# SECRET_KEY = config("SECRET_KEY", cast=Secret, default="secret")
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*")
