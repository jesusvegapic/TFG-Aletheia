import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from lato import Application

from apps.admin.api.routers import courses
from apps.admin.api.config.api_config import ApiConfig
from apps.admin.container import ApplicationContainer
from src.framework_ddd.core.domain.errors import DomainError, EntityNotFoundError
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory, logger
from src.framework_ddd.core.infrastructure.database import Base

# dependency injection container


LoggerFactory.configure(logger_name="api")
config = ApiConfig()
container = ApplicationContainer(config=config)
api = FastAPI(debug=config.DEBUG)  # type: ignore
api.include_router(courses.router)
api.container = container  # type: ignore


@api.exception_handler(DomainError)
async def unicorn_exception_handler(request: Request, exc: DomainError):
    if container.config.DEBUG:
        raise exc

    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc} did something. There goes a rainbow..."},
    )


@api.exception_handler(EntityNotFoundError)  # type: ignore
async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Entity {exc.kwargs} not found in {exc.repository.__class__.__name__}"
        },
    )


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
