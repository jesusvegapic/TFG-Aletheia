from typing import List
from pydantic import BaseModel


class DomainEvent(BaseModel):
    def __next__(self):
        yield self


class CompositeDomainEvent(DomainEvent):
    events: list[DomainEvent]

    def __next__(self):
        yield from self.events


DomainEvents = List[DomainEvent]
