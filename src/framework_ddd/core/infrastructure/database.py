import asyncio
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
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Ejecutar la función asíncrona y obtener el Future
            future = asyncio.run_coroutine_threadsafe(self._grid_out.read(size), loop)
            result = future.result()  # type: ignore
        else:
            async def run_async_function():
                future = await self._grid_out.read(size)
                return await future

            result = asyncio.run(run_async_function())

        return result


class AsyncGridOutWrapper(AsyncBinaryIOProtocol):
    def __init__(self, grid_out: AsyncIOMotorGridOut):
        self._grid_out = grid_out

    async def read(self, size: int = -1) -> bytes:
        return await self._grid_out.read(size)

    def sync_mode(self) -> BinaryIOProtocol:
        return GridOutWrapper(self._grid_out)
