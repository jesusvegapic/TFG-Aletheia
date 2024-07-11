from unittest.mock import AsyncMock

from src.agora.students.application.commands.finish_lectio import finish_lectio, FinishLectio
from src.agora.students.domain.entities import StudentLectio, StudentCourse
from src.agora.students.domain.value_objects import LectioStatus
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.agora.students.students_module import TestStudentsModule, StudentMother


class FinishLectioShould(TestStudentsModule):

    async def test_finish_a_lectio_correctly(self):
        self.repository.get = AsyncMock()
        fake_student = StudentMother.random(
            courses_in_progress=[
                StudentCourse(
                    id=StudentCourse.next_id().hex,
                    course_id=GenericUUID.next_id().hex,
                    lectios=[
                        StudentLectio(
                            id=StudentLectio.next_id().hex,
                            status=LectioStatus.STARTED
                        )
                    ]
                )
            ]
        )
        self.repository.get.return_value = fake_student
        self.repository.add = AsyncMock()

        publish = AsyncMock()

        await finish_lectio(
            command=FinishLectio(
                student_id=fake_student.id,
                course_id=fake_student.courses_in_progress[0].id,
                lectio_id=fake_student.courses_in_progress[0].lectios[0].id
            ),
            student_repository=self.repository,
            publish=publish
        )

        expected_lectio = StudentLectio(
            id=fake_student.courses_in_progress[0].lectios[0].id,
            status=LectioStatus.FINISHED
        )

        self.assertEqual(fake_student.courses_in_progress[0].lectios[0], expected_lectio)
