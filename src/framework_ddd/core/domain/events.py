from dataclasses import field, dataclass
from datetime import datetime
from uuid import uuid4

from lato import Event


@dataclass(frozen=True)
class DomainEvent(Event):  # type: ignore
    entity_id: str
    event_id: str = field(default_factory=lambda: uuid4().hex, init=False)
    ocurred_on: datetime = field(default_factory=datetime.now, init=False)
