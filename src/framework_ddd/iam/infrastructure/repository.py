import uuid

from sqlalchemy import Column, UUID, String, Boolean, ForeignKey

from src.framework_ddd.core.infrastructure.ddd_repositories.data_mapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.core.infrastructure.sql_alchemy.sql_alchemy_database import Base
from src.framework_ddd.iam.domain.entities import User
from src.framework_ddd.iam.domain.repository import UserRepository


class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    is_superuser = Column(Boolean(), nullable=False)


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

    def get_by_access_token(self, access_token: str) -> User | None:
        try:
            instance = (
                self._session.query(UserModel)
                .filter_by(access_token=access_token)
                .one()
            )
            return self._get_entity(instance)
        except NoResultFound:
            return None

    def get_by_email(self, email: Email) -> User | None:
        try:
            instance = self._session.query(UserModel).filter_by(email=email).one()
            return self._get_entity(instance)
        except NoResultFound:
            return None