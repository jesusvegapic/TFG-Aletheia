import logging
import uuid
from dataclasses import dataclass

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject  # noqa
from lato import Application, TransactionContext, as_type
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import Session

from src.courses.application import courses_module
from src.courses.domain.repository import CourseRepository
from src.courses.infrastructure.repository import SqlCourseRepository
from src.shared.infrastructure.custom_loggin import logger


@dataclass
class Config:
    APP_NAME: str
    DEBUG: bool
    DATABASE_ECHO: bool
    DATABASE_URL: str
    LOGGER_NAME: str


def create_db_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        config.DATABASE_URL, echo=config.DATABASE_ECHO
    )
    from src.shared.infrastructure.database import Base

    # TODO: it seems like a hack, but it works...
    Base.metadata.bind = engine
    return engine


def create_application(db_engine: AsyncEngine):
    application = Application(
        "Aletheia",
        version=0.1,
        db_engine=db_engine,
    )

    application.include_submodule(courses_module)

    @application.on_enter_transaction_context
    async def on_enter_transaction_context(ctx: TransactionContext):
        engine = application.get_dependency("db_engine")
        session = AsyncSession(engine)
        transaction_id = uuid.uuid4()
        logger.correlation_id = transaction_id  # type: ignore
        ctx.set_dependencies(
            logger=logger,
            transaction_id=transaction_id,
            publish_async=ctx.publish_async,
            session=session,
            course_repository=as_type(SqlCourseRepository(session), CourseRepository)
        )
        logger.debug("<<< Begin transaction")

    @application.on_exit_transaction_context
    async def on_exit_transaction_context(ctx: TransactionContext, exception=None):
        def is_rollback(exception):
            return False

        session: AsyncSession = ctx["session"]
        if is_rollback(exception):
            await session.rollback()
            logger.warning(f"rollback due to {exception}")
        else:
            await session.commit()
            logger.debug(f"commited")
        await session.close()
        logger.debug(">>> End transaction")

    @application.transaction_middleware
    async def logging_middleware(ctx: TransactionContext, call_next):
        description = (
            f"{ctx.current_action[1]} -> {repr(ctx.current_action[0])}"
            if ctx.current_action
            else ""
        )
        logger.debug(f"Executing {description}...")
        result = await call_next()
        logger.debug(f"Finished executing {description}")
        return result

    return application


class ApplicationContainer(containers.DeclarativeContainer):
    """Dependency Injection container for the application (application-level config)
    see https://github.com/ets-labs/python-dependency-injector for more details
    """
    __self__ = providers.Self()
    config = providers.Dependency(instance_of=Config)
    db_engine = providers.Singleton(create_db_engine, config)
    application = providers.Singleton(create_application, db_engine)
