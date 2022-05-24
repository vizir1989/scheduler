import os
from importlib import import_module

from celery import Celery


def load_app():
    worker_type = os.getenv('WORKER_TYPE', 'base')
    pack_path = ['celery_app', 'celeryconfig', worker_type]

    worker_config = import_module('.'.join(pack_path), package='.')

    app = Celery()
    app.config_from_object(worker_config.Config)

    return app
