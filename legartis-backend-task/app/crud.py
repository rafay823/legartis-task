from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from app.dtos.tasks import *

from app.models import Task
from datetime import datetime

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def create_task(
    db: AsyncSession,
    title: str,
    description: str,
    deadline_date: datetime,
    task_status: bool = False
):
    new_task = Task(title=title, description=description, task_status=task_status, deadline_date=deadline_date)

    db.add(new_task)
    try:
        await db.commit()
        await db.refresh(new_task)
        return new_task
    except IntegrityError:
        await db.rollback()
        raise ValueError("Task could not be created due to integrity error.")

async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskCreateDTO
):
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(
            title=task_data.title,
            description=task_data.description,
            deadline_date=task_data.deadline_date,
            task_status=task_data.task_status
        )
        .execution_options(synchronize_session="fetch")
    )
    try:
        await db.execute(stmt)
        await db.commit()
        updated_task = await db.get(Task, task_id)
        return updated_task
    except IntegrityError:
        await db.rollback()
        raise ValueError("Task could not be updated.")