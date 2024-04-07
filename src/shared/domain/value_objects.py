import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    ...


class GenericUUID(uuid.UUID):
    @classmethod
    def next_id(cls):
        return cls(int=uuid.uuid4().int)
