from sqlalchemy import Column, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.agora.students.domain.value_objects import LectioStatus
from src.agora.students.domain.entities import Student, StudentCourse, StudentFaculty, StudentLectio
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository


class StudentModel(Base):
    __tablename__ = "students"
    personal_user_id = Column(UUIDType(binary=False), ForeignKey(PersonalUserModel.user_id), primary_key=True)  # type: ignore
    faculty_id = Column(UUIDType(binary=False), ForeignKey(FacultyModel.id), nullable=False)  # type: ignore
    degree_id = Column(UUIDType(binary=False), ForeignKey(DegreeModel.id), nullable=False)  # type: ignore
    faculty = relationship(FacultyModel, backref=None, lazy="selectin")
    degree = relationship(DegreeModel, backref=None, lazy="selectin")
    personal_user = relationship(PersonalUserModel, lazy="selectin")
    student_courses = relationship(
        "StudentCourseModel",
        back_populates="student",
        lazy="selectin"
    )


class StudentCourseModel(Base):
    __tablename__ = "students_courses"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    student_id = Column(UUIDType(binary=False), ForeignKey(StudentModel.personal_user_id))  # type: ignore
    last_visited_lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    course = relationship(CourseModel, lazy="selectin")
    student = relationship(
        StudentModel,
        back_populates="student_courses",  # type: ignore
        lazy="selectin"
    )
    lectios_in_progress = relationship(
        'StudentLectioModel',
        lazy="selectin",
        back_populates="student_course"
    )
    last_visited_lectio = relationship(LectioModel)  # type: ignore
    __table_args__ = (PrimaryKeyConstraint("student_id", "id"),)


class StudentLectioModel(Base):
    __tablename__ = "students_lectios"  # type: ignore
    student_course_id = Column(UUIDType(binary=False), ForeignKey(StudentCourseModel.id))  # type: ignore
    lectio_id = Column(UUIDType(binary=False), ForeignKey(LectioModel.id))  # type: ignore
    progress = Column(Enum(LectioStatus))  # type: ignore
    student_course = relationship(StudentCourseModel, back_populates="lectios_in_progress", lazy="selectin")
    lectio = relationship(LectioModel, lazy="selectin")  # type: ignore
    __table_args__ = (
        PrimaryKeyConstraint("student_course_id", "lectio_id"),
    )


class StudentDataMapper(DataMapper):

    def model_to_entity(self, instance: StudentModel) -> Student:
        return Student(
            id=instance.personal_user.user.id.hex,
            name=instance.personal_user.name,
            firstname=instance.personal_user.firstname,
            second_name=instance.personal_user.second_name,
            email=instance.personal_user.user.email,
            password_hash=instance.personal_user.user.password,
            faculty=StudentFaculty(instance.faculty.id.hex, [degree.id for degree in instance.faculty.degrees]),
            degree=instance.degree.id.hex,
            courses_in_progress=[
                StudentCourse(
                    course.id.hex,
                    course.course_id.hex,
                    [
                        StudentLectio(lectio.lectio_id.hex, lectio.progress)
                        for lectio in course.lectios_in_progress
                    ],
                    course.last_visited_lectio_id.hex if course.last_visited_lectio_id else None
                )
                for course in instance.student_courses
            ],

        )

    def entity_to_model(self, student: Student) -> StudentModel:
        return StudentModel(
            personal_user_id=GenericUUID(student.id),
            faculty_id=GenericUUID(student.faculty.id),
            degree_id=GenericUUID(student.degree),
            student_courses=[
                StudentCourseModel(
                    id=GenericUUID(course.id),
                    course_id=GenericUUID(course.course_id),
                    student_id=GenericUUID(student.id),
                    lectios_in_progress=[
                        StudentLectioModel(
                            student_course_id=GenericUUID(course.id),
                            lectio_id=GenericUUID(lectio.id),
                            progress=lectio.status
                        )
                        for lectio in course.lectios
                    ],
                    last_visited_lectio_id=course.last_visited_lectio,
                )
                for course in student.courses_in_progress
            ],
            personal_user=PersonalUserModel(
                user_id=GenericUUID(student.id),
                name=student.name,
                firstname=student.firstname,
                second_name=student.second_name,
                user=UserModel(
                    id=GenericUUID(student.id),
                    email=student.email,
                    password=student.hashed_password,
                    is_superuser=student.is_superuser
                )
            )
        )


class SqlAlchemyStudentRepository(StudentRepository, SqlAlchemyGenericRepository):
    mapper_class = StudentDataMapper
    model_class = StudentModel
