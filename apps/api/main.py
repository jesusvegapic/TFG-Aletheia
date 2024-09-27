import time
from fastapi import FastAPI, Request
from lato import Application
from apps.api.routers import courses, faculties, students, teachers
from apps.api.config.api_config import ApiConfig
from apps.container import ApplicationContainer
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory, logger
from src.framework_ddd.core.infrastructure.database import Base

# dependency injection container


LoggerFactory.configure(logger_name="api")
config = ApiConfig()  # type: ignore
container = ApplicationContainer(config=config)
api = FastAPI(debug=config.DEBUG)  # type: ignore
api.include_router(courses.router)
api.include_router(students.router)
api.include_router(faculties.router)
api.include_router(teachers.router)
api.container = container  # type: ignore


@api.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    finally:
        pass


@api.get("/")
async def root():
    return {"info": "Online auctions API. See /docs for documentation"}


async def init_db():
    db_engine = container.db_engine()
    async with db_engine.connect() as db:
        logger.info(f"using db engine {db_engine}, creating tables")
        await db.run_sync(Base.metadata.create_all)
        await db.commit()
    logger.info("setup complete")


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application
