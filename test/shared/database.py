import asyncio
from unittest import IsolatedAsyncioTestCase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.framework_ddd.core.infrastructure.database import Base


class TestInMemorySqlDatabase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
        self.session_factory = async_sessionmaker(
            bind=engine
        )
        self.engine = engine

        async with engine.connect() as db:
            await db.run_sync(Base.metadata.create_all)
        self.session = self.session_factory()

    async def asyncTearDown(self):
        await self.session.close()
