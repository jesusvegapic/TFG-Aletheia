from unittest.mock import AsyncMock
from src.agora.students.application.commands.set_last_visited_lectio import SetLastVisitedLectio, \
    set_last_visited_lectio
from src.agora.students.domain.entities import StudentCourse, StudentLectio, Student
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.agora.students.students_module import TestStudentsModule, StudentMother


class SetLastVisitedLectioShould(TestStudentsModule):
    async def test_get_last_visited_on_a_course_if_exists_course(self):
        command = SetLastVisitedLectio(
            student_id=GenericUUID.next_id().hex,
            course_id=GenericUUID.next_id().hex,
            lectio_id=GenericUUID.next_id().hex
        )

        test_student = StudentMother.random(
            courses_in_progress=[
                StudentCourse(
                    id=GenericUUID.next_id().hex,
                    course_id=command.course_id,
                    lectios=[StudentLectio(id=StudentLectio.next_id().hex), StudentLectio(id=command.lectio_id)]
                )
            ]
        )

        self.repository.get = AsyncMock()
        self.repository.get.return_value = test_student
        self.repository.add = AsyncMock()

        publish = AsyncMock()

        await set_last_visited_lectio(command, self.repository, publish)

        args, kwargs = self.repository.add.call_args

        actual_student = args[0]

        actual_lectio_id = actual_student.get_last_visited_lectio(command.course_id)

        self.assertEqual(actual_lectio_id, GenericUUID(command.lectio_id))
