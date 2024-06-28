from dataclasses import dataclass
from src.akademos.videos.domain.errors import VideoApplicationError
from src.framework_ddd.core.infrastructure.errors import RepositoryError, InconsistentDatabaseError


class AsyncMotorGridFsVideoRepositoryError(RepositoryError, VideoApplicationError):
    ...


@dataclass(frozen=True)
class NullContentType(AsyncMotorGridFsVideoRepositoryError, InconsistentDatabaseError):
    id: str

