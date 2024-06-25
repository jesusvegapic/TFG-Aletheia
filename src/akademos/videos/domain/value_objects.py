import mimetypes
from src.akademos.videos.domain.errors import VideoNameError, VideoTypeError


class VideoName(str):
    def __new__(cls, name: str):
        if name.__len__() > VideoName.max_length():
            raise VideoNameError(name=name, max_length=VideoName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100


class VideoType(str):
    __VALID_VIDEO_MIMETYPE_PREFIX = "video/"

    def __new__(cls, type: str):
        if (
                not type.startswith(cls.__VALID_VIDEO_MIMETYPE_PREFIX) or
                mimetypes.guess_type(f"file.{type.split('/')[-1]}")[0] != type

        ):
            raise VideoTypeError(type=type)

        return super().__new__(cls, type)
