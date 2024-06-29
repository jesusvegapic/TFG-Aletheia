from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.domain.entities import User
from src.framework_ddd.iam.domain.repository import UserRepository
from src.framework_ddd.iam.domain.value_objects import Email
from src.framework_ddd.iam.infrastructure.user_model import UserModel


class UserDataMapper(DataMapper):
    def model_to_entity(self, instance: UserModel) -> User:
        return User(
            id=instance.id,
            email=instance.email,
            password_hash=instance.password,
            is_superuser=instance.is_superuser,
        )

    def entity_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            password=entity.password_hash,
            is_superuser=entity.is_superuser,
        )


class SqlAlchemyUserRepository(SqlAlchemyGenericRepository, UserRepository):
    """Listing repository implementation"""

    mapper_class = UserDataMapper
    model_class = UserModel

    async def get_by_access_token(self, access_token: str) -> User | None:
        try:
            instance = (
                await self._session.execute(
                    select(UserModel)
                    .filter_by(access_token=access_token)
                )
            ).one()

            return self._get_entity(instance)
        except NoResultFound:
            return None

    async def get_by_email(self, email: Email) -> User | None:
        try:
            instance = (await self._session.execute(select(UserModel).filter_by(email=email))).one()
            return self._get_entity(instance)
        except NoResultFound:
            return None
