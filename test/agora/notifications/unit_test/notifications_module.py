from unittest import IsolatedAsyncioTestCase
from src.framework_ddd.mailing.domain.email_sender import EmailSender
from src.framework_ddd.mailing.domain.entities import EmailMessage


class TestEmailSender(EmailSender):
    async def send(self, entity: EmailMessage):
        pass


class TestNotificationsModule(IsolatedAsyncioTestCase):
    sender: EmailSender

    def setUp(self):
        self.sender = TestEmailSender()
