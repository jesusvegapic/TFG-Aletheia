from pydantic import BaseModel


class PostCourseRequest(BaseModel):
    teacher_id: str
    name: str
    description: str


class PutLectioRequest(BaseModel):
    name: str
    description: str
