from src.shared.domain.entities import GenericUUID, DomainEvent


class CourseCreated(DomainEvent):
    id: GenericUUID
