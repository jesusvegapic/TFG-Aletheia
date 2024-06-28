from typing import Union, List
from unittest.mock import AsyncMock
from lato.message import Query
from src.agora.shared.application.queries import GetCourse, GetCourseResponse, LectioDto
from src.agora.students.application.commands.enroll_in_a_course import EnrollInACourse, enroll_in_a_course
from src.agora.students.domain.entities import Student, StudentCourse, StudentLectio
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.agora.students.students_module import TestStudentsModule


class EnrollInACourseShould(TestStudentsModule):

    def setUp(self):
        super().setUp()

    async def test_enroll_in_as_course_correctly(self):
        student_id = GenericUUID.next_id().hex
        course_id = GenericUUID.next_id().hex
        faculty_id = GenericUUID.next_id().hex
        owner_id = GenericUUID.next_id().hex
        lectio_id = GenericUUID.next_id().hex
        derecho_id = GenericUUID.next_id().hex

        async def publish(message: Union[Query, List]):
            if isinstance(message, GetCourse):
                return GetCourseResponse(
                    id=course_id,
                    name="kant vs hegel",
                    owner=owner_id,
                    description="la panacea de la filosofia",
                    lectios=[
                        LectioDto(
                            id=lectio_id,
                            name="Contexto histórico"
                        )
                    ]
                )

        course_expected = StudentCourse(
            id=course_id,
            lectios={StudentLectio(id=lectio_id)}
        )

        command = EnrollInACourse(
            student_id=student_id,
            course_id=course_id
        )

        self.repository.get = AsyncMock()

        student_initial_args = {
            "id": student_id,
            "name": "pepe",
            "firstname": "vega",
            "second_name": "fernandez",
            "email": "pepe@gmail.com",
            "password_hash": b"papapapa",
            "is_superuser": False,
            "faculty": faculty_id,
            "degree": derecho_id
        }

        self.repository.get.return_value = Student(**student_initial_args)

        expected_student = Student(
            courses_in_progress={course_expected},
            **student_initial_args
        )

        self.repository.add = AsyncMock()

        await enroll_in_a_course(command, self.repository, publish)

        args, kwargs = self.repository.add.call_args

        actual_student = args[0]

        self.assertEqual(actual_student, expected_student)
