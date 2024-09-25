from unittest.mock import AsyncMock
from src.agora.students.application.commands.sing_up_student import SignUpStudent, sign_up_student
from src.agora.students.domain.entities import Student, StudentFaculty
from src.agora.students.domain.events import StudentCreated
from src.akademos.faculties.application.queries.get_faculty import GetFaculty, GetFacultyResponse
from src.framework_ddd.core.domain.events import DomainEvent
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.application.services import IamService
from test.agora.students.students_module import TestStudentsModule


class SignupStudentShould(TestStudentsModule):
    async def test_signup_valid_student(self):
        command = SignUpStudent(
            student_id=GenericUUID.next_id().hex,
            email="pepito@gmail.com",
            password="oi56ujdf",
            name="pepito",
            firstname="sanchez",
            second_name="fenandez",
            faculty=GenericUUID.next_id().hex,
            degree=GenericUUID.next_id().hex
        )

        hashed_password = IamService.hash_password(command.password)

        teacher_expected = Student(
            command.student_id,
            command.name,
            command.firstname,
            command.second_name,
            command.email,
            hashed_password,
            StudentFaculty(
                command.faculty,
                [GenericUUID(command.degree)]
            ),
            command.degree
        )

        self.repository.add = AsyncMock()

        events = []

        async def publish(event: DomainEvent):
            events.append(event)

        publish_query = AsyncMock()
        publish_query.return_value = GetFacultyResponse(
            id=command.faculty,
            name="Derecho",
            degrees=[command.degree]
        )

        await sign_up_student(command, self.repository, publish_query, publish)

        args, kwargs = self.repository.add.call_args

        self.assertEqual(args[0].model_dump(), teacher_expected.model_dump())

        expected_event = StudentCreated(
            entity_id=teacher_expected.id,
            email=command.email,
            hashed_password=hashed_password,
            name=command.name,
            firstname=command.firstname,
            second_name=command.second_name,
            faculty_id=command.faculty,
            degree_id=command.degree
        )

        self.assertEqual(events[0].event_dump(), expected_event.event_dump())
