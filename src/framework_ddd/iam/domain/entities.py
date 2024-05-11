from dataclasses import dataclass, Field
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.value_objects import Name, Surnames, Email


@dataclass
class User(AggregateRoot):
    email: Email
    password_hash: bytes
    is_superuser: bool = Field(default=False)  # type: ignore

    @property
    def username(self):
        return self.email

    @username.setter
    def username(self, value):
        self.email = value


class AnonymousUser(User):
    def __init__(self):
        super().__init__(
            id=GenericUUID("00000000-0000-0000-0000-000000000000"),
            email=None,
            password_hash=b""
        )

    @property  # type: ignore
    def username(self):
        return "<anonymous>"


@dataclass
class PersonalUser(User):
    name: Name
    surname: Surnames


