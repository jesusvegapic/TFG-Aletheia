from typing import Optional
from unittest import IsolatedAsyncioTestCase

from src.agora.notifications_subscriptions.domain.entities import NotificationsSubscription
from src.agora.notifications_subscriptions.domain.repository import NotificationsSubscriptionRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class TestNotificationsSubscriptionRepository(NotificationsSubscriptionRepository):
    async def add(self, entity: NotificationsSubscription):
        pass

    async def get(self, id: GenericUUID) -> Optional[NotificationsSubscription]:
        pass

    async def remove(self, entity: NotificationsSubscription):
        pass

    async def remove_by_id(self, id: GenericUUID):
        pass


class TestNotificationsSubscriptionsModule(IsolatedAsyncioTestCase):
    repository: NotificationsSubscriptionRepository

    def setUp(self):
        self.repository = TestNotificationsSubscriptionRepository()

