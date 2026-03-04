from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# CREATE
@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    return await task_service.create_task(db, task_data)


# READ ALL
@router.get("/", response_model=List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await task_service.get_all_tasks(db)


# PUT — Full Replace (or use as full update)
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    task = await task_service.update_task(db, task_id, task_data)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# PATCH — Mark Complete
@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_complete(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    task = await task_service.mark_task_complete(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# DELETE
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await task_service.delete_task(db, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found..")

    return {"message": "Task deleted successfully"}