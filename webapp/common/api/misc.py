from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from celery_app.celeryapp import app
from conf.config import settings
from utils.health_checker.health_checker import db_alive, db_migrated, workers_alive
from webapp.common.schemas.misc import Health
from webapp.deps import get_db

router = APIRouter()


@router.get(
    '/health_checker',
    response_model=Health,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {'model': Health}},
)
async def healthcheck(response: Response, db: AsyncSession = Depends(get_db)):
    db_liveness: bool = await db_alive(db)
    migrated: bool = await db_migrated(db) if db_liveness else False
    workers_liveness: bool = workers_alive(app, settings.WORKERS_NAME)
    status_msg = {
        'db': 'ok' if db_liveness else 'error',
        'migrations': 'ok' if migrated else 'error',
        'workers': 'ok' if workers_liveness else 'error',
    }

    if not all([db_liveness, migrated, workers_liveness]):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return status_msg
