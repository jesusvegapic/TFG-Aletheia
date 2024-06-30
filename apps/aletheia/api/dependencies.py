from typing import Coroutine, Any
from lato import Application
from fastapi import Request, UploadFile

from src.framework_ddd.core.domain.files import BinaryIOProtocol


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


class UploadFileWrapper(BinaryIOProtocol):
    def __init__(self, upload_file: UploadFile):
        self._upload_file = upload_file

    async def read(self, size: int = -1) -> Coroutine[Any, Any, bytes]:
        return self._upload_file.read(size)
