from datetime import datetime
from typing import ClassVar, Any
from lato import Event


class DomainEvent(Event):  # type: ignore
    entity_id: str
    ocurred_on: ClassVar[datetime] = datetime.now()

    def event_dump(self) -> dict[str, Any]:
        return super().model_dump(exclude={"id", "ocurred_on"})
