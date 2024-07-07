from re import split
from sqlalchemy_utils import UUIDType  # type: ignore
from src.akademos.courses.domain.entities import Course, Lectio
from src.akademos.courses.domain.repository import CourseRepository
from src.akademos.courses.domain.value_objects import Topic
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel


class CourseDataMapper(DataMapper):

    def model_to_entity(self, instance: CourseModel) -> Course:
        def lectio_model_to_entity(lectio_instance: LectioModel) -> Lectio:
            return Lectio(
                id=lectio_instance.id.hex,
                name=lectio_instance.name,  # type: ignore
                description=lectio_instance.description,  # type: ignore
                video_id=lectio_instance.video_id.hex
            )

        return Course(
            id=instance.id.hex,  # type: ignore
            owner=instance.owner.hex,  # type: ignore
            name=instance.name,  # type: ignore
            description=instance.description,  # type: ignore
            state=instance.state,  # type: ignore
            topics=[Topic(topic) for topic in split(";", instance.topics)],  # type: ignore
            lectios=[lectio_model_to_entity(lectio_instance) for lectio_instance in instance.lectios]
        )

    def entity_to_model(self, course: Course) -> CourseModel:
        def lectio_entity_to_model(lectio: Lectio):
            return LectioModel(
                id=lectio.id,
                course_id=course.id,
                name=lectio.name,
                description=lectio.description,
                video_id=lectio.video_id
            )

        return CourseModel(
            id=course.id,
            owner=course.owner,
            name=course.name,
            description=course.description,
            state=course.state,
            topics=";".join(course.topics),
            lectios=[lectio_entity_to_model(lectio) for lectio in course.lectios]
        )


class SqlCourseRepository(SqlAlchemyGenericRepository, CourseRepository):
    mapper_class = CourseDataMapper
    model_class = CourseModel
