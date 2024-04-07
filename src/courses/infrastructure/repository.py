import uuid

from sqlalchemy import Column, Enum, String
from sqlalchemy_utils import UUIDType  # type: ignore

from src.courses.domain.entities import Course
from src.courses.domain.repository import CourseRepository
from src.courses.domain.value_objects import CourseState, CourseName, CourseDescription
from src.shared.domain.value_objects import GenericUUID
from src.shared.infrastructure.data_mapper import DataMapper
from src.shared.infrastructure.database import Base
from src.shared.infrastructure.repository import SqlAlchemyGenericRepository


class CoursePersistenceModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(CourseName.max_length()), nullable=False)
    description = Column(String(CourseDescription.max_length()), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore


def deserialize_id(value: str) -> GenericUUID:
    if isinstance(value, uuid.UUID):
        return GenericUUID(value.hex)
    return GenericUUID(value)


class CourseDataMapper(DataMapper):

    def persistence_model_to_entity(self, instance: CoursePersistenceModel) -> Course:
        return Course(
            id=deserialize_id(instance.id),  # type: ignore
            owner=deserialize_id(instance.owner),  # type: ignore
            name=CourseName(instance.name),  # type: ignore
            description=CourseDescription(instance.description),  # type: ignore
            state=CourseState(instance.state)  # type: ignore
        )

    def entity_to_persistence_model(self, course: Course) -> CoursePersistenceModel:
        return CoursePersistenceModel(
            id=course.id,
            owner=course.owner,
            name=course.name,
            description=course.description,
            state=course.state
        )


class SqlCourseRepository(SqlAlchemyGenericRepository, CourseRepository):
    mapper_class = CourseDataMapper
    persistence_model_class = CoursePersistenceModel
