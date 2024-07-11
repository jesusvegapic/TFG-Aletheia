from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from src.agora.shared.infrastructure.models import DegreeModel
from src.akademos.teachers.domain.entities import Teacher, TeacherFaculty
from src.akademos.teachers.domain.repository import TeacherRepository
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.infrastructure.sql_alchemy.models import TeacherModel, TeacherDegreesModel


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
