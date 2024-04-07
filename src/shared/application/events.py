import sys
from dataclasses import field, dataclass
from typing import Any

from pydantic import BaseModel

from src.shared.domain.events import DomainEvent
from src.shared.domain.value_objects import GenericUUID


class EventId(GenericUUID):
    ...


class IntegrationEvent(BaseModel):
    """
    Integration events are used to communicate between modules/system via inbox-outbox pattern.
    They are created in a domain event handler and then saved in an outbox for further delivery.
    As a result, integration events are handled asynchronously.
    """


@dataclass
class EventResult:
    """
    Result of event execution (success or failure) by an event handler.
    """

    event_id: EventId = field(default_factory=EventId.next_id)
    payload: Any = None
    command: Any = (
        None  # command to be executed as a result of this event (experimental)
    )
    events: list[DomainEvent] = field(default_factory=list)
    errors: list[Any] = field(default_factory=list)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def is_success(self) -> bool:
        return not self.has_errors()

    def __hash__(self):
        return id(self)

    @classmethod
    def failure(cls, message="Failure", exception=None) -> "EventResult":
        exception_info = sys.exc_info()
        errors = [(message, exception, exception_info)]
        result = cls(errors=errors)
        return result

    @classmethod
    def success(
            cls, event_id=None, payload=None, command=None, event=None, events=None
    ) -> "EventResult":
        if events is None:
            events = []
        if event:
            events.append(event)
        return cls(event_id=event_id, payload=payload, command=command, events=events)


class EventResultSet(set):

    def is_success(self):
        return all([r.is_success() for r in self])

    @property
    def events(self):
        all_events = []
        for event in self:
            all_events.extend(event.events)
        return all_events

    @property
    def commands(self):
        all_commands = [event.command for event in self if event.command]
        return all_commands
