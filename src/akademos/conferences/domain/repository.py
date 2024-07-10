from abc import ABC

from src.akademos.conferences.domain.entities import Conference
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class ConferenceRepository(GenericRepository[GenericUUID, Conference], ABC):
    ...
