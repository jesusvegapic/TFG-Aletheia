from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.akademos.teachers.domain.entities import Teacher, TeacherFaculty
from src.akademos.teachers.domain.repository import TeacherRepository
from src.akademos.teachers.domain.value_objects import TeacherPosition
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel


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


class TeacherDegreesModel(Base):
    __tablename__ = "teacher_degrees"
    id = Column(UUIDType(binary=False), ForeignKey(DegreeModel.id))  # type: ignore
    teacher_id = Column(UUIDType(binary=False), ForeignKey(TeacherModel.personal_user_id))  # type: ignore
    teacher = relationship(TeacherModel, back_populates="degrees")
    __table_args__ = (PrimaryKeyConstraint(teacher_id, id), )


class TeacherDataMapper(DataMapper):

    def model_to_entity(self, instance: TeacherModel) -> Teacher:
        return Teacher(
            instance.personal_user_id.hex,
            instance.personal_user.user.email,
            instance.personal_user.user.password,
            instance.personal_user.name,
            instance.personal_user.firstname,
            instance.personal_user.second_name,
            TeacherFaculty(
                instance.faculty_id.hex,
                [degree.id for degree in instance.faculty.degrees]
            ),
            [degree.id.hex for degree in instance.degrees],
            instance.position  # type: ignore
        )

    def entity_to_model(self, teacher: Teacher) -> TeacherModel:
        return TeacherModel(
            personal_user_id=teacher.id,
            faculty_id=teacher.faculty.id,
            position=teacher.position,
            degrees=[
                TeacherDegreesModel(
                    id=degree,
                    teacher_id=teacher.id
                )
                for degree in teacher.degrees
            ],
            personal_user=PersonalUserModel(
                user_id=teacher.id,
                name=teacher.name,
                firstname=teacher.firstname,
                second_name=teacher.second_name,
                user=UserModel(
                    id=teacher.id,
                    email=teacher.email,
                    password=teacher.hashed_password,
                    is_superuser=True
                )
            )
        )


class SqlAlchemyTeacherRepository(TeacherRepository, SqlAlchemyGenericRepository):
    model_class = TeacherModel
    mapper_class = TeacherDataMapper
