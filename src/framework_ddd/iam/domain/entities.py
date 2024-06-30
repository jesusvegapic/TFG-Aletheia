from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.iam.domain.value_objects import Name, Surnames, Email


class User(AggregateRoot):
    _email: Email
    _password_hash: bytes
    _is_superuser: bool

    def __init__(self, id: str, email: str, password_hash: bytes, is_superuser: bool):
        super().__init__(id)
        self._email = Email(email)
        self._password_hash = password_hash
        self._is_superuser = is_superuser

    @property
    def email(self) -> str:
        return self._email

    @property
    def password_hash(self):
        return self._password_hash

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
            password_hash: bytes,
            is_superuser: bool
    ):
        super().__init__(id, email, password_hash, is_superuser)
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
