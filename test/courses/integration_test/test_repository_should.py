from unittest import IsolatedAsyncioTestCase

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.Academia.courses.domain.entities import Course
from src.Academia.courses.domain.value_objects import CourseName, CourseDescription
from src.Academia.courses.infrastructure.repository import SqlCourseRepository
from src.shared.domain.ddd.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.sql_alchemy.sql_alchemy_database import Base


class SqlAlchemyCourseRepositoryShould(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
        cls.session_factory = async_sessionmaker(
            bind=engine
        )
        cls.engine = engine

    async def asyncSetUp(self):
        self.session = self.session_factory()
        self.repository = SqlCourseRepository(self.session)
        async with self.engine.connect() as db:
            await db.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        await self.session.close()

    async def test_save_valid_course(self):
        course_id = Course.next_id()
        teacher_id = GenericUUID.next_id()
        course = Course(
            id=course_id,
            owner=teacher_id,
            name=CourseName("Kant vs Hegel"),
            description=CourseDescription("La panacea de la historía de la filosofía moderna")
        )
        self.repository.add(course)
        course_found = await self.repository.get(course.id)
        await self.session.commit()

        self.assertEqual(course, course_found)
