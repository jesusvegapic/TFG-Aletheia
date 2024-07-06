import asyncio
import concurrent.futures
from motor.motor_asyncio import AsyncIOMotorGridOut
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import force_auto_coercion  # type: ignore
from src.framework_ddd.core.domain.files import BinaryIOProtocol, AsyncBinaryIOProtocol

force_auto_coercion()
Base = declarative_base()


class GridOutWrapper(BinaryIOProtocol):
    def __init__(self, grid_out: AsyncIOMotorGridOut):
        self._grid_out = grid_out

    def read(self, size: int = -1) -> bytes:  # type: ignore
        loop = asyncio.get_event_loop()
        if loop.is_running():
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = loop.run_in_executor(pool, lambda:
                    asyncio.run(self._grid_out.read(size))  # type: ignore
                                              )
                result = future.result()  # type: ignore
                return result
        else:
            result = asyncio.run(self._grid_out.read(size))
            return result


class AsyncGridOutWrapper(AsyncBinaryIOProtocol):
    def __init__(self, grid_out: AsyncIOMotorGridOut):
        self._grid_out = grid_out

    async def read(self, size: int = -1) -> bytes:
        return await self._grid_out.read(size)

    def sync_mode(self) -> BinaryIOProtocol:
        return GridOutWrapper(self._grid_out)
