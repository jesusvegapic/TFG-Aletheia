from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.framework_ddd.core.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
    is_superuser = Column(Boolean(), nullable=False)  # type: ignore


class PersonalUserModel(Base):
    __tablename__ = "personal_users"
    user_id = Column(UUIDType(binary=False), ForeignKey(UserModel.id), primary_key=True)  # type: ignore
    name = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)
    user = relationship(UserModel)

