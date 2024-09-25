from dataclasses import dataclass

from src.framework_ddd.core.domain.errors import DomainError, ApplicationError


class CreateEmailMessageError(ApplicationError):
    ...


@dataclass(frozen=True)
class EmailSubjectError(CreateEmailMessageError, DomainError):
    actual_length: int
    max_length: int


@dataclass(frozen=True)
class EmailBodyError(CreateEmailMessageError, DomainError):
    actual_bytes_length: int
    max_bytes_length: int


@dataclass(frozen=True)
class EmailError(DomainError):
    email: str
