from enum import StrEnum
from re import split

from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy_utils import UUIDType  # type: ignore
from src.agora.notifications_subscriptions.domain.entities import NotificationsSubscription, TeacherCoursesSubscription
from src.agora.notifications_subscriptions.domain.repository import NotificationsSubscriptionRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.core.infrastructure.datamapper import DataMapper, MapperEntity, MapperModel
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.framework_ddd.iam.infrastructure.user_model import UserModel
from src.shared.infrastructure.sql_alchemy.models import TeacherModel  # type: ignore


class NotificationsSubscriptionType(StrEnum):
    TEACHER_COURSES = "TEACHER_COURSES"


class NotificationsSubscriptionModel(Base):
    __tablename__ = "notifications_subscriptions"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    subscriber_id = Column(UUIDType(binary=False), ForeignKey(UserModel.id), nullable=False)  # type: ignore
    teacher_id = Column(UUIDType(binary=False), ForeignKey(TeacherModel.personal_user_id))  # type: ignore
    type = Column(Enum(NotificationsSubscriptionType), nullable=False)  # type: ignore
    topics = Column(String(255))


class NotificationsSubscriptionDataMapper(DataMapper):

    def model_to_entity(self, instance: NotificationsSubscriptionModel) -> NotificationsSubscription:  # type: ignore
        if instance.type == NotificationsSubscriptionType.TEACHER_COURSES:
            return TeacherCoursesSubscription(
                id=instance.id.hex,
                subscriber_id=instance.subscriber_id.hex,  # type: ignore
                teacher_id=instance.teacher_id.hex,  # type: ignore
                topics=split(";", instance.topics)  # type: ignore
            )

    def entity_to_model(self, entity: NotificationsSubscription) -> NotificationsSubscriptionModel:  # type: ignore
        if isinstance(entity, TeacherCoursesSubscription):
            return NotificationsSubscriptionModel(
                id=GenericUUID(entity.id),
                subscriber_id=GenericUUID(entity.subscriber_id),
                teacher_id=GenericUUID(entity.teacher_id),
                type=NotificationsSubscriptionType.TEACHER_COURSES,
                topics=";".join(entity.topics)
            )


class SqlAlchemyNotificationsSubscriptionRepository(SqlAlchemyGenericRepository, NotificationsSubscriptionRepository):
    model_class = NotificationsSubscriptionModel
    mapper_class = NotificationsSubscriptionDataMapper
