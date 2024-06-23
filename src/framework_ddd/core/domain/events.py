from datetime import datetime

from lato import Event

from src.framework_ddd.core.domain.value_objects import GenericUUID


class DomainEvent(Event):  # type: ignore
    entity_id: str
    event_id: str
    ocurred_on: datetime

    def __init__(self, entity_id: str):
        super().__init__()
        self.entity_id = entity_id
        self.event_id = GenericUUID.next_id().hex
        self.ocurred_on = datetime.now()
