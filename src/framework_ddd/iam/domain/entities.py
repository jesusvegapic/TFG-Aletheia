from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.iam.domain.value_objects import Name, Surnames
from src.framework_ddd.mailing.domain.value_objects import Email


class User(AggregateRoot):
    _email: Email
    _hashed_password: bytes
    _is_superuser: bool

    def __init__(self, id: str, email: str, hashed_password: bytes, is_superuser: bool):
        super().__init__(id)
        self._email = Email(email)
        self._hashed_password = hashed_password
        self._is_superuser = is_superuser

    @property
    def email(self) -> str:
        return self._email

    @property
    def hashed_password(self):
        return self._hashed_password

    @property
    def is_superuser(self):
        return self._is_superuser


class PersonalUser(User):
    _name: Name
    _surnames: Surnames

    def __init__(
            self,
            id: str,
            name: str,
            firstname: str,
            second_name: str,
            email: str,
            hashed_password: bytes,
            is_superuser: bool
    ):
        super().__init__(id, email, hashed_password, is_superuser)
        self._name = Name(name)
        self._surnames = Surnames(firstname, second_name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def firstname(self):
        return self._surnames.first_name

    @property
    def second_name(self):
        return self._surnames.second_name
