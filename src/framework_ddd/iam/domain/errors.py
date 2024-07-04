from dataclasses import dataclass
from src.framework_ddd.core.domain.errors import DomainError


@dataclass(frozen=True)
class PersonalUserNameError(DomainError):
    name: str


@dataclass(frozen=True)
class PersonalUserSurnamesError(DomainError):
    firstname: str
    second_name: str


@dataclass(frozen=True)
class EmailError(DomainError):
    email: str


@dataclass(frozen=True)
class InvalidCredentialsException(DomainError):
    ...


@dataclass(frozen=True)
class ExpiredTokenError(DomainError):
    ...
