from typing import List

from pydantic import BaseModel


class GetConferenceHttpResponse(BaseModel):
    id: str
    owner: str
    name: str
    description: str
    topics: List[str]
    video_url: str
