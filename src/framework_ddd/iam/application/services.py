import datetime
from datetime import timedelta
import bcrypt
import jwt
from pydantic import BaseModel
from src.framework_ddd.iam.domain.errors import InvalidCredentialsException, ExpiredTokenError
from src.framework_ddd.iam.domain.repository import UserRepository, User
from src.framework_ddd.iam.domain.value_objects import Email


class IamUserInfo(BaseModel):
    email: str
    user_id: str
    is_superuser: bool


class IamService:
    __user_repository: UserRepository
    __secret_key: str
    __algorithm: str
    __access_token_expire_after_minutes: int

    def __init__(
            self,
            user_repository: UserRepository,
            secret_key: str,
            algorithm: str = "HS256",
            access_token_expire_after_minutes: int = 240
    ):
        self.__user_repository = user_repository
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__access_token_expire_after_minutes = access_token_expire_after_minutes

    @classmethod
    def hash_password(cls, password: str):
        hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
        return hashed_password

    async def authenticate_with_email_and_password(self, email: str, password: str):
        user = await self.__user_repository.get_by_email(Email(email))
        if not user:
            raise InvalidCredentialsException()

        password_match = bcrypt.checkpw(
            password.encode("UTF-8"), user.hashed_password
        )

        if not password_match:
            raise InvalidCredentialsException()

        return self.create_access_token_for_user(user)

    def create_access_token_for_user(self, user):
        access_token_expires = timedelta(minutes=self.__access_token_expire_after_minutes)

        data = {"sub": user.email, "id": user.id, "is_superuser": user.is_superuser}

        to_encode = data.copy()

        expire = datetime.datetime.now(datetime.UTC) + access_token_expires

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
        return encoded_jwt

    def get_userid_from_token(self, token: str):
        payload = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        expired: float = payload["exp"]
        if datetime.datetime.now(datetime.UTC) > datetime.datetime.fromtimestamp(expired, tz=datetime.UTC):
            raise ExpiredTokenError()

        return IamUserInfo(email=payload["sub"], user_id=payload["id"], is_superuser=payload["is_superuser"])
