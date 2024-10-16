
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from app.dtos.tasks import TaskCreateDTO, TaskResponseDTO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    task_status = Column(Boolean, default=False)
    deadline_date = Column(DateTime(timezone=True), nullable=False)

async def create_task(db_session: AsyncSession, task_create_dto: TaskCreateDTO) -> TaskResponseDTO:
    task = Task(
        title=task_create_dto.title,
        description=task_create_dto.description,
        task_status=task_create_dto.task_status,
        deadline_date=task_create_dto.deadline_date
    )
    db_session.add(task)
    try:
        await db_session.commit()
        await db_session.refresh(task)
        return TaskResponseDTO.from_orm(task)
    except IntegrityError:
        await db_session.rollback()
        raise ValueError("Task could not be created due to integrity error.")
