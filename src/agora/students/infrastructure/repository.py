from functools import reduce
from sqlalchemy import Column, ForeignKey, Enum, PrimaryKeyConstraint, CheckConstraint, select, \
    ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.agora.students.domain.value_objects import LectioStatus
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.agora.students.domain.entities import Student, Faculty, StudentCourse
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.iam.infrastructure.repository import UserModel
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.shared.utils.structures import merge_dict


class StudentModel(Base):
    __tablename__ = "students"
    user_id = Column(UUIDType(binary=False), ForeignKey=UserModel.id, primary_key=True)  # type: ignore
    faculty_id = Column(UUIDType(binary=False), ForeignKey(FacultyModel.id), nullable=False)  # type: ignore
    degree_id = Column(UUIDType(binary=False), ForeignKey(DegreeModel.id), nullable=False)  # type: ignore
    faculty = relationship(FacultyModel)
    degree = relationship(DegreeModel)
    student_courses = relationship(
        "StudentCourseModel",
        back_populates="student"
    )
    last_visited_lectio = relationship("StudentLectioModel")


class StudentCourseModel(Base):
    __tablename__ = "students_courses"
    id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.id))  # type: ignore
    course = relationship(CourseModel)
    student = relationship(
        StudentModel,
        back_populates=StudentModel.enrolled_courses  # type: ignore
    )
    lectios_in_progress = relationship(
        "StudentLectio",
        back_populates="course"
    )
    __table_args__ = PrimaryKeyConstraint("student_id", "course_id")


class StudentLectioModel(Base):
    __tablename__ = "students_lectios"  # type: ignore
    student_course_id = Column(UUIDType(binary=False), ForeignKey(StudentCourseModel.id))  # type: ignore
    lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    progress = Column(Enum(LectioStatus))  # type: ignore
    student = relationship(
        StudentModel,
        back_populates=StudentModel.lectios_in_progress  # type: ignore
    )
    lectio = relationship(LectioModel)  # type: ignore
    __table_args__ = (
        PrimaryKeyConstraint( "student_course_id", "lectio_id"),

    )


class StudentLastVisitedLectioModel(Base):
    __tablename__ = "students_last_visited_lectios"
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.id), primary_key=True)  # type: ignore
    lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    student = relationship(StudentModel)
    lectio =
    __table_args__ = (
        ForeignKeyConstraint(
            ["student", "lectio_id"],
            [StudentLectioModel.student_id, StudentLectioModel.lectio_id]
        )
    )


class StudentDataMapper(DataMapper):

    def persistence_model_to_entity(self, instance: StudentModel) -> Student:

        def enrolled_course_model_to_entity(instance: StudentCourseModel) -> StudentCourse:

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
