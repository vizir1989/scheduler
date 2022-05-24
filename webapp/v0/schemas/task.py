from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID

from conf.constants import StatusType


class TaskData(BaseModel):
    task_uuid: UUID

    class Config:
        orm_mode = True


class Task(BaseModel):
    version: str
    data: TaskData


class TaskStatusData(BaseModel):
    task_uuid: UUID
    status: StatusType

    class Config:
        orm_mode = True


class TaskStatus(BaseModel):
    version: str
    data: TaskStatusData


class TaskResultData(BaseModel):
    task_uuid: UUID
    result: Optional[str] = None
    log: Optional[str] = None

    class Config:
        orm_mode = True


class TaskResult(BaseModel):
    version: str
    data: TaskResultData
