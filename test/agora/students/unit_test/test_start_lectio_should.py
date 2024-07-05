from unittest.mock import AsyncMock
from src.agora.students.application.commands.start_lectio import start_lectio, StartLectio
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.agora.students.students_module import TestStudentsModule, StudentMother


class StartLectioShould(TestStudentsModule):

    async def test_start_a_lectio_correctly(self):
        self.repository.get = AsyncMock()
        fake_student = StudentMother.random()
        self.repository.get.return_value = fake_student
        self.repository.add = AsyncMock()

        def publish():
            ...

        await start_lectio(
            command=StartLectio(
                student_id=fake_student.id,
                course_id=fake_student.courses_in_progress[0].id,
                lectio_id=GenericUUID.next_id().hex
            ),
            student_repository=self.repository,
            publish=publish
        )
