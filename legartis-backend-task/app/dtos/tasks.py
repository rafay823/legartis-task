from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class TaskCreateDTO(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    task_status: bool = False
    deadline_date: datetime

    @field_validator('title', 'description')
    def check_not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty or just whitespace')
        return value

# Response Model
class TaskResponseDTO(BaseModel):
    title: str
    description: str
    task_status: bool
    deadline_date: str

    @classmethod
    def from_orm(cls, task_create_dto: TaskCreateDTO):
        return cls(
            title=task_create_dto.title,
            description=task_create_dto.description,
            task_status=task_create_dto.task_status,
            deadline_date=task_create_dto.deadline_date.isoformat()  # Convert to string
        )
