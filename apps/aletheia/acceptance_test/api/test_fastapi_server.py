from unittest import IsolatedAsyncioTestCase
from fastapi import FastAPI
from apps.aletheia.container import Config, ApplicationContainer
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory
from src.framework_ddd.core.infrastructure.database import Base


class TestFastapiServer(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = Config(
            APP_NAME="api_test",
            DATABASE_URL="sqlite+aiosqlite:///:memory:",
            BUCKET_URL="mongodb://root:example@localhost:27017/",
            DATABASE_ECHO=True,
            DEBUG=True,
            LOGGER_NAME="aletheia acceptance_test"
        )
        LoggerFactory.configure(logger_name="api_test")
        container = ApplicationContainer(config=config)
        api = FastAPI(debug=config.DEBUG)
        api.container = container
        self.api = api
        async with container.db_engine().connect() as bd:
            await bd.run_sync(Base.metadata.create_all)
