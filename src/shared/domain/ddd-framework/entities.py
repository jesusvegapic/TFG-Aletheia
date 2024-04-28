from dataclasses import dataclass, field
from typing import TypeVar, Generic

from lato import Event

from src.shared.domain.ddd.buisness_rules import BusinessRuleValidationMixin
from src.shared.domain.ddd.value_objects import GenericUUID

EntityId = TypeVar("EntityId", bound=GenericUUID)


@dataclass
class Entity(Generic[EntityId]):
    id: EntityId = field(hash=True)

    @classmethod
    def next_id(cls) -> EntityId:
        return GenericUUID.next_id()


class Aggregate(Entity):
    ...


@dataclass(kw_only=True)
class AggregateRoot(BusinessRuleValidationMixin, Entity[EntityId]):
    events: list = field(default_factory=list)

    def register_event(self, event: Event):
        self.events.append(event)

    def collect_events(self):
        events = self.events
        self.events = []
        return events
