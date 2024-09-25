from dataclasses import dataclass


class InfrastructureError(Exception):
    pass


class RepositoryError(InfrastructureError):
    ...


class InconsistentDatabaseError(InfrastructureError):
    ...


class AsyncMotorGridFsGenericRepositoryError(RepositoryError):
    ...


@dataclass(frozen=True)
class NullFilename(AsyncMotorGridFsGenericRepositoryError, InconsistentDatabaseError):
    id: str

@dataclass(frozen=True)
class NullContentType(AsyncMotorGridFsGenericRepositoryError, InconsistentDatabaseError):
    id: str
