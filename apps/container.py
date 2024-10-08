import uuid
from dataclasses import dataclass
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject  # noqa
from lato import Application, TransactionContext, as_type, Query
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket, AsyncIOMotorClientSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from src.agora.conferences.application import agora_conferences_module
from src.agora.courses.application import agora_courses_module
from src.agora.notifications.application import notifications_module
from src.agora.notifications_subscriptions.application import notifications_subscriptions_module
from src.agora.notifications_subscriptions.domain.repository import NotificationsSubscriptionRepository
from src.agora.notifications_subscriptions.infrastructure.repository import \
    SqlAlchemyNotificationsSubscriptionRepository
from src.agora.students.application import students_module
from src.agora.students.domain.repository import StudentRepository
from src.agora.students.infrastructure.repository import SqlAlchemyStudentRepository
from src.agora.teachers.application import agora_teachers_module
from src.agora.videos.application import agora_videos_module
from src.akademos.conferences.application import akademos_conferences_module
from src.akademos.conferences.domain.repository import ConferenceRepository
from src.akademos.conferences.infrastructure.repository import SqlAlchemyConferenceRepository
from src.akademos.courses.application import akademos_courses_module
from src.akademos.courses.domain.repository import CourseRepository
from src.akademos.courses.infrastructure.repository import SqlCourseRepository
from src.akademos.faculties.application import faculties_module
from src.akademos.faculties.domain.repository import FacultyRepository
from src.akademos.faculties.infrastructure.repository import SqlAlchemyFacultyRepository
from src.akademos.teachers.application import teachers_module
from src.akademos.teachers.domain.repository import TeacherRepository
from src.akademos.teachers.infrastructure.repository import SqlAlchemyTeacherRepository
from src.akademos.videos.application import videos_module
from src.akademos.videos.domain.repository import VideoRepository
from src.akademos.videos.infrastructure.repository import AsyncMotorGridFsVideoRepository
from src.framework_ddd.core.infrastructure.custom_loggin import logger
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.infrastructure.repository import SqlAlchemyUserRepository
from src.framework_ddd.mailing.domain.email_sender import EmailSender
from src.framework_ddd.mailing.domain.value_objects import Email
from src.framework_ddd.mailing.infrastructure.email_sender import EmailServerURL, AioSmtpEmailSender


@dataclass
class Config:
    APP_NAME: str
    DEBUG: bool
    DATABASE_ECHO: bool
    DATABASE_URL: str
    EMAIL_SERVER_URL: EmailServerURL
    SYSTEM_EMAIL: Email
    BUCKET_URL: str
    LOGGER_NAME: str
    SECRET_KEY: str


def create_db_engine(config: Config) -> AsyncEngine:
    engine = create_async_engine(
        config.DATABASE_URL, echo=config.DATABASE_ECHO
    )
    from src.framework_ddd.core.infrastructure.database import Base


    Base.metadata.bind = engine
    return engine


def create_mongodb_client(config: Config) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(config.BUCKET_URL)


def create_gridfs_client(mongodb_client: AsyncIOMotorClient):
    return AsyncIOMotorGridFSBucket(mongodb_client.admin)


def create_application(
        db_engine: AsyncEngine,
        bucket_session_factory: AsyncIOMotorClient,
        bucket: AsyncIOMotorGridFSBucket,
        config: Config
):
    application = Application(
        "Aletheia",
        version=0.1,
        db_engine=db_engine,
        bucket_session_factory=bucket_session_factory,
        bucket=bucket,
        secret_key=config.SECRET_KEY
    )

    application.include_submodule(akademos_courses_module)
    application.include_submodule(videos_module)
    application.include_submodule(students_module)
    application.include_submodule(agora_courses_module)
    application.include_submodule(faculties_module)
    application.include_submodule(teachers_module)
    application.include_submodule(agora_teachers_module)
    application.include_submodule(agora_videos_module)
    application.include_submodule(notifications_subscriptions_module)
    application.include_submodule(notifications_module)
    application.include_submodule(akademos_conferences_module)
    application.include_submodule(agora_conferences_module)

    @application.on_enter_transaction_context
    async def on_enter_transaction_context(ctx: TransactionContext):
        async def publish_query(message: Query):
            result = await ctx.publish_async(message)
            result_list = list(result.values())
            return result_list[0] if len(result_list) > 0 else None

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
            publish=ctx.publish_async,
            publish_query=publish_query,
            db_session=db_session,
            email_sender=as_type(AioSmtpEmailSender(config.EMAIL_SERVER_URL), EmailSender),
            aletheia_platform_email=config.SYSTEM_EMAIL,
            bucket_session=bucket_session,
            course_repository=as_type(SqlCourseRepository(db_session), CourseRepository),
            video_repository=as_type(AsyncMotorGridFsVideoRepository(bucket, bucket_session), VideoRepository),
            student_repository=as_type(SqlAlchemyStudentRepository(db_session), StudentRepository),
            faculty_repository=as_type(SqlAlchemyFacultyRepository(db_session), FacultyRepository),
            teacher_repository=as_type(SqlAlchemyTeacherRepository(db_session), TeacherRepository),
            conference_repository=as_type(SqlAlchemyConferenceRepository(db_session), ConferenceRepository),
            notifications_subscriptions_repository=as_type(
                SqlAlchemyNotificationsSubscriptionRepository(db_session),
                NotificationsSubscriptionRepository
            ),
            iam_service=as_type(
                IamService(
                    SqlAlchemyUserRepository(db_session),
                    application.get_dependency("secret_key")
                ),
                IamService
            )
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
    application = providers.Singleton(
        create_application,
        db_engine,
        mongodb_client,
        gridfs_client,
        config
    )
