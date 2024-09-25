from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import TransactionContext
from apps.aletheia.api.dependencies import get_transaction_context
from apps.aletheia.api.models.iam import LoginRequest
from src.framework_ddd.iam.application.services import IamService

router = APIRouter()


@router.post(
    "/auth/accesstoken"
)
@inject
async def login(
        request_body: LoginRequest,
        ctx: Annotated[TransactionContext, Depends(get_transaction_context)]
):
    iam_service: IamService = ctx[IamService]
    response = await iam_service.authenticate_with_email_and_password(request_body.email, request_body.password)
    return response
