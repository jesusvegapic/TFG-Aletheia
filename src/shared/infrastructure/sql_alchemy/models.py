import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.akademos.teachers.domain.value_objects import TeacherPosition
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel
from src.shared.domain.value_objects import CourseState


class TeacherModel(Base):
    __tablename__ = "teachers"
    personal_user_id = Column(
        UUIDType(binary=False),
        ForeignKey(PersonalUserModel.user_id),
        primary_key=True
    )  # type: ignore
    faculty_id = Column(UUIDType(binary=False), ForeignKey(FacultyModel.id), nullable=False)  # type: ignore
    position = Column(Enum(TeacherPosition), nullable=False)  # type: ignore
    faculty = relationship(FacultyModel, backref=None, lazy="selectin")
    degrees = relationship('TeacherDegreesModel', back_populates="teacher", lazy="selectin")
    personal_user = relationship(PersonalUserModel, lazy="selectin")
    courses = relationship(
        'CourseModel',
        back_populates="teacher"
    )
    conferences = relationship(
        'ConferenceModel',
        back_populates="teacher"
    )


class TeacherDegreesModel(Base):
    __tablename__ = "teacher_degrees"
    id = Column(UUIDType(binary=False), ForeignKey(DegreeModel.id))
    teacher_id = Column(UUIDType(binary=False), ForeignKey(TeacherModel.personal_user_id))  # type: ignore
    teacher = relationship(TeacherModel, back_populates="degrees")
    __table_args__ = (PrimaryKeyConstraint(teacher_id, id), )



class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), ForeignKey(TeacherModel.personal_user_id), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    topics = Column(String(255), nullable=False)
    lectios = relationship(
        "LectioModel",
        back_populates="course",
        lazy="selectin"
    )
    teacher = relationship(
        TeacherModel,
        back_populates="courses",
        lazy="selectin"
    )


class LectioModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    video_id = Column(UUIDType(binary=False))  # type: ignore
    course = relationship(CourseModel, back_populates="lectios")


class ConferenceModel(Base):
    __tablename__ = "conferences"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    owner = Column(UUIDType(binary=False), ForeignKey(TeacherModel.personal_user_id), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    topics = Column(String(255), nullable=False)
    video_id = Column(UUIDType(binary=False))  # type: ignore
    teacher = relationship(
        TeacherModel,
        back_populates="conferences",
        lazy="selectin"
    )
