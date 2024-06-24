from abc import ABC

from src.akademos.videos.domain.entities import Video
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class VideoRepository(GenericRepository[GenericUUID, Video], ABC):
    pass
