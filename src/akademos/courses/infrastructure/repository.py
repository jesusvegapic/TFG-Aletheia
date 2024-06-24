import uuid
from sqlalchemy_utils import UUIDType  # type: ignore

from src.akademos.courses.domain.entities import Course, Lectio
from src.akademos.courses.domain.repository import CourseRepository
from src.akademos.courses.domain.value_objects import Topic
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel, TopicModel


def deserialize_id(value: str) -> GenericUUID:
    if isinstance(value, uuid.UUID):
        return GenericUUID(value.hex)
    return GenericUUID(value)


class CourseDataMapper(DataMapper):

    def model_to_entity(self, instance: CourseModel) -> Course:
        def lectio_model_to_entity(lectio_instance: LectioModel) -> Lectio:
            return Lectio(
                id=deserialize_id(lectio_instance.id),  # type: ignore
                name=LectioName(lectio_instance.name),  # type: ignore
                description=LectioDescription(lectio_instance.description)  # type: ignore
            )

        return Course(
            id=deserialize_id(instance.id),  # type: ignore
            owner=deserialize_id(instance.owner),  # type: ignore
            name=instance.name,  # type: ignore
            description=instance.description,  # type: ignore
            state=instance.state,  # type: ignore
            topics=[Topic(topic.name) for topic in instance.topics],
            lectios=[lectio_model_to_entity(lectio_instance) for lectio_instance in instance.lectios]
        )

    def entity_to_model(self, course: Course) -> CourseModel:
        def lectio_entity_to_model(lectio: Lectio):
            return LectioModel(
                id=lectio.id,
                course_id=course.id,
                name=lectio.name,
                description=lectio.description
            )

        return CourseModel(
            id=course.id,
            owner=course.owner,
            name=course.name,
            description=course.description,
            state=course.state,
            topics=[TopicModel(name=topic, course_id=course.id) for topic in course.topics],
            lectios=[lectio_entity_to_model(lectio) for lectio in course.lectios]
        )


class SqlCourseRepository(SqlAlchemyGenericRepository, CourseRepository):
    mapper_class = CourseDataMapper
    model_class = CourseModel
