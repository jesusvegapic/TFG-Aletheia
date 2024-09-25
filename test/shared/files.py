from src.framework_ddd.core.domain.files import BinaryIOProtocol, AsyncBinaryIOProtocol


class TestBinaryIOProtocol(BinaryIOProtocol):
    def read(self, size: int = -1) -> bytes:
        return b"blablabla"


class TestAsyncBinaryIOProtocol(AsyncBinaryIOProtocol):
    async def read(self, size: int = -1):
        return b"blablabla"

    def sync_mode(self) -> BinaryIOProtocol:
        return TestBinaryIOProtocol()
