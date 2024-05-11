from functools import reduce

from sqlalchemy import Column, ForeignKey, Enum, PrimaryKeyConstraint, CheckConstraint, select, \
    ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.platform.students.domain.entities import Student, Faculty
from src.platform.students.domain.repository import StudentRepository
from src.platform.students.domain.value_objects import LectioStatus, Name, Surnames
from src.framework_ddd.core.infrastructure.ddd_repositories.data_mapper import DataMapper
from src.framework_ddd.core.infrastructure.sql_alchemy.sql_alchemy_database import Base
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.shared.utils.structures import merge_dict


class StudentModel(Base):
    __tablename__ = "students"
    user_id = Column(UUIDType(binary=False), ForeignKey=UserModel.id, primary_key=True)
    faculty_id = Column(UUIDType(binary=False), ForeignKey(FacultyModel.id))  # type: ignore
    degree_id = Column(UUIDType(binary=False), ForeignKey(DegreeModel.id))  # type: ignore
    faculty = relationship(FacultyModel)
    degree = relationship(DegreeModel)
    enrolled_courses = relationship(
        "StudentEnrolledCourseModel",
        back_populates="student"
    )
    last_visited_lectio = relationship("StudentLectioModel")


class StudentEnrolledCourseModel(Base):
    __tablename__ = "students_enrolled_courses"
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.id))  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    course = relationship(CourseModel)
    student = relationship(
        StudentModel,
        back_populates=StudentModel.enrolled_courses  # type: ignore
    )
    lectios_in_progress = relationship(
        "StudentLectioProgress",
        back_populates="course"
    )
    __table_args__ = PrimaryKeyConstraint("student_id", "course_id")


class StudentLectioProgressModel(Base):
    __tablename__ = "students_lectios_progress"
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.id))  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    progress = Column(Enum(LectioStatus))  # type: ignore
    student = relationship(
        StudentModel,
        back_populates=StudentModel.lectios_in_progress  # type: ignore
    )
    lectio = relationship(LectioModel)  # type: ignore
    course = relationship(
        StudentEnrolledCourseModel,
        back_populates=StudentEnrolledCourseModel.lectios_in_progress  # type: ignore
    )
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "lectio_id"),
        ForeignKeyConstraint(
            ["student_id", "course_id"],
            [StudentEnrolledCourseModel.student_id, StudentEnrolledCourseModel.course_id]
        )
    )


class StudentLastVisitedLectioModel(Base):
    __tablename__ = "students_last_visited_lectios"
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.id), primary_key=True)  # type: ignore
    lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    student = relationship(StudentModel)
    __table_args__ = (
        ForeignKeyConstraint(
            ["student", "lectio_id"],
            [StudentLectioProgressModel.student_id, StudentLectioProgressModel.lectio_id]
        ),
        CheckConstraint(
            select(StudentLectioProgressModel)
            .where(
                StudentLectioProgressModel.student_id == student_id and
                StudentLectioProgressModel.lectio_id == lectio_id and
                (
                    StudentLectioProgressModel.progress == LectioStatus.STARTED or
                    StudentLectioProgressModel.progress == LectioStatus.FINISHED
                )
            )
            .exists()
        )
    )


class StudentDataMapper(DataMapper):

    def persistence_model_to_entity(self, instance: StudentModel) -> Student:
        courses_in_progress, courses_lectios = reduce(
            lambda course: (
                enrolled_course_model_to_entity(course),
                reduce(merge_dict, [(GenericUUID(lectio.id), lectio_model_to_entity(lectio)) for lectio in course.lectios], {})
            ),
            instance.enrolled_courses
        )
        student = Student(
            id=GenericUUID(instance.id),
            name=Name(instance.name),
            surnames=Surnames(instance.firstname, instance.secondname),
            faculty=Faculty(faculty_model_to_entity(instance.faculty)),
            degree=GenericUUID(instance.degree_id),
            courses_in_progress=courses_in_progress,
            courses_lectios=courses_lectios,
            last_visited_lectio=(
                courses_lectios[GenericUUID(instance.last_visited_lectio.lectio_id)]
                if instance.last_visited_lectio.lectio_id
                else None
            )
        )

        return student

    def entity_to_persistence_model(self, entity: Student) -> StudentModel:
        pass


class SqlAlchemyStudentRepository(StudentRepository, SqlAlchemyGenericRepository):
    mapper_class = StudentDataMapper
    model_class = StudentModel
