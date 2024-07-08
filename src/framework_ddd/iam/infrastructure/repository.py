from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.domain.entities import User
from src.framework_ddd.iam.domain.repository import UserRepository
from src.framework_ddd.iam.domain.value_objects import Email
from src.framework_ddd.iam.infrastructure.user_model import UserModel


class UserDataMapper(DataMapper):
    def model_to_entity(self, instance: UserModel) -> User:
        return User(
            id=instance.id.hex,  # type: ignore
            email=instance.email,  # type: ignore
            hashed_password=instance.password,  # type: ignore
            is_superuser=instance.is_superuser,  # type: ignore
        )

    def entity_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=GenericUUID(entity.id),
            email=entity.email,
            password=entity.hashed_password,  # type: ignore
            is_superuser=entity.is_superuser,
        )


class SqlAlchemyUserRepository(SqlAlchemyGenericRepository, UserRepository):
    """Listing repository implementation"""

    mapper_class = UserDataMapper
    model_class = UserModel

    async def get_by_email(self, email: Email) -> User | None:
        try:
            instance = (await self._session.execute(select(UserModel).where(UserModel.email == email))).scalar_one()
            return self._get_entity(instance)
        except NoResultFound:
            return None
