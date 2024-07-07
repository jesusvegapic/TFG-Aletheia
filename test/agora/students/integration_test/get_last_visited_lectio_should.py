from src.agora.shared.application.queries import GetLectioResponse
from src.agora.students.application.queries.get_last_visited_lectio import get_last_visited_lectio, GetLastVisitedLectio
from src.agora.students.domain.entities import StudentCourse, StudentLectio
from src.agora.students.infrastructure.repository import SqlAlchemyStudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import LectioModel
from test.agora.students.students_module import StudentMother
from test.shared.database import TestInMemorySqlDatabase


class GetLastVisitedLectioShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyStudentRepository(self.session)

    async def test_get_valid_lectio(self):
        lectio_id = StudentLectio.next_id()
        course_id = StudentCourse.next_id().hex
        video_id = GenericUUID.next_id()
        self.session.add(
            LectioModel(
                id=lectio_id,
                name="Kant vs Hegel",
                description="La panacea de la historía de la filosofía",
                video_id=video_id
            )
        )

        test_student = StudentMother.random(
            courses_in_progress=[
                StudentCourse(
                    id=course_id,
                    lectios=[StudentLectio(id=lectio_id.hex)],
                    last_visited_lectio=lectio_id
                )
            ]
        )

        query = GetLastVisitedLectio(
            student_id=test_student.id,
            course_id=course_id
        )

        await self.repository.add(test_student)
        await self.session.commit()

        response = await get_last_visited_lectio(query, self.session)

        expected_response = GetLectioResponse(
            lectio_id=lectio_id.hex,
            name="Kant vs Hegel",
            description ="La panacea de la historía de la filosofía",
            video_id =video_id.hex
        )

        self.assertEqual(response, expected_response)
