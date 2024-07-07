from unittest.mock import AsyncMock
from src.akademos.faculties.application.commands import CreateFaculty
from src.akademos.faculties.application.commands.create_faculty import DegreeDto, create_faculty
from src.akademos.faculties.domain.entities import Faculty, Degree
from src.akademos.faculties.domain.events import FacultyCreated
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.akademos.faculties.unit_test.faculties_module import TestFacultiesModule


class CreateFacultyShould(TestFacultiesModule):

    async def test_create_valid_faculty(self):
        command = CreateFaculty(
            faculty_id=GenericUUID.next_id().hex,
            name="Derecho",
            degrees=[
                DegreeDto(
                    id=GenericUUID.next_id().hex,
                    name="Ade"
                ),
                DegreeDto(
                    id=GenericUUID.next_id().hex,
                    name="Derecho"
                )
            ]
        )

        expected_faculty = Faculty(
            id=command.faculty_id,
            name=command.name,
            degrees=[
                Degree(
                    id=degree.id,
                    name=degree.name
                )
                for degree in command.degrees
            ]
        )

        self.repository.add = AsyncMock()

        publish = AsyncMock()

        await create_faculty(command, self.repository, publish)

        args, kwargs = self.repository.add.call_args

        self.assertEqual(args[0].model_dump(), expected_faculty.model_dump())

        args, kwargs = publish.call_args

        expected_event = FacultyCreated(
            entity_id=expected_faculty.id,
            name=expected_faculty.name,
            degrees=[degree.id for degree in expected_faculty.degrees]
        )

        self.assertEqual(args[0].event_dump(), expected_event.event_dump())
