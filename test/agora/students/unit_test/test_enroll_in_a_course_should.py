from unittest.mock import AsyncMock
from src.agora.shared.application.queries import GetCourseResponse, LectioDto
from src.agora.students.application.commands.enroll_in_a_course import EnrollInACourse, enroll_in_a_course
from src.agora.students.domain.entities import Student, StudentCourse, StudentLectio, StudentFaculty
from src.agora.students.domain.events import StudentHasBeenEnrolledInACourse
from src.framework_ddd.core.domain.events import DomainEvent
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
        derecho_id = GenericUUID.next_id()

        events = []

        async def publish(event: DomainEvent):
            events.append(event)

        publish_query = AsyncMock()
        publish_query.return_value = GetCourseResponse(
            id=course_id,
            name="kant vs hegel",
            owner=owner_id,
            description="la panacea de la filosofia",
            topics=["Filosofía", "Linguistica"],
            lectios=[
                LectioDto(
                    id=lectio_id,
                    name="Contexto histórico"
                )
            ]
        )

        course_expected = StudentCourse(
            id=course_id,
            lectios=[StudentLectio(id=lectio_id)]
        )

        command = EnrollInACourse(
            student_id=student_id,
            course_id=course_id
        )

        self.repository.get = AsyncMock()

        student_faculty = StudentFaculty(faculty_id, [derecho_id])

        student_initial_args = {
            "id": student_id,
            "name": "pepe",
            "firstname": "vega",
            "second_name": "fernandez",
            "email": "pepe@gmail.com",
            "password_hash": b"papapapa",
            "faculty": student_faculty,
            "degree": derecho_id.hex
        }

        self.repository.get.return_value = Student(**student_initial_args)

        expected_student = Student(
            courses_in_progress=[course_expected],
            **student_initial_args
        )

        self.repository.add = AsyncMock()

        await enroll_in_a_course(command, self.repository, publish_query, publish)

        args, kwargs = self.repository.add.call_args

        actual_student = args[0]

        self.assertEqual(actual_student, expected_student)
        self.assertTrue(len(events) == 1)
        self.assertTrue(isinstance(events[0], StudentHasBeenEnrolledInACourse))
        self.assertEqual(
            events[0].event_dump(),
            StudentHasBeenEnrolledInACourse(
                entity_id=expected_student.id,
                course_id=course_expected.id
            ).event_dump()
        )
