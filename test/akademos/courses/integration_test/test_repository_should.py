from src.akademos.courses.domain.entities import Course, Lectio
from src.akademos.courses.infrastructure.repository import SqlCourseRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyCourseRepositoryShould(TestInMemorySqlDatabase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlCourseRepository(self.session)

    async def test_save_valid_course(self):
        course = Course(
            id=Course.next_id().hex,
            owner=GenericUUID.next_id().hex,
            name="Kant vs Hegel",
            description="La panacea de la historía de la filosofía moderna",
            topics=[
                "Filosofía",
                "Literatura"
            ],
            lectios=[
                Lectio(
                    id=GenericUUID.next_id().hex,
                    name="contexto historico",
                    description="perspectiva materialista",
                    video_id=GenericUUID.next_id().hex
                )
            ]
        )

        await self.repository.add(course)
        await self.session.commit()
        course_found = await self.repository.get(course.id)

        self.assertEqual(course, course_found)
