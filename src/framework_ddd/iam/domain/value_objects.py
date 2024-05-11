from dataclasses import dataclass
from typing import re  # type: ignore

from src.framework_ddd.core.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Name(ValueObject):
    value: str

    def __post_init__(self):
        if len(self.value) > 20:
            raise DomainException()


@dataclass(frozen=True)
class Surnames(ValueObject):
    first_name: str
    second_name: str

    def __post_init__(self):
        if len(self.first_name) > 20 or len(self.second_name) > 20:
            raise DomainException()


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def __post_init__(self):
        # Expresión regular para validar un correo electrónico
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, self.value):
            raise EmailError()

