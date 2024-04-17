import uuid

from sqlalchemy import Column, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from src.courses.domain.entities import Course, Lectio
from src.courses.domain.repository import CourseRepository
from src.courses.domain.value_objects import CourseState, CourseName, CourseDescription, LectioName, LectioDescription
from src.shared.domain.value_objects import GenericUUID
from src.shared.infrastructure.data_mapper import DataMapper
from src.shared.infrastructure.database import Base
from src.shared.infrastructure.repositories import SqlAlchemyGenericRepository


class CoursePersistenceModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(CourseName.max_length()), nullable=False)
    description = Column(String(CourseDescription.max_length()), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    lectios = relationship("LectioPersistenceModel", back_populates="course")


class LectioPersistenceModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CoursePersistenceModel.id))  # type: ignore
    name = Column(String(CourseName.max_length()), nullable=False)
    description = Column(String(CourseDescription.max_length()), nullable=False)
    course = relationship(CoursePersistenceModel, back_populates="lectios")


def deserialize_id(value: str) -> GenericUUID:
    if isinstance(value, uuid.UUID):
        return GenericUUID(value.hex)
    return GenericUUID(value)


class CourseDataMapper(DataMapper):

    def persistence_model_to_entity(self, instance: CoursePersistenceModel) -> Course:
        def lectio_persistence_model_to_entity(lectio_instance: LectioPersistenceModel) -> Lectio:
            return Lectio(
                id=deserialize_id(lectio_instance.id),  # type: ignore
                name=LectioName(lectio_instance.name),  # type: ignore
                description=LectioDescription(lectio_instance.description)  # type: ignore
            )

        return Course(
            id=deserialize_id(instance.id),  # type: ignore
            owner=deserialize_id(instance.owner),  # type: ignore
            name=CourseName(instance.name),  # type: ignore
            description=CourseDescription(instance.description),  # type: ignore
            state=CourseState(instance.state),  # type: ignore
            lectios=[lectio_persistence_model_to_entity(lectio_instance) for lectio_instance in instance.lectios]
        )

    def entity_to_persistence_model(self, course: Course) -> CoursePersistenceModel:
        def lectio_entity_to_persistence_model(lectio: Lectio):
            return LectioPersistenceModel(
                id=lectio.id,
                course_id=course.id,
                name=lectio.name,
                description=lectio.description
            )

        return CoursePersistenceModel(
            id=course.id,
            owner=course.owner,
            name=course.name,
            description=course.description,
            state=course.state,
            lectios=[lectio_entity_to_persistence_model(lectio) for lectio in course.lectios]
        )


class SqlCourseRepository(SqlAlchemyGenericRepository, CourseRepository):
    mapper_class = CourseDataMapper
    persistence_model_class = CoursePersistenceModel
