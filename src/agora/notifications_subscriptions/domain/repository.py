from abc import ABC
from src.agora.notifications_subscriptions.domain.entities import NotificationsSubscription
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class NotificationsSubscriptionRepository(GenericRepository[GenericUUID, NotificationsSubscription], ABC):
    ...
