from dataclasses import dataclass
from tempfile import SpooledTemporaryFile


@dataclass
class VideoDto:
    file: SpooledTemporaryFile
    filename: str
    content_type: str
    