from dataclasses import dataclass

from src.framework_ddd.core.domain.errors import DomainError, ApplicationError


class ConferencesModuleError(ApplicationError):
    ...


class CreateConferenceError(ConferencesModuleError):
    ...


@dataclass(frozen=True)
class ConferenceNameError(CreateConferenceError, DomainError):
    name: str
    max_length: int


@dataclass(frozen=True)
class ConferenceDescriptionError(CreateConferenceError, DomainError):
    description: str
    max_length: int
