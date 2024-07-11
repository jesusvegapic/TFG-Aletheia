from src.agora.shared.application.queries import LectioProgressDto
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.agora.students.application.queries.get_course_state_progress import get_course_state_progress, \
    GetCourseStateProgress, GetCourseStateProgressResponse
from src.agora.students.domain.entities import StudentCourse, StudentLectio
from src.agora.students.domain.value_objects import LectioStatus
from src.agora.students.infrastructure.repository import SqlAlchemyStudentRepository
from src.akademos.teachers.infrastructure.repository import TeacherDegreesModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.domain.value_objects import CourseState
from src.shared.infrastructure.sql_alchemy.models import TeacherModel, CourseModel, LectioModel
from test.agora.students.students_module import StudentMother
from test.shared.database import TestInMemorySqlDatabase


class GetCourseStateProgressShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyStudentRepository(self.session)

    async def test_get_course_state_progress(self):
        faculty_id = GenericUUID.next_id()
        degree_id = GenericUUID.next_id()
        self.session.add(
            FacultyModel(
                id=faculty_id,
                name="Derecho",
                degrees=[
                    DegreeModel(
                        id=degree_id,
                        name="Derecho"
                    ),
                    DegreeModel(
                        id=GenericUUID.next_id(),
                        name="Filosofía"
                    )
                ]
            )
        )

        teacher_id = GenericUUID.next_id()

        self.session.add(
            TeacherModel(
                personal_user_id=teacher_id,
                faculty_id=faculty_id,
                position="FULL_PROFESSOR",
                degrees=[TeacherDegreesModel(
                    id=degree_id,
                    teacher_id=teacher_id
                )],
                personal_user=PersonalUserModel(
                    user_id=teacher_id,
                    name="pepito",
                    firstname="gonzalez",
                    second_name="perez",
                    user=UserModel(
                        id=teacher_id,
                        email="pepito@gmail.com",
                        password="dadada",
                        is_superuser=True
                    )
                )
            )
        )

        course_id = GenericUUID.next_id()

        first_lectio_id = GenericUUID.next_id()
        second_lectio_id = GenericUUID.next_id()

        self.session.add(
            CourseModel(
                id=course_id,
                owner=teacher_id,
                name="Kant vs hegel",
                description="La panacea de la historia de la filosofía",
                state=CourseState.PUBLISHED,
                topics="Filosofía;Biología",
                lectios=[
                    LectioModel(
                        id=first_lectio_id,
                        name="irrelevante",
                        description="mas irrelevante",
                        video_id=GenericUUID.next_id()
                    ),
                    LectioModel(
                        id=second_lectio_id,
                        name="irrelevante",
                        description="mas irrelevante",
                        video_id=GenericUUID.next_id()
                    )
                ]
            )
        )

        student = StudentMother.random(
            courses_in_progress=[
                StudentCourse(
                    id=course_id.hex,
                    lectios=[
                        StudentLectio(
                            id=first_lectio_id.hex,
                            status=LectioStatus.FINISHED
                        ),
                        StudentLectio(
                            id=second_lectio_id.hex,
                            status=LectioStatus.STARTED
                        )
                    ]
                )
            ]
        )

        await self.repository.add(student)
        await self.session.commit()

        query = GetCourseStateProgress(
            student_id=student.id,
            course_id=course_id.hex
        )

        response = await get_course_state_progress(query, self.session)

        first_lectio = student.courses_in_progress[0].lectios[0]
        second_lectio = student.courses_in_progress[0].lectios[1]

        response_expected = GetCourseStateProgressResponse(
            lectios_progress=[
                LectioProgressDto(
                    id=first_lectio.id,
                    name="irrelevante",
                    progress=first_lectio.status
                ),
                LectioProgressDto(
                    id=second_lectio.id,
                    name="irrelevante",
                    progress=second_lectio.status
                )
            ],
            course_percent_progress=50
        )

        self.assertEqual(response, response_expected)
