import asyncio
from queue import Queue
from typing import List, Tuple, Any
from unittest import IsolatedAsyncioTestCase
import aiosmtpd.handlers
from aiosmtpd.controller import Controller
from src.framework_ddd.mailing.domain.entities import EmailMessage
from src.framework_ddd.mailing.infrastructure.email_sender import AioSmtpEmailSender


class TestEmailHandler(aiosmtpd.handlers.Message):
    messages: List[Tuple[str, str, List[str], Any]]

    def __init__(self):
        super().__init__()
        self.messages = []

    def handle_message(self, message):
        self.messages.append((message["Subject"], message["From"], message["To"], message.get_payload()))


class EmailSenderShould(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.handler = TestEmailHandler()
        self.controller = Controller(self.handler, hostname='localhost', port=1025)
        self.controller.start()
        self.sender = AioSmtpEmailSender('localhost', 1025)
        await self.sender.create_pool()

    async def asyncTearDown(self):
        self.controller.stop()

    async def test_send_valid_email(self):
        message = EmailMessage(
            id=EmailMessage.next_id().hex,
            to=["aragorn@gmail.com", "gandalf@gmail.com"],
            from_="aletheia@gmail.com",
            subject="email de prueba",
            body="body de prueba"
        )

        await self.sender.send(message)

        subject, from_, to, data = self.handler.messages[0]

        self.assertEqual(subject, message.subject)
        self.assertEqual(from_, message.from_)
        self.assertEqual(to, ",".join(message.to))
        self.assertEqual(data, message.body+"\r\n")
