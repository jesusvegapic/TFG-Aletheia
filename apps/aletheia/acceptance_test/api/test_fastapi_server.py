from unittest import IsolatedAsyncioTestCase
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from apps.aletheia.container import Config, ApplicationContainer
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory
from src.framework_ddd.core.infrastructure.database import Base
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.infrastructure.user_model import UserModel


class TestFastapiServer(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = Config(
            APP_NAME="api_test",
            DATABASE_URL="sqlite+aiosqlite:///:memory:",
            BUCKET_URL="mongodb://root:example@localhost:27017/",
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
        async with container.db_engine().connect() as bd:
            await bd.run_sync(Base.metadata.create_all)
            session = AsyncSession(container.db_engine())
            session.add(
                UserModel(
                    id=GenericUUID.next_id(),
                    email=self.admin_email,
                    password=IamService.hash_password(self.admin_password),
                    is_superuser=True
                )
            )
            await session.commit()
            await session.close()

