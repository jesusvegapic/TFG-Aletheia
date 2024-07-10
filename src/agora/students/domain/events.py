from typing import List

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


class LectioHasBeenVisitedOnStudentCourse(DomainEvent):
    course_id: str
    lectio_id: str


class StudentSubscribedToTeacherCourses(DomainEvent):
    subscription_id: str
    teacher_id: str
    topics: List[str]
