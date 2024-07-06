from typing import Coroutine, Any
from motor.motor_asyncio import AsyncIOMotorGridOut
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import force_auto_coercion  # type: ignore
from src.framework_ddd.core.domain.files import BinaryIOProtocol

force_auto_coercion()
Base = declarative_base()


class GridOutWrapper(BinaryIOProtocol):
    def __init__(self, grid_out: AsyncIOMotorGridOut):
        self._grid_out = grid_out

    async def read(self, size: int = -1) -> bytes:
        return await self._grid_out.read(size)
