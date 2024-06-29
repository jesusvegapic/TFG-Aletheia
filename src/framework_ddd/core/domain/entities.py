from lato import Event
from pydantic import BaseModel

from src.framework_ddd.core.domain.buisness_rules import BusinessRuleValidationMixin
from src.framework_ddd.core.domain.value_objects import GenericUUID


class Entity(BaseModel):
    _id: GenericUUID

    def __init__(self, id: str):
        super().__init__()
        self._id = GenericUUID(id)

    @property
    def id(self):
        return self._id.hex

    @classmethod
    def next_id(cls) -> GenericUUID:
        return GenericUUID.next_id()

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True


class Aggregate(Entity):
    ...


class AggregateRoot(BusinessRuleValidationMixin, Entity):
    _events: list[Event]

    def __init__(self, id: str):
        super().__init__(id)
        self._events = []

    def _register_event(self, event: Event):
        self._events.append(event)

    def pull_domain_events(self):
        events = self._events
        self._events = []
        return events

