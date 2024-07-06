from typing import BinaryIO
from lato import Application
from fastapi import Request, UploadFile
from src.framework_ddd.core.domain.files import BinaryIOProtocol, AsyncBinaryIOProtocol


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


class BinaryIOWrapper(BinaryIOProtocol):
    def __init__(self, binary_io: BinaryIO):
        self._binary_io = binary_io

    def read(self, size: int = -1) -> bytes:
        return self._binary_io.read(size)


class UploadFileWrapper(AsyncBinaryIOProtocol):
    def __init__(self, upload_file: UploadFile):
        self._upload_file = upload_file

    async def read(self, size: int = -1) -> bytes:
        return await self._upload_file.read(size)

    def sync_mode(self) -> BinaryIOProtocol:
        return BinaryIOWrapper(self._upload_file.file)
