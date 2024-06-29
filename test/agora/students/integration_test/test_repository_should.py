from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.agora.students.domain.entities import Student, StudentFaculty, StudentCourse, StudentLectio
from src.agora.students.infrastructure.repository import SqlAlchemyStudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyStudentRepositoryShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyStudentRepository(self.session)

    async def test_save_valid_student(self):
        degree_id = GenericUUID.next_id()
        faculty_id = GenericUUID.next_id().hex
        self.session.add(
            FacultyModel(
                id=faculty_id,
                name="Derecho",
                degrees=[
                    DegreeModel(
                        id=degree_id.hex,
                        name="Ade"
                    )
                ]
            )
        )

        await self.session.commit()

        student = Student(
            id=Student.next_id().hex,
            name="pepe",
            firstname="vega",
            second_name="picón",
            email="pepe@gmail.com",
            password_hash=b"passwd",
            faculty=StudentFaculty(
                id=faculty_id,
                degrees=[degree_id]
            ),
            degree=degree_id.hex,
            courses_in_progress=[
                StudentCourse(
                    id=StudentCourse.next_id().hex,
                    lectios=[
                        StudentLectio(
                            id=StudentLectio.next_id().hex
                        )
                    ]
                )
            ],
            last_visited_lectio=GenericUUID.next_id().hex

        )

        await self.repository.add(student)
        student_found = await self.repository.get(student.id)
        await self.session.commit()

        self.assertEqual(student, student_found)
