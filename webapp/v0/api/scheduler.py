import logging
import uuid
from typing import Optional

import celery
from celery import states
from celery.app.control import Control
from celery.exceptions import CeleryError
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Query
from starlette import status

from celery_app.celeryapp import app
from conf.config import settings
from conf.constants import STATUS_MAP, StatusType
from utils.health_checker.health_checker import workers_alive
from webapp.v0.schemas.task import Task, TaskData, TaskResult, TaskResultData, TaskStatus, TaskStatusData
from workers.constants import WORKERS

logger = logging.getLogger(__name__)

router = APIRouter()

API_VERSION_MAJOR = 0
API_VERSION_MINOR = 1
API_VERSION_PATH = 0

API_VERSION = f'{API_VERSION_MAJOR}.{API_VERSION_MINOR}.{API_VERSION_PATH}'


@router.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(
    worker_name: str = Query(..., regex=f"^({'|'.join(WORKERS.keys())})$"),
    x: Optional[int] = Query(None),
    y: Optional[int] = Query(None),
    z: Optional[int] = Query(None),
):
    worker: celery.Task = WORKERS[worker_name]
    kwargs = {}
    if x is not None:
        kwargs['x'] = x
    if y is not None:
        kwargs['y'] = y
    if z is not None:
        kwargs['z'] = z

    try:
        result: AsyncResult = worker.apply_async(
            kwargs=kwargs,
            expires=settings.CELERY_TIMEOUT,
            expiration=settings.CELERY_TIMEOUT,
            task_limit=settings.CELERY_TASK_LIMIT,
        )
        if not workers_alive(app, [worker_name]):
            worker.update_state(result.id, states.REVOKED)
            Control(app).revoke(result.id)
    except CeleryError as exc:
        logger.exception('Sending task raised: %r', exc)
        raise HTTPException(408, str(exc))

    data: TaskData = TaskData.parse_obj({'task_uuid': result.id})
    return Task(
        version=API_VERSION,
        data=data,
    )


@router.post('/tasks/{task_uuid}/status', response_model=TaskStatus)
async def get_task_status(task_uuid: uuid.UUID):
    try:
        task: AsyncResult = AsyncResult(str(task_uuid))
    except CeleryError as exc:
        logger.exception('Getting task status raised: %r', exc)
        raise HTTPException(408, str(exc))
    data: TaskStatusData = TaskStatusData.parse_obj({'task_uuid': task_uuid, 'status': STATUS_MAP[task.status]})
    return TaskStatus(
        version=API_VERSION,
        data=data,
    )


@router.post('/tasks/{task_uuid}/result', response_model=TaskResult)
async def get_task_result(task_uuid: uuid.UUID):
    try:
        task: AsyncResult = AsyncResult(str(task_uuid))
    except CeleryError as exc:
        logger.exception('Getting task result raised: %r', exc)
        raise HTTPException(408, str(exc))

    result = {'task_uuid': task.id, 'result': str(task.result)}

    if task.status == states.FAILURE:
        result['log'] = task.traceback

    data: TaskResultData = TaskResultData.parse_obj(result)

    return TaskResult(
        version=API_VERSION,
        data=data,
    )
