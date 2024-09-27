from src.akademos.faculties.domain.entities import Faculty, Degree
from src.akademos.faculties.infrastructure.repository import SqlAlchemyFacultyRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyFacultyRepositoryShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyFacultyRepository(self.session)

    async def test_add_valid_faculty(self):
        faculty = Faculty(
            id=Faculty.next_id().hex,
            name="Derecho",
            degrees=[
                Degree(
                    id=Degree.next_id().hex,
                    name="Ade"
                ),
                Degree(
                    id=Degree.next_id().hex,
                    name="Derecho"
                )
            ]
        )

        await self.repository.add(faculty)
        await self.session.commit()

        actual_faculty = await self.repository.get(GenericUUID(faculty.id))

        self.assertEqual(actual_faculty, faculty)
