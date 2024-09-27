from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.akademos.teachers.domain.entities import Teacher, TeacherFaculty
from src.akademos.teachers.domain.value_objects import TeacherPosition
from src.akademos.teachers.infrastructure.repository import SqlAlchemyTeacherRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyTeacherRepositoryShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyTeacherRepository(self.session)

    async def test_save_valid_teacher(self):
        degrees_id = [GenericUUID.next_id().hex, GenericUUID.next_id().hex]
        faculty_id = GenericUUID.next_id().hex
        self.session.add(
            FacultyModel(
                id=faculty_id,
                name="Derecho",
                degrees=[
                    DegreeModel(
                        id=degrees_id[0],
                        name="Ade"
                    ),
                    DegreeModel(
                        id=degrees_id[1],
                        name="Derecho"
                    )
                ]
            )
        )

        await self.session.commit()

        teacher = Teacher(
            id=Teacher.next_id().hex,
            name="pepe",
            firstname="vega",
            second_name="picón",
            email="pepe@gmail.com",
            hashed_password=b"passwd",
            faculty=TeacherFaculty(
                id=faculty_id,
                degrees=[GenericUUID(degree) for degree in degrees_id]
            ),
            degrees=degrees_id,
            position=TeacherPosition.SENIOR_LECTURER
        )

        await self.repository.add(teacher)
        await self.session.commit()
        teacher_found = await self.repository.get(teacher.id)
        await self.session.commit()

        self.assertEqual(teacher, teacher_found)
