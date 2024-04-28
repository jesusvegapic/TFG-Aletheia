import uuid
from dataclasses import dataclass
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject  # noqa
from lato import Application, TransactionContext, as_type
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket, AsyncIOMotorClientSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from src.admin.courses.application import courses_module
from src.admin.courses.domain.repository import CourseRepository
from src.admin.courses.infrastructure.repository import SqlCourseRepository
from src.shared.infrastructure.custom_loggin import logger
from src.videos.application import videos_module
from src.videos.domain.repository import VideoRepository
from src.videos.infrastructure.repository import AsyncMotorGridFsVideoRepository


@dataclass
class Config:
    APP_NAME: str
    DEBUG: bool
    DATABASE_ECHO: bool
    DATABASE_URL: str
    BUCKET_URL: str
    LOGGER_NAME: str


def create_db_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        config.DATABASE_URL, echo=config.DATABASE_ECHO
    )
    from src.shared.infrastructure.persistence.sql_alchemy.database import Base

    # TODO: it seems like a hack, but it works...
    Base.metadata.bind = engine
    return engine


def create_mongodb_client(config: Config) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(config.BUCKET_URL)


def create_gridfs_client(mongodb_client: AsyncIOMotorClient):
    return AsyncIOMotorGridFSBucket(mongodb_client.admin)


def create_application(
        db_engine: AsyncEngine,
        bucket_session_factory: AsyncIOMotorClient,
        bucket: AsyncIOMotorGridFSBucket
):
    application = Application(
        "Aletheia",
        version=0.1,
        db_engine=db_engine,
        bucket_session_factory=bucket_session_factory,
        bucket=bucket
    )

    application.include_submodule(courses_module)
    application.include_submodule(videos_module)

    @application.on_enter_transaction_context
    async def on_enter_transaction_context(ctx: TransactionContext):
        engine = application.get_dependency("db_engine")
        db_session = AsyncSession(engine)
        bucket_session_factory: AsyncIOMotorClient = application.get_dependency("bucket_session_factory")
        bucket_session = await bucket_session_factory.start_session()
        bucket = application.get_dependency("bucket")
        transaction_id = uuid.uuid4()
        logger.correlation_id = transaction_id  # type: ignore
        ctx.set_dependencies(
            logger=logger,
            transaction_id=transaction_id,
            publish_async=ctx.publish_async,
            db_session=db_session,
            bucket_session=bucket_session,
            course_repository=as_type(SqlCourseRepository(db_session), CourseRepository),
            video_repository=as_type(AsyncMotorGridFsVideoRepository(bucket, bucket_session), VideoRepository)
        )
        logger.debug("<<< Begin transaction")

    @application.on_exit_transaction_context
    async def on_exit_transaction_context(ctx: TransactionContext, exception=None):
        db_session: AsyncSession = ctx["db_session"]
        bucket_session: AsyncIOMotorClientSession = ctx["bucket_session"]
        if exception:
            await db_session.rollback()
            logger.warning(f"rollback due to {exception}")
        else:
            await db_session.commit()
            logger.debug(f"commited")
        await bucket_session.end_session()
        await db_session.close()
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
    mongodb_client = providers.Singleton(create_mongodb_client, config)
    gridfs_client = providers.Singleton(create_gridfs_client, mongodb_client)
    application = providers.Singleton(create_application, db_engine, mongodb_client, gridfs_client)
