import logging
from typing import List

import sqlalchemy as sa
from alembic import config, script
from alembic.runtime import migration
from celery import Celery
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncSession

import conf.config as app_config

logger = logging.getLogger(__name__)


async def db_alive(db: AsyncSession) -> bool:
    liveness: bool = False
    try:
        await db.execute('SELECT 1')
        liveness = True
    except sa.exc.OperationalError as exc:
        logger.warning('HEALTH: %s', exc)
    return liveness


async def db_migrated(db: AsyncSession) -> bool:
    connection = await db.connection()

    def get_current_revision(connection: Connection):
        context = migration.MigrationContext.configure(
            connection=connection,
            opts={'version_table': app_config.settings.ALEMBIC_MIGRATION_VERSION_TABLE},
        )
        return context.get_current_revision()

    current_revision = await connection.run_sync(get_current_revision)
    alembic_cfg = config.Config('conf/alembic.ini')
    script_ = script.ScriptDirectory.from_config(alembic_cfg)
    migrated: bool = current_revision == script_.get_current_head()
    if not migrated:
        logger.warning(
            'HEALTH: migrations in db %s != script %s',
            current_revision,
            script_.get_current_head(),
        )
    return migrated


def workers_alive(app: Celery, workers: List[str]) -> bool:
    ping = app.control.inspect().ping()
    workers_result = {worker: False for worker in workers}
    for ping_key in ping.keys():
        worker_name, worker_id = ping_key.split('@')
        workers_result[worker_name] = True

    return all(workers_result.values())
