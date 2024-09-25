import re
from dataclasses import dataclass
from src.framework_ddd.core.domain.value_objects import ValueObject
from src.framework_ddd.iam.domain.errors import PersonalUserNameError, PersonalUserSurnamesError


@dataclass(frozen=True)
class Name(ValueObject, str):
    value: str

    def __post_init__(self):
        if len(self.value) > 20:
            raise PersonalUserNameError(name=self)

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Surnames(ValueObject):
    first_name: str
    second_name: str

    def __post_init__(self):
        if len(self.first_name) > 20 or len(self.second_name) > 20:
            raise PersonalUserSurnamesError(firstname=self.first_name, second_name=self.second_name)
