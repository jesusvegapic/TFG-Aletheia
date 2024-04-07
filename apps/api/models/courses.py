from pydantic import BaseModel


class CreateCourseRequest(BaseModel):
    teacher_id: str
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True
