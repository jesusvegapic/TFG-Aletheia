from src.framework_ddd.core.domain.files import BinaryIOProtocol


class TestBinaryIOProtocol(BinaryIOProtocol):
    async def read(self, size: int = -1):
        return b"blablabla"
