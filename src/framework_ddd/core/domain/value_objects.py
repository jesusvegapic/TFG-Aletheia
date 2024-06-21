import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    ...


class GenericUUID(uuid.UUID):
    @classmethod
    def next_id(cls):
        return cls(int=uuid.uuid4().int)


class FacultyName(str):
    def __new__(cls, name: str):
        if name.__len__() > FacultyName.max_length():
            raise FacultyNameError(name, FacultyName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100
