from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    time: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    time: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
