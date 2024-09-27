from typing import BinaryIO, Annotated
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from lato import Application, TransactionContext
from fastapi import Request, UploadFile, HTTPException
from src.framework_ddd.core.domain.files import BinaryIOProtocol, AsyncBinaryIOProtocol
from src.framework_ddd.iam.application.services import IamService, IamUserInfo

bearer = HTTPBearer()


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


async def get_transaction_context(  # type: ignore
        app: Annotated[Application, Depends(get_application)],
) -> TransactionContext:
    """Creates a new transaction context for each request"""

    async with app.transaction_context() as ctx:
        yield ctx


async def get_authenticated_user_info(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> IamUserInfo:
    access_token = credentials.credentials
    iam_user_info = ctx[IamService].auth_by_token(access_token)
    if not iam_user_info:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return iam_user_info


async def get_authenticated_super_user_info(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
        ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
) -> IamUserInfo:
    access_token = credentials.credentials
    iam_user_info: IamUserInfo = ctx[IamService].auth_by_token(access_token)
    if not iam_user_info:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not iam_user_info.is_superuser:
        raise HTTPException(status_code=401, detail="Not authorized.")
    return iam_user_info


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
