from abc import ABC
from src.shared.domain.ddd.repository import GenericRepository
from src.shared.domain.ddd.value_objects import GenericUUID
from src.videos.domain.entities import Video


class VideoRepository(GenericRepository[GenericUUID, Video], ABC):
    pass
