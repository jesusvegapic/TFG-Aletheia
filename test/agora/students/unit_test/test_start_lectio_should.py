from unittest.mock import AsyncMock
from src.agora.students.application.commands.start_lectio import start_lectio, StartLectio
from src.agora.students.domain.entities import StudentLectio
from src.agora.students.domain.value_objects import LectioStatus
from test.agora.students.students_module import TestStudentsModule, StudentMother


class StartLectioShould(TestStudentsModule):

    async def test_start_a_lectio_correctly(self):
        self.repository.get = AsyncMock()
        fake_student = StudentMother.random()
        self.repository.get.return_value = fake_student
        self.repository.add = AsyncMock()

        publish = AsyncMock()

        await start_lectio(
            command=StartLectio(
                student_id=fake_student.id,
                course_id=fake_student.courses_in_progress[0].course_id,
                lectio_id=fake_student.courses_in_progress[0].lectios[0].id
            ),
            student_repository=self.repository,
            publish=publish
        )

        expected_lectio = StudentLectio(
            id=fake_student.courses_in_progress[0].lectios[0].id,
            status=LectioStatus.STARTED
        )

        self.assertEqual(fake_student.courses_in_progress[0].lectios[0].model_dump(), expected_lectio.model_dump())
