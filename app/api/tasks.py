from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.db.model import Task 
from app.api.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_embedding import generate_task_embedding

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    embedding = generate_task_embedding(
        task.title,
        task.description,
        task.time
    )

    new_task = Task(
        title=task.title,
        description=task.description,
        time=task.time,
        embedding=str(embedding)  # stored as TEXT for now
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # update only provided fields
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    # regenerate embedding after update
    task.embedding = str(
        generate_task_embedding(
            task.title,
            task.description,
            task.time
        )
    )

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"status": "deleted"}
