from dataclasses import dataclass

from src.shared.domain.iam.entities import User


@dataclass(kw_only=True)
class Student(User):
    courses: list[GenericUUID]

    def enroll_in_a_course(self, course_id: GenericUUID):
        self.courses.append(course_id)
