import abc
from abc import abstractmethod
from typing import Generic, TypeVar

from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.entities import User as DomainUser
from src.framework_ddd.iam.domain.value_objects import Email

User = TypeVar("User", bound=DomainUser)


class UserRepository(GenericRepository[GenericUUID, User], Generic[User], metaclass=abc.ABCMeta):
    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        ...
