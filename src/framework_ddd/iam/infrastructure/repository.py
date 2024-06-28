import uuid
from sqlalchemy import Column, UUID, String, Boolean, ForeignKey, select
from sqlalchemy.exc import NoResultFound
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.domain.entities import User
from src.framework_ddd.iam.domain.repository import UserRepository
from src.framework_ddd.iam.domain.value_objects import Email


class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    is_superuser = Column(Boolean(), nullable=False)  # type: ignore


class PersonalUserModel(Base):
    __tablename__ = "personal_users"
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserModel.id), primary_key=True)
    name = Column(String(255), nulleable=False)
    firstname = Column(String(255), nulleable=False)
    secondname = Column(String(255), nulleable=False)


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
