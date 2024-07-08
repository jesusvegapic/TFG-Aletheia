from src.agora.shared.application.queries import ListCoursesResponse, ListedCourseDto
from src.agora.students.application.queries.list_courses_enrolled import list_courses_enrolled, ListCoursesEnrolled
from src.agora.students.domain.entities import StudentCourse
from src.agora.students.infrastructure.repository import SqlAlchemyStudentRepository
from src.akademos.courses.domain.value_objects import CourseState
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import CourseModel
from test.agora.students.students_module import StudentMother
from test.shared.database import TestInMemorySqlDatabase


class ListCoursesEnrolledShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyStudentRepository(self.session)

    async def test_list_valid_courses(self):
        test_student = StudentMother.random(
            courses_in_progress=[
                StudentCourse(id=StudentCourse.next_id().hex),
                StudentCourse(id=StudentCourse.next_id().hex)
            ]
        )

        first_owner = GenericUUID.next_id()
        second_owner = GenericUUID.next_id()

        self.session.add(
            CourseModel(
                id=GenericUUID(test_student.courses_in_progress[0].id),
                owner=first_owner,
                name="Kant vs Hegel",
                description="La panacea de la historía de la filosofía",
                state=CourseState.CREATED,
                topics="Filosofía;Derecho"
            )
        )

        self.session.add(
            CourseModel(
                id=GenericUUID(test_student.courses_in_progress[1].id),
                owner=second_owner,
                name="Filosofía de Gustavo Bueno",
                description="Un comentario de los ensayos materialistas",
                state=CourseState.CREATED,
                topics="Filosofía;Derecho"
            )
        )

        await self.repository.add(test_student)

        await self.session.commit()

        query = ListCoursesEnrolled(student_id=test_student.id)

        response = await list_courses_enrolled(query, self.session)

        expected_response = ListCoursesResponse(
            courses=[
                ListedCourseDto(
                    id=test_student.courses_in_progress[0].id,
                    name="Kant vs Hegel",
                    owner=first_owner.hex
                ),
                ListedCourseDto(
                    id=test_student.courses_in_progress[1].id,
                    name="Filosofía de Gustavo Bueno",
                    owner=second_owner.hex
                )
            ]
        )

        self.assertEqual(response, expected_response)
