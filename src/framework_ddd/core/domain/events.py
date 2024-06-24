from datetime import datetime
from typing import ClassVar

from lato import Event

from src.framework_ddd.core.domain.value_objects import GenericUUID


class DomainEvent(Event):  # type: ignore
    entity_id: str
    event_id: ClassVar[str] = GenericUUID.next_id().hex
    ocurred_on: ClassVar[datetime] = datetime.now()
