from typing import Optional, List
from unittest.mock import AsyncMock

from lato.message import Message

from src.akademos.faculties.application.queries.get_faculty import GetFaculty, GetFacultyResponse
from src.akademos.teachers.application.commands.sign_up_teacher import SignUpTeacher, sign_up_teacher
from src.akademos.teachers.domain.entities import Teacher, TeacherFaculty
from src.akademos.teachers.domain.events import TeacherCreated
from src.akademos.teachers.domain.value_objects import TeacherPosition
from src.framework_ddd.core.domain.events import DomainEvent
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.application.services import IamService
from test.akademos.teachers.unit_test.teachers_module import TestTeachersModule


class SignupTeacherShould(TestTeachersModule):

    async def test_sign_up_valid_teacher(self):
        command = SignUpTeacher(
            teacher_id=GenericUUID.next_id().hex,
            email="pepito@gmail.com",
            password="oi56ujdf",
            name="pepito",
            firstname="sanchez",
            second_name="fenandez",
            faculty_id=GenericUUID.next_id().hex,
            degrees=[GenericUUID.next_id().hex, GenericUUID.next_id().hex],
            position=TeacherPosition.FULL_PROFESSOR
        )

        hashed_password = IamService.hash_password(command.password)

        teacher_expected = Teacher(
            command.teacher_id,
            command.email,
            hashed_password,
            command.name,
            command.firstname,
            command.second_name,
            TeacherFaculty(
                command.faculty_id,
                [GenericUUID(degree) for degree in command.degrees]
            ),
            command.degrees,
            command.position
        )

        self.repository.add = AsyncMock()

        events = []

        async def publish(message: Message):
            if isinstance(message, GetFaculty):
                return GetFacultyResponse(
                    id=command.faculty_id,
                    name="Derecho",
                    degrees=command.degrees
                )
            elif isinstance(message, DomainEvent):
                events.append(message)

        await sign_up_teacher(command, self.repository, publish)

        args, kwargs = self.repository.add.call_args

        self.assertEqual(args[0], teacher_expected)

        expected_event = TeacherCreated(
            entity_id=teacher_expected.id,
            mail=command.email,
            hashed_password=hashed_password,
            name=command.name,
            firstname=command.firstname,
            second_name=command.second_name,
            faculty_id=command.faculty_id,
            degrees=command.degrees,
            position=command.position
        )

        self.assertEqual(events[0], expected_event)
