from src.framework_ddd.core.domain.events import DomainEvent


class StudentCreated(DomainEvent):
    name: str
    firstname: str
    second_name: str
    email: str
    faculty_id: str
    degree_id: str


class StudentHasBeenEnrolledInACourse(DomainEvent):
    course_id: str
