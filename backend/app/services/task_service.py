# backend/app/services/task_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate,TaskUpdate
from datetime import datetime, timedelta
from sqlalchemy import and_


# CREATE
async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


# READ ALL
async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()


# GET BY ID
async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


# UPDATE
async def update_task(
    db: AsyncSession,
    task_id: int,
    update_data: TaskUpdate
) -> Task | None:

    task = await get_task_by_id(db, task_id)

    if not task:
        return None

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


# DELETE
async def delete_task(db: AsyncSession, task_id: int) -> bool:
    task = await get_task_by_id(db, task_id)

    if not task:
        return False

    await db.delete(task)
    await db.commit()

    return True

# TODAY TASKS
async def get_today_tasks(db: AsyncSession):
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    result = await db.execute(
        select(Task).where(
            and_(
                Task.completed == False,
                Task.due_date >= now,
                Task.due_date < tomorrow
            )
        ).order_by(Task.priority.desc(), Task.due_date.asc())
    )

    return result.scalars().all()