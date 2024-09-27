from typing import List

from pydantic import BaseModel


class PutTeacherCoursesSubscription(BaseModel):
    teacher_id: str
    topics: List[str]
