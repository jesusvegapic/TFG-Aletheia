import re
from dataclasses import dataclass

from src.framework_ddd.core.domain.value_objects import ValueObject
from src.framework_ddd.mailing.domain.errors import EmailSubjectError, EmailBodyError, EmailError


@dataclass(frozen=True)
class Email(str):
    value: str

    def __post_init__(self):
        # Expresión regular para validar un correo electrónico
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, self.value):
            raise EmailError(email=self)

    def __str__(self):
        return self.value


class EmailSubject(str):
    def __new__(cls, value: str):
        if len(value) > EmailSubject.max_length():
            raise EmailSubjectError(actual_length=len(value), max_length=EmailSubject.max_length())
        else:
            return super().__new__(cls, value)

    @classmethod
    def max_length(cls):
        return 60


class EmailBody(str):
    def __new__(cls, value: str):
        bytes_length = len(value.encode("UTF-8"))
        if bytes_length > EmailBody.max_bytes_length():
            raise EmailBodyError(actual_bytes_length=bytes_length, max_bytes_length=EmailBody.max_bytes_length())
        else:
            super().__new__(cls, value)

    @classmethod
    def max_bytes_length(cls):
        return 25 * 1024 * 1024
