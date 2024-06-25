from asyncio import Protocol
from typing import Coroutine, Any


class BinaryIOProtocol(Protocol):
    async def read(self, size: int = -1) -> Coroutine[Any, Any, bytes]: ...
