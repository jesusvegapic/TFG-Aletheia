import email
import threading
from asyncio import Queue
from smtplib import SMTPException, SMTPConnectError, SMTPServerDisconnected
from typing import Optional

import tenacity.asyncio
from aiosmtplib import SMTP
from circuitbreaker import circuit, CircuitBreakerError  # type: ignore
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.framework_ddd.mailing.domain.email_sender import EmailSender
from src.framework_ddd.mailing.domain.entities import EmailMessage


class AioSmtpEmailSender(EmailSender):
    def __init__(
            self,
            server: str,
            port: int,
            user: Optional[str] = None,
            password: Optional[str] = None,
            tls=False,
            max_connections=5
    ):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.tls = tls
        self.max_connections = max_connections
        self.pool: Queue[SMTP] = Queue(max_connections)
        self.lock = threading.Lock()

    async def create_pool(self):
        for _ in range(self.max_connections):
            await self.pool.put(await self.create_connection())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type((SMTPConnectError, SMTPServerDisconnected, CircuitBreakerError)),
        reraise=True
    )
    @circuit(
        failure_threshold=3,
        expected_exception=(SMTPConnectError, SMTPServerDisconnected),
        recovery_timeout=10
    )
    async def create_connection(self):
        conn = SMTP(hostname=self.server, port=self.port)
        await conn.connect()
        if self.tls:
            await conn.starttls()
        if self.user and self.password:
            await conn.login(self.user, self.password)
        return conn

    async def get_connection(self):
        conn = await self.pool.get()
        return conn

    async def release_connection(self, conn):
        with self.lock:
            await self.pool.put(conn)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception_type((SMTPConnectError, SMTPServerDisconnected, CircuitBreakerError)),
        reraise=True
    )
    @circuit(
        failure_threshold=3,
        expected_exception=(SMTPConnectError, SMTPServerDisconnected),
        recovery_timeout=10
    )
    async def send(self, email_message: EmailMessage):
        message = email.message.EmailMessage()
        message.set_content(email_message.body)
        message['Subject'] = email_message.subject
        message['From'] = email_message.from_
        message['To'] = ",".join(email_message.to)

        connection = await self.get_connection()
        try:
            await connection.send_message(message)
        except SMTPConnectError:
            connection = await self.create_connection()
            await connection.send_message(message)
        finally:
            await self.release_connection(connection)
