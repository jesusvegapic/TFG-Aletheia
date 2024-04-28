from dataclasses import dataclass

from src.shared.domain.ddd.value_objects import ValueObject


@dataclass(frozen=True)
class VideoName(ValueObject):
    value: str


@dataclass(frozen=True)
class VideoType(ValueObject):
    value: str
