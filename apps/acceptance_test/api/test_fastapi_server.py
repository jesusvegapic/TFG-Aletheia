import os
from unittest import IsolatedAsyncioTestCase
from aiosmtpd.controller import Controller
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from apps.container import Config, ApplicationContainer
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.infrastructure.user_model import UserModel
from src.framework_ddd.mailing.domain.value_objects import Email
from src.framework_ddd.mailing.infrastructure.email_sender import EmailServerURL
from test.framework_ddd.mailing.integration_test.test_email_sender_should import TestEmailHandler


class TestFastapiServer(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = Config(
            APP_NAME="api_test",
            DATABASE_URL="sqlite+aiosqlite:///:memory:",
            BUCKET_URL=os.getenv("TEST_MONGO_URI"),
            EMAIL_SERVER_URL=EmailServerURL(host="localhost", port=1025),
            SYSTEM_EMAIL=Email("aletheia@aleheia.com"),
            DATABASE_ECHO=True,
            DEBUG=True,
            LOGGER_NAME="aletheia acceptance_test",
            SECRET_KEY="asbcfd"
        )
        LoggerFactory.configure(logger_name="api_test")
        container = ApplicationContainer(config=config)
        api = FastAPI(debug=config.DEBUG)
        api.container = container
        self.api = api
        self.admin_email = "admin@aletheia.com"
        self.admin_password = "admin"
        self.admin_id = GenericUUID.next_id().hex
        async with container.db_engine().connect() as bd:
            await bd.run_sync(Base.metadata.create_all)
            session = AsyncSession(container.db_engine())
            session.add(
                UserModel(
                    id=self.admin_id,
                    email=self.admin_email,
                    password=IamService.hash_password(self.admin_password),
                    is_superuser=True
                )
            )
            await session.commit()
            await session.close()

        self.email_handler = TestEmailHandler()
        self.email_controller = Controller(self.email_handler, "localhost", 1025)
        self.email_controller.start()

    def tearDown(self):
        self.email_controller.stop()
