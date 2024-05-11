from lato import Application
from fastapi import Request


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application
