from lato import Event

from src.framework_ddd.core.domain.buisness_rules import BusinessRuleValidationMixin
from src.framework_ddd.core.domain.value_objects import GenericUUID


class Entity:
    _id: GenericUUID

    def __init__(self, id: str):
        self._id = GenericUUID(id)

    @property
    def id(self):
        return self._id.hex

    @classmethod
    def next_id(cls) -> GenericUUID:
        return GenericUUID.next_id()


class Aggregate(Entity):
    ...


class AggregateRoot(BusinessRuleValidationMixin, Entity):
    _events: list[Event]

    def _register_event(self, event: Event):
        self._events.append(event)

    def pull_domain_events(self):
        events = self._events
        self._events = []
        return events
